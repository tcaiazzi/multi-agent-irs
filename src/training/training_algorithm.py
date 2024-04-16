from ray.rllib.algorithms.apex_dqn.apex_dqn import ApexDQNConfig
import rsp
from ray.rllib.algorithms.apex_dqn.apex_dqn import ApexDQNConfig
from ray.rllib.algorithms.dqn import DQNConfig
from ray.rllib.algorithms.impala import ImpalaConfig
from ray.rllib.algorithms.pg import PGConfig
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env import PettingZooEnv
from ray.rllib.examples.models.action_mask_model import TorchActionMaskModel
from ray.rllib.models import ModelCatalog
from ray.rllib.utils import check_env
from ray.tune.registry import register_env
# SERVE PER AVERE LO SPAZIO DELLE AZIONI DI DIMENSIONI DIVERSE
# e VOLENDO ANCHE LE OBSERVATIONs
from supersuit.multiagent_wrappers import (pad_action_space_v0)

env_name = "rsp"


# Definisco il mio ambiente
def env_creator(algorithm: str, type_of_test: str, num_agents: int, num_att_actions: int, k_att: float,
                num_def_actions: int, k_def: float):
    # Nome ambiente
    env = rsp.env(algorithm, type_of_test, num_agents, num_att_actions, k_att, num_def_actions, k_def,
                  render_mode="human")
    # Registro il mio ambiente
    register_env(env_name, lambda config: PettingZooEnv(pad_action_space_v0(env)))
    # register_env(env_name, lambda config: PettingZooEnv(pad_observations_v0(pad_action_space_v0(env_creator()))))

    # Mi serve per usare l'action mask in odo da avere ad ogni step solo specifiche mosse
    # senza dover gestire io mosse non selezionabili
    ModelCatalog.register_custom_model("am_model", TorchActionMaskModel)

    # Mi servono per il check e l'inizializzazione degli algoritmi
    test_env = PettingZooEnv(pad_action_space_v0(env))
    obs_space = test_env.observation_space
    act_space = test_env.action_space

    # Verifico l'ambiente così ch se faccio modifiche me lo dice senza fare il running e l'inizializzazione degli algoritmi
    check_env(test_env)

    return obs_space, act_space


# ROLLOUT = PARTITE PER EPOCA ( IMPOSTATE PERCHE ALCUNI ALG COME IMPALA E PG NON ERANO DI DEFAULT 10)
# NUM_CPUS_FOR_LOCAL_WORKER = CPU PER IL TRINER
# NUM_ROLLOUT_WORKER = OGNUGNO UNA CPU PER ADDESTRAMENTO PARALLELO


class DQN:
    def __init__(self, type_of_test: str, num_agents: int, num_att_actions: int, k_att: float, num_def_actions: int,
                 k_def: float):
        obs_space, act_space = env_creator(self.__class__.__name__, type_of_test,
                                           num_agents, num_att_actions, k_att, num_def_actions, k_def)
        self.config = (
            DQNConfig()
            .environment(
                env=env_name
            ).resources(num_gpus=0)
            .rollouts(
                num_rollout_workers=3,
                rollout_fragment_length=10
            ).multi_agent(
                policies={
                    "attacker": (None, obs_space, act_space, {}),
                    "defender": (None, obs_space, act_space, {}),
                },
                policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
            ).debugging(
                log_level="INFO"
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
                model={
                    "custom_model": "am_model",
                },
            )  # .callbacks(MyCallbacks)
        )


