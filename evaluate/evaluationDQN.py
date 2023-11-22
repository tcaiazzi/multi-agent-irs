# se lancio dalla cartella principale
import sys 

sys.path.append('./')

from  visualizzazione import visualizza_reward_mosse

from algoritmiTraining import DQN

from ray.rllib.algorithms.algorithm import Algorithm


# 20 training iteration
#pathDQN = '/home/matteo/ray_results/DQN_2023-11-10_12-40-26/DQN_rsp_f0eb6_00000_0_2023-11-10_12-40-26/checkpoint_000000'
# 1 iteration
pathDQN = sys.argv[1]

# Algoritmi
config = DQN().config

# Mi risolve i problemi di mismatch con la rete, non so perche, ma per l'action mask
config['hiddens'] = []
config['dueling'] = False

# per l'evaluation
config['evaluation_interval'] = 1

algo = config.build()

algo.restore(pathDQN)

algo.evaluate()

visualizza_reward_mosse()









#######################################################################################################################

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