import aec_rps
from pettingzoo.test import api_test
# algoritmo con solo tensorflow multi agente senza NN 
from ray.rllib.algorithms import ppo
from ray.tune.registry import register_env
from ray.rllib.algorithms.maddpg.maddpg import MADDPGConfig
from ray.rllib.env import PettingZooEnv,MultiAgentEnv
from ray import air
from ray import tune
from ray.rllib.policy import TFPolicy,TorchPolicy
from ray.rllib.policy.policy import PolicySpec
from ray.rllib.examples.policy.rock_paper_scissors_dummies import AlwaysSameHeuristic
from ray.rllib.utils import check_env
from ray.rllib.algorithms.qmix import QMixConfig

import ray

env = aec_rps.env(render_mode="human")
env.reset(seed=42)
#register_env("mio",lambda _:MultiAgentEnv(env))

#ray.init()

""" config = QMixConfig()  
config = config.training(gamma=0.9, lr=0.01)  
config = config.resources(num_gpus=0)  
config = config.rollouts(num_rollout_workers=4)
congig = config.disable_env_checking = True
print(config.to_dict())  
# Build an Algorithm object from the config and run 1 training iteration.
algo = config.build(env='mio')  
algo.train()   """

""" register_env("grouped_test", MultiAgentEnv(env,))
results = tune.run(
    "QMIX",
    stop={"timesteps_total": 5,},
    config={
        "mixer": "qmix",
        "env": "grouped_test",
        "env_config": {"agents": ["0", "1", "2"]},
        "num_workers": 0,
        "timesteps_per_iteration": 2,
    },
) """


# Così va ma senza polisi sceglie random, ma va la logica della reward e dello stopping

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

env.close()


register_env("grouped_test", aec_rps.env(render_mode="human"))
results = tune.run(
    "QMIX",
    stop={"timesteps_total": 5,},
    config={
        "mixer": "qmix",
        "env": "grouped_test",
        "env_config": {"agents": ["0", "1"]},
        "num_workers": 0,
        "timesteps_per_iteration": 2,
    },
)
