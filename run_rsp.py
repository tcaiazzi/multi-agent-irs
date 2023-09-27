import rsp
from pettingzoo.test import api_test
# algoritmo con solo tensorflow multi agente senza NN 
from ray.rllib.algorithms import ppo
from ray.tune.registry import register_env
from ray.rllib.algorithms.maddpg.maddpg import MADDPGConfig
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

import ray

import os

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

#from pettingzoo.classic import leduc_holdem_v4

torch, nn = try_import_torch()

stop = {
        "training_iteration": 1,
        "timesteps_total": 100000,
        "episode_reward_mean": 1000.0,
    }


def env_creator():
        #env = RLCardBase("leduc-holdem", 2, (36,))
        #env = aec_rps.env(render_mode="human")
        env = rsp.env(render_mode="human")
        #env = TestEnv()
        #env = MyEnv()
        return env

env_name = "leduc_holdem_v4"
register_env(env_name, lambda config: PettingZooEnv(env_creator()))

test_env = PettingZooEnv(env_creator())
obs_space = test_env.observation_space
act_space = test_env.action_space

config = PGConfig().environment(env_name,disable_env_checking=True).framework("torch").multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    )
results = tune.Tuner(
        "PG", param_space=config, run_config=air.RunConfig(stop=stop, verbose=1)
    ).fit()
print(results)


# Così va ma senza polisi sceglie random, ma va la logica della reward e dello stopping
""" env = aec_rps.env(render_mode="human")
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
            # this is where you would insert your policy
            # qui dovrei inserire l'algoritmo che mi identifica la policy(?)
            #mask = observation["action_mask"]
            action = env.action_space(agent).sample()

        print('Azione selezionata da esegire:',action)
        print('Reward accumulata:',reward)
        print('Termination:',termination)
        print('Troncation:',truncation)
        print('Step:')
        env.step(action)
    else:
        #api_test(env, num_cycles=1000, verbose_progress=True)
        env.close()
        break

env.close() """

