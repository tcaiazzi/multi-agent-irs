import rsp
from pettingzoo.test import api_test
# algoritmo con solo tensorflow multi agente senza NN 
from ray.rllib.algorithms import ppo
from ray.tune.registry import register_env
from ray.rllib.algorithms.bandit.bandit import BanditLinUCBConfig
from ray.rllib.algorithms.pg import PGConfig
from ray.rllib.env import PettingZooEnv,MultiAgentEnv
from ray import air
from ray import tune
from ray.rllib.policy import TFPolicy,TorchPolicy
from ray.rllib.policy.policy import PolicySpec
from ray.rllib.examples.policy.rock_paper_scissors_dummies import AlwaysSameHeuristic
from ray.rllib.utils import check_env
from ray.rllib.algorithms.qmix import QMixConfig
from gymnasium.spaces import Discrete, Dict, Box,Tuple
import numpy as np
from ray.rllib.algorithms.dqn import DQNConfig
from pettingzoo.test import performance_benchmark
import ray
from gymnasium.spaces import Box, Discrete
from ray import tune
from ray.rllib.algorithms.dqn import DQNConfig
from ray.rllib.algorithms.dqn.dqn_torch_model import DQNTorchModel
from ray.rllib.env import PettingZooEnv
from ray.rllib.models import ModelCatalog
from ray.rllib.models.torch.fcnet import FullyConnectedNetwork as TorchFC
from ray.rllib.utils.framework import try_import_torch
from ray.rllib.utils.torch_utils import FLOAT_MAX
from ray.tune.registry import register_env
import os
from ray.rllib.algorithms.impala import ImpalaConfig
from stable_baselines3 import DQN
import gymnasium as gym
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.algorithms.apex_dqn.apex_dqn import ApexDQNConfig
from ray.rllib.algorithms.algorithm import Algorithm
import sys
from ray.rllib.examples.env.action_mask_env import ActionMaskEnv
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
if len(sys.argv) == 4:
    lr = sys.argv[1]
    n_mosse = sys.argv[2] 
    n_iterazioni = sys.argv[3]
    print('lr:',lr)
    print('n_mosse:',n_mosse)
    print('n_iterazioni:',n_iterazioni)


torch, nn = try_import_torch()

# COndizioni di stopping degli algoritmi 
stop = {
        # epoche/passi dopo le quali il training si arresta
        "training_iteration": 1,

        # passi ambientali dell'agente nell'ambiente
        # ci sarebbe un minimo di 200
        #"timesteps_total": 3000,

        # ferma il training quando la ricompensa media dell'agente nell'episodio è pari o maggiore
        #"episode_reward_mean": 200,
    }

# Ray
ray.shutdown()
ray.init()


def env_creator():
        #env = RLCardBase("leduc-holdem", 2, (36,))
        #env = aec_rps.env(render_mode="human")
        env = rsp.env(render_mode="human")
        #env = TestEnv()
        #env = MyEnv()
        return env

env_name = "rsp"
register_env(env_name, lambda config: PettingZooEnv(pad_action_space_v0(env_creator())))
#register_env(env_name, lambda config: PettingZooEnv(pad_observations_v0(pad_action_space_v0(env_creator()))))

# Mi servono per il check e l'inizializzazione degli algoritmi
test_env = PettingZooEnv(pad_action_space_v0(env_creator()))
#test_env = PettingZooEnv(pad_observations_v0(pad_action_space_v0(env_creator())))
obs_space = test_env.observation_space
act_space = test_env.action_space

# Verifico l'ambiente così ch se faccio modifiche me lo dice senza fare il running e l'inizializzazione degli algoritmi
check_env(test_env)

################################################# RAY #######################################
############################################## APEX-DQN #####################################
#############################################################################################
# è un DQN evoluto, ovvero DQN su architettura APE-x (una gpu che apprende e più worker cpu che collezionano esperienza)