class ApexDQN:
    def __init__(self, type_of_test, num_agents: int, num_att_actions: int, k_att: float, num_def_actions: int,
                 k_def: float):
        obs_space, act_space = env_creator(self.__class__.__name__, type_of_test, num_agents, num_att_actions, k_att,
                                           num_def_actions, k_def)
        self.config = (
            ApexDQNConfig()
            .environment(
                env=env_name
            ).resources(num_gpus=0, num_cpus_for_local_worker=0, num_cpus_per_worker=2)
            .rollouts(
                num_rollout_workers=2,
                rollout_fragment_length=10,
            ).training(
                train_batch_size=200,
                model={
                    "custom_model": "am_model",
                }
            ).multi_agent(
                policies={
                    "attacker": (None, obs_space, act_space, {}),
                    "defender": (None, obs_space, act_space, {}),
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


# Strano l'attaccante si addestra a scegliere nop e poi difensore -log e finisce, non vorrei che minimizzasse 
# Però se così fosse il difensore non terminerebbe subito
class Impala:
    def __init__(self, type_of_test, num_agents: int, num_att_actions: int, k_att: float, num_def_actions: int,
                 k_def: float):
        obs_space, act_space = env_creator(self.__class__.__name__, type_of_test, num_agents, num_att_actions, k_att,
                                           num_def_actions, k_def)
        self.config = (
            ImpalaConfig()
            .environment(env_name, disable_env_checking=True)
            .resources(num_gpus=0, num_cpus_for_local_worker=4, num_cpus_per_worker=2)
            .framework("torch")
            .multi_agent(
                policies={
                    "attacker": (None, obs_space, act_space, {}),
                    "defender": (None, obs_space, act_space, {}),
                },
                policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
            ).training(
                model={
                    "custom_model": "am_model"
                },
            ).rollouts(
                num_rollout_workers=2,
                rollout_fragment_length=10,
            ).exploration(

            )
        )


# Con 100 training iteration ho visto che le partite terminano con il difensore che in una media di 50 mosse vince
# PER ora tra PPO con 50 e Impala con 40 lui con 100 è il migliore (piu o meno il tempo di addstramento è stato lo stesso,
# se non quantop meno accettabile da attendere, perciò sono stati scelti questi valori di training non per 
# performance uguali)
class PG:
    def __init__(self, type_of_test, num_agents: int, num_att_actions: int, k_att: float, num_def_actions: int,
                 k_def: float):
        obs_space, act_space = env_creator(self.__class__.__name__, type_of_test, num_agents, num_att_actions, k_att,
                                           num_def_actions, k_def)
        self.config = (
            PGConfig()
            .environment(env_name, disable_env_checking=True)
            .resources(num_gpus=0, num_cpus_for_local_worker=1, num_cpus_per_worker=1)
            .framework("torch")
            .multi_agent(
                policies={
                    "attacker": (None, obs_space, act_space, {}),
                    "defender": (None, obs_space, act_space, {}),
                },
                policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
            ).training(
                model={
                    "custom_model": "am_model"
                },
            ).rollouts(
                num_rollout_workers=1,
                rollout_fragment_length=10,
            ).exploration(
            )
        )

    # Con 50 epoche alcune le vince altre le perde, PG mi sembrava vincesse sempre (potrei sbagliare) pero partite piu brevi


class PPO:
    def __init__(self, type_of_test, num_agents: int, num_att_actions: int, k_att: float, num_def_actions: int,
                 k_def: float):
        obs_space, act_space = env_creator(self.__class__.__name__, type_of_test, num_agents, num_att_actions, k_att,
                                           num_def_actions, k_def)
        self.config = (
            PPOConfig()
            .environment(env_name, disable_env_checking=True)
            # cpu_for_local_worker è per il training del ppo, devo capire quali per i rollout worker
            .resources(num_gpus=0, num_cpus_for_local_worker=2, num_cpus_per_worker=2)
            .framework("torch")
            .multi_agent(
                policies={
                    "attacker": (None, obs_space, act_space, {}),
                    "defender": (None, obs_space, act_space, {}),
                },
                policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
            ).training(
                model={
                    "custom_model": "am_model"
                },
            ).rollouts(
                num_rollout_workers=3,
            ).exploration(
            )
        )
        # PER IL CUSTOM MODEL ERROR
        self.config.rl_module(_enable_rl_module_api=False)
        self.config.training(_enable_learner_api=False)
