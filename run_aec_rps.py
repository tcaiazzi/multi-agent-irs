import aec_rps
from pettingzoo.test import api_test
# algoritmo con solo tensorflow multi agente senza NN 
from ray.rllib.algorithms import ppo
from ray.tune.registry import register_env
from ray.rllib.algorithms.maddpg.maddpg import MADDPGConfig
from ray.rllib.env import PettingZooEnv
from ray import air
from ray import tune
from ray.rllib.policy import TFPolicy,TorchPolicy
from ray.rllib.policy.policy import PolicySpec
from ray.rllib.examples.policy.rock_paper_scissors_dummies import AlwaysSameHeuristic
from ray.rllib.utils import check_env

import ray
env = aec_rps.env(render_mode="human")
env.reset(seed=42)

register_env("mio",lambda _:PettingZooEnv(env))
ray.init()
""" testEnv = PettingZooEnv(env)
check_env(testEnv) """

""" config = MADDPGConfig()
print(config.replay_buffer_config)  
replay_config = config.replay_buffer_config.update(  
    {
        "capacity": 100000,
        "prioritized_replay_alpha": 0.8,
        "prioritized_replay_beta": 0.45,
        "prioritized_replay_eps": 2e-6,
    }
)
config.training(replay_buffer_config=replay_config)   
config = config.resources(num_gpus=0)   
config = config.rollouts(num_rollout_workers=4)   
config = config.environment("mio")   
algo = config.build()  
algo.train() """



""" testEnv = PettingZooEnv(env)
obsSpace = testEnv.observation_space
print('obsSpace:',obsSpace)
actSpace = testEnv.action_space
print('actSpace:',actSpace) """

""" config = MADDPGConfig()
config.training(n_step=200)  
config.multi_agent(
    policies={
                "attaccante": (PolicySpec(policy_class=AlwaysSameHeuristic),obsSpace,actSpace,{ "agent_id":0 }),
                "difensore": (PolicySpec(policy_class=AlwaysSameHeuristic),obsSpace,actSpace,{ "agent_id":1 }),
            },
            policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),)

config.environment(env="mio")  
config.environment(disable_env_checking=True)
#algo = config.build(env='mio')
#algo.train() """

""" tune.Tuner(  
    "MADDPG",
    run_config=air.RunConfig(stop={"episode_reward_mean":200}),
    param_space=config.to_dict()
).fit() """



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