""" config = ApexDQNConfig().environment(env=env_name).resources(num_gpus=1).rollouts(
     num_rollout_workers=1, rollout_fragment_length=30
     ).training(
        train_batch_size=200
        #model={"custom_model": "pa_model"},
    ).multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).debugging(
        log_level="DEBUG"
    ).framework(framework="torch").exploration(
        exploration_config={
            # The Exploration class to use.
            "type": "EpsilonGreedy",
            # Config for the Exploration class' constructor:
            "initial_epsilon": 0.1,
            "final_epsilon": 0.0,
            "epsilon_timesteps": 100000,  # Timesteps over which to anneal epsilon.
        }
    )
config['evaluation_interval'] = 1
config['create_env_on_driver'] = True
algo = config.build()
algo.train()
results = algo.evaluate()

print(results.results) """

""" 
results = tune.run(
    "APEX",
    stop=stop,
    checkpoint_freq=10,
    config=config.to_dict(),
)
 """
#############################################################################################
###############################################  DQN  #######################################
#############################################################################################
""" config = DQNConfig().environment(
      env=env_name
      ).resources().rollouts(
            num_rollout_workers=1, rollout_fragment_length=30
            ).multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).debugging(
        log_level="DEBUG"
    ).framework(framework="torch").exploration(
        exploration_config={
            # The Exploration class to use.
            "type": "EpsilonGreedy",
            # Config for the Exploration class' constructor:
            "initial_epsilon": 0.1,
            "final_epsilon": 0.0,
            "epsilon_timesteps": 100000,  # Timesteps over which to anneal epsilon.
        }
    ).training(train_batch_size=200)
config['evaluation_interval'] = 1
config['create_env_on_driver'] = True
algo = config.build()
print('TRAINING...')
algo.train()
print('EVALUATE...')
results = algo.evaluate()
print(results.results) """

""" results = tune.run(
    "DQN",
    name="DQN",
    stop=stop,
    checkpoint_freq=10,
    config=config.to_dict(),
)
 """

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

""" config = ImpalaConfig().environment(env_name,disable_env_checking=True).resources(num_gpus=1).framework("torch").multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).training(
          model={
                # only one may be TRUe di use_*
                'use_lstm': False,
                'lstm_cell_size': 64,
                'use_attention': False
          }
    )
config['evaluation_interval'] = 1
config['create_env_on_driver'] = True


algo = config.build()
print('TRAINING...')
algo.train()
print('EVALUATE...')
results = algo.evaluate()
print(results)  """

""" results = tune.Tuner(
        "IMPALA", param_space=config, run_config=air.RunConfig(stop=stop, verbose=1)
    ).fit() 
 """
############################################################################################
##############################################  PG  ########################################
############################################################################################
# Policy gradient
# vanilla policy gradients using experience collected from the latest interaction with the agent implementation 
# (using experience collected from the latest interaction with the agent)
from ray.rllib.examples.models.action_mask_model import ActionMaskModel
ModelCatalog.register_custom_model("pa_model", ActionMaskModel)

config = PGConfig().environment(env_name,disable_env_checking=True).resources(num_gpus=1).framework("torch").multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {
                #  "model": {
                #    "custom_model": ActionMaskModel,
                #},
                #"use_action_mask": True,
            }),
            "difensore": (None, obs_space, act_space, {
                #  'model': {
                #    'custom_model': ActionMaskModel,
                #},
                #'use_action_mask': True,
            }),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).training(
          model={
                'use_lstm': False,
                'use_attention':False,
          }
    )

config['evaluation_interval'] = 1
config['create_env_on_driver'] = True

algo = config.build()
print('TRAINING...')
algo.train()
""" 
print('EVALUATE...')
results = algo.evaluate(2)
print(results) """

""" results = tune.Tuner(
        "PG",
        param_space=config, 
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

""" config = PPOConfig().environment(env_name,disable_env_checking=True).resources(num_gpus=1).framework("torch").multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).training(
          model={
                'use_lstm':True
          }
    )

config['evaluation_interval'] = 1
config['create_env_on_driver'] = True

algo = config.build()
print('TRAINING...')
algo.train()
print('EVALUATE...')
algo.evaluate()
results = algo.evaluate()
print('RESULTS')
print(results) """

""" results = tune.Tuner(
        "PPO", param_space=config, run_config=air.RunConfig(stop=stop, verbose=1,checkpoint_config=air.CheckpointConfig(checkpoint_at_end=True))
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
