import rsp
import ray
import time

from ray import tune
from ray import train
from ray import air

from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.tune import Stopper

from ray.rllib.algorithms.impala import ImpalaConfig
from ray.rllib.algorithms.pg import PGConfig
from ray.rllib.algorithms.dqn import DQNConfig
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.algorithms.apex_dqn.apex_dqn import ApexDQNConfig

from ray.rllib.utils.framework import try_import_torch
from ray.rllib.utils import check_env

from ray.rllib.examples.models.action_mask_model import TorchActionMaskModel

from ray.tune.registry import register_env

from ray.rllib.models import ModelCatalog

from ray.rllib.env import PettingZooEnv

from pettingzoo.test import api_test
from pettingzoo.test import performance_benchmark

import sys


# SERVE PER AVERE LO SPAZIO DELLE AZIONI DI DIMENSIONI DIVERSE
# e VOLENDO ANCHE LE OBSERVATIONs
from supersuit.multiagent_wrappers import pad_action_space_v0,pad_observations_v0


# NEI RESULT TROVIAMO:
# episode_length NUMERO DEI TURNI PRIMA DELLA TERMINAZIONE (1 SOLO ATTACCANTE, 2 ATTACCANTE+DIFENSORE ...)
# policy_*_reward METTE SOLO LE REWARD OTTENUTE DALL'AGENTE QUANDO VINCE
# episode_reward È LA SOMMA DELLE REWARD ATTACCANTE E DIFENSORE (AD OGNI TURNO NE VINCE UNO SOLO)
# MI SON FATTO UN RESULT TUTTO MIO CUSTOM, PER ORA SCRIVE SUL FILE MA MODIFICABILE

# prendo parametri in input
# AZIONI NON AUMENTABILI AUTOMATICAMENTE PERCHE COME CODIFICO IL SUO COMPORTAMENTO? ERRORE QUANDO SELEZIONA QUELLA MOSSA
# SPAZIO DELLE OSSERVAZIONI ANCHE, POTREBBE NON GIUNGERE PIU ALL'ARRESTO PERCHÈ LE AZIONI NON LO MODIFICANO
# GLI AGENTI POTREI (da pensare)
""" if len(sys.argv) == 4:
    lr = sys.argv[1]
    n_mosse = sys.argv[2] 
    n_iterazioni = sys.argv[3]
    print('lr:',lr)
    print('n_mosse:',n_mosse)
    print('n_iterazioni:',n_iterazioni) """


torch, nn = try_import_torch()
torch.cuda.empty_cache()

# COndizioni di stopping degli algoritmi 
stop = {
        # epoche/passi dopo le quali il training si arresta
        "training_iteration": 2,

        "timesteps_total":2,

        # passi ambientali dell'agente nell'ambiente
        # ci sarebbe un minimo di 200
        "timesteps_total": 2,

        # ferma il training quando la ricompensa media dell'agente nell'episodio è pari o maggiore
        "episode_reward_max": 100,
    }

# RAY  VIENE UTILIZZATO PER POTER FARE IL TUNING DEGLI IPERPARAMETRI
# SI PUO DEFINIRE UN RANGE ED IN AUTOMATICA FA I DIVERSI TRAINING CON LE DIVERSE CONFIG
ray.shutdown()
ray.init()

# Definisco il mio ambiente
def env_creator():
        env = rsp.env(render_mode="human")
        return env

# Nome ambiente
env_name = "rsp"

# Registro il mio ambiente
register_env(env_name, lambda config: PettingZooEnv(pad_action_space_v0(env_creator())))
#register_env(env_name, lambda config: PettingZooEnv(pad_observations_v0(pad_action_space_v0(env_creator()))))

# Mi serve per usare l'action mask in odo da avere ad ogni step solo specifiche mosse
# senza dover gestire io mosse non selezionabili
ModelCatalog.register_custom_model("am_model", TorchActionMaskModel)

# Mi servono per il check e l'inizializzazione degli algoritmi
test_env = PettingZooEnv(pad_action_space_v0(env_creator()))
obs_space = test_env.observation_space
act_space = test_env.action_space

# Verifico l'ambiente così ch se faccio modifiche me lo dice senza fare il running e l'inizializzazione degli algoritmi
check_env(test_env)

