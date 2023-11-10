from algoritmiTraining import DQN, ApexDQN,Impala,PG,PPO


pathDQN = '/home/matteo/ray_results/DQN_2023-11-10_12-27-34/DQN_rsp_25267_00000_0_2023-11-10_12-27-34/checkpoint_000000'

pathApexDQN = ''

pathImpala = ''

pathPG = ''

pathPPO =  ''

############################################ PER VEDERLO GIOCARE #####################################
# Così va ma senza polisi sceglie random, ma va la logica della reward e dello stopping

from ray.rllib.algorithms.algorithm import Algorithm
from visualizzazione import visualizza_reward_mosse

# Algoritmi
config = DQN().config
#config = ApexDQN().config
#config = Impala().config
#config = PG().config
#config = PPO().config


# Mi risolve i problemi di mismatch con la rete, non so perche, ma per l'action mask
config['hiddens'] = []
config['dueling'] = False

# per l'evaluation
config['evaluation_interval'] = 1

algo = config.build()

algo.restore(pathDQN)
#algo.restore(pathApexDQN)
#algo.restore(pathImpala)
#algo.restore(pathPG)
#algo.restore(pathPPO)

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