################################################# RAY #######################################
############################################## APEX-DQN #####################################
#############################################################################################
# è un DQN evoluto, ovvero DQN su architettura APE-x (una gpu che apprende e più worker cpu che collezionano esperienza)
""" 
# Fa dei controlli ad ogni episodi, così ad esempio si ferma la partita quando la cuulative reward del difensore super i 100
class MyCallbacks(DefaultCallbacks):
    def on_episode_end(self, worker, base_env, policies, episode, **kwargs):
        # Controlla il valore della cumulative reward
        if episode.agent_rewards['difensore'] > 100:
            return True  # Interrompi il training """

# Sempre che stia funzionando lo stopping a tempo
class TimeStopper(Stopper):
    def __init__(self):
        self._start = time.time()
        self._deadline = 60  # Stop all trials after 2 seconds

    def __call__(self, trial_id, result):
        return False

    def stop_all(self):
        return time.time() - self._start > self._deadline
    
config = (
    ApexDQNConfig()
    .environment(
            env=env_name
    ).resources(
            num_gpus=1
    ).rollouts(
            num_rollout_workers=1,
            rollout_fragment_length=30
    ).training(
            train_batch_size=200,
            model = { 
                    "custom_model": "am_model",
                }
    ).multi_agent(
            policies={
                    "attaccante": (None, obs_space, act_space, {}),
                    "difensore": (None, obs_space, act_space, {}),
            },
            policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).debugging(
    ).framework(
            framework="torch"
    ).exploration(
            exploration_config={
                    # The Exploration class to use.
                    "type": "EpsilonGreedy",
                    # Config for the Exploration class' constructor:
                    "initial_epsilon": 0.1,
                    "final_epsilon": 0.0,
                    "epsilon_timesteps": 100000,  # Timesteps over which to anneal epsilon.
            }
    )
)

# Mi risolve i problemi di mismatch con la rete
config['hiddens'] = []
config['dueling'] = False

# Actin mask
#config["env_config"] = {"use_action_masking": True}


#config['evaluation_interval'] = 1
#config['create_env_on_driver'] = True

# Qui non ho la stop condition
""" algo = config.build()
results = algo.train()
results = algo.evaluate()
print(results) """


results = tune.Tuner(
    "APEX",
    run_config = train.RunConfig(stop=TimeStopper(),verbose=1),
    param_space = config.to_dict(),
).fit()
print(results)

#############################################################################################
###############################################  DQN  #######################################
#############################################################################################

config = (
    DQNConfig()
    .environment(
            env=env_name
    ).resources(
                    
    ).rollouts(
            num_rollout_workers=1,
            rollout_fragment_length=30
    ).multi_agent(
            policies={
                    "attaccante": (None, obs_space, act_space, {}),
                    "difensore": (None, obs_space, act_space, {}),
                },
            policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).debugging(
            log_level="DEBUG"
    ).framework(
            framework="torch"
    ).exploration(
            exploration_config={
                    # The Exploration class to use.
                    "type": "EpsilonGreedy",
                    # Config for the Exploration class' constructor:
                    "initial_epsilon": 0.1,
                    "final_epsilon": 0.0,
                    "epsilon_timesteps": 100000,  # Timesteps over which to anneal epsilon.
                }
    ).training(
            model = { 
                    "custom_model": "am_model", 
                }
    )#.callbacks(MyCallbacks)
)

# Mi risolve i problemi di mismatch con la rete, non so perche, ma per l'action mask
config['hiddens'] = []
config['dueling'] = False

# NON RICORDO IL PERCHE'
#config['evaluation_interval'] = 1
#config['create_env_on_driver'] = True

""" algo = config.build()
algo.train()
results = algo.evaluate()
print(results) """


""" results = tune.Tuner(
    "DQN",
    run_config = train.RunConfig(stop=stop,verbose=1),
    param_space = config.to_dict(),
).fit() """


###################################################################################################
#########################################  IMPALA-PG-PPO  #########################################
# Sono algoritmi che permettono l'implementazioni di reti neurali come lSTM-RNN-... 
# l'environment riceve un'azione genera un'observation e va in input al modello (policy class)
# di default asseconda dell'input/ azione/ ... sono definite di default delle reti (Fully, conv, ecc...)

# "use_lstm": True or "use_attention": True in your model config
# you can specify the size of the LSTM layer by 
# all keys: ['_disable_preprocessor_api', '_disable_action_flattening', 'fcnet_hiddens', 'fcnet_activation', 
#               'conv_filters', 'conv_activation', 'post_fcnet_hiddens', 'post_fcnet_activation', 'free_log_std',
#               'no_final_linear', 'vf_share_layers', 'use_lstm', 'max_seq_len', 'lstm_cell_size', 'lstm_use_prev_action',
#               'lstm_use_prev_reward', '_time_major', 'use_attention', 'attention_num_transformer_units', 
#               'attention_dim', 'attention_num_heads', 'attention_head_dim', 'attention_memory_inference', 
#               'attention_memory_training', 'attention_position_wise_mlp_dim', 'attention_init_gru_gate_bias', 
#               'attention_use_n_prev_actions', 'attention_use_n_prev_rewards', 'framestack', 'dim', 'grayscale', 
#               'zero_mean', 'custom_model', 'custom_model_config', 'custom_action_dist', 'custom_preprocessor', 
#               'encoder_latent_dim', 'always_check_shapes', 'lstm_use_prev_action_reward', '_use_default_native_models']

# POSSO FARE ANCHE UN CUSTOM MODEL (o come in deep o con i parametri sopra)
# https://docs.ray.io/en/latest/rllib/rllib-models.html#built-in-auto-lstm-and-auto-attention-wrappers

###################################################################################################
###############################################  IMPALA  ##########################################
###################################################################################################
# Basato sullo Stocasthic gradient discent (SGD)
# gradiente stimato e non calcolato

config = (
      ImpalaConfig()
      .environment(env_name,disable_env_checking=True)
      .resources(num_gpus=1)
      .framework("torch")
      .multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).training(
          model={
                "custom_model": "am_model"
                },
    )
)

config['evaluation_interval'] = 1
config['create_env_on_driver'] = True

""" 
algo = config.build()
algo.train()
results = algo.evaluate()
print(results)  """

""" results = tune.Tuner(
        "IMPALA", param_space=config.to_dict(), run_config=air.RunConfig(stop=stop, verbose=1)
    ).fit()  """


############################################################################################
##############################################  PG  ########################################
############################################################################################
# Policy gradient
# vanilla policy gradients using experience collected from the latest interaction with the agent implementation 
# (using experience collected from the latest interaction with the agent)

config = (
      PGConfig()
      .environment(env_name,disable_env_checking=True)
      .resources(num_gpus=1)
      .framework("torch")
      .multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).training(
          model={
                "custom_model": "am_model"
                },
    )
)  

config['evaluation_interval'] = 1
config['create_env_on_driver'] = True

""" 
algo = config.build()
algo.train()
results = algo.evaluate()
print('RESULTS:',results) """

""" results = tune.Tuner(
        "PG",
        param_space=config.to_dict(), 
        run_config=air.RunConfig(stop=stop, verbose=1)
    ).fit()
config.evaluation() """

##################################################################################################
################################################  PPO  ###########################################
##################################################################################################
# Proximal Policy Optimization e fa uso del PG con l'aggiunta di clipped objective function 
# (penalizzando grandicambiamenti nella policy)
# PG avanzato piu veloce
# multiple SGD 

config = (
      PPOConfig()
      .environment(env_name,disable_env_checking=True)
      .resources(num_gpus=1)
      .framework("torch")
      .multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).training(
          model={
                "custom_model": "am_model"
                },
    )
)
# PER IL CUSTOM_MODEL
config.rl_module( _enable_rl_module_api=False)
config.training(_enable_learner_api=False)

config['evaluation_interval'] = 1
config['create_env_on_driver'] = True 

""" algo = config.build()
algo.train()
algo.evaluate()
results = algo.evaluate()
print('RESULTS:',results) """

""" results = tune.Tuner(
        "PPO", param_space=config.to_dict(), run_config=air.RunConfig(stop=stop, verbose=1,checkpoint_config=air.CheckpointConfig(checkpoint_at_end=True))
    ).fit()  """






############################################ PER VEDERLO GIOCARE #####################################
# Così va ma senza polisi sceglie random, ma va la logica della reward e dello stopping
""" env = rsp.env(render_mode="human")
env.reset(seed=42)
action = 0

for agent in env.agent_iter():

    if len(env.agents)>1:
        print('\n')
        print('Seleziono agente:',agent)
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            action = None
        else:
            # this is where you would insert your polic
            mask = observation["action_mask"]
            action = env.action_space(agent).sample(mask)

        print('Osservazione:',observation)
        print('Azione selezionata da eseguire:',action)
        print('Reward accumulata:',reward)
        print('Termination:',termination)
        print('Troncation:',truncation)
        print('Step:')
        env.step(action)
    else:
        api_test(env, num_cycles=1000, verbose_progress=True)
        env.close()
        break

env.close() """
