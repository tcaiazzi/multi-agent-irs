# se lancio dalla cartella principale
import sys 

sys.path.append('./')

from  visualizzazione import visualizza_reward_mosse

from algoritmiTraining import Impala

from ray.rllib.algorithms.algorithm import Algorithm


# 10 training operation: circa 1500 partite con un totale di 7600 mosse circa, molto bene (anche meno ma ci ha messo poco
# ad addestrarsi, i valori anche nel training molto bene)
# sembra instabile ma veloce a convergere ed è veloce
#pathImpala = '/home/matteo/ray_results/IMPALA_2023-11-10_14-12-54/IMPALA_rsp_dbbe5_00000_0_2023-11-10_14-12-54/checkpoint_000000'
# 20 training iteration
pathImpala = '/home/matteo/ray_results/IMPALA_2023-11-13_15-21-42/IMPALA_rsp_f7fb3_00000_0_2023-11-13_15-21-43/checkpoint_000000'

############################################ PER VEDERLO GIOCARE #####################################
# Così va ma senza polisi sceglie random, ma va la logica della reward e dello stopping


# Algoritmi
config = Impala().config

# Mi risolve i problemi di mismatch con la rete, non so perche, ma per l'action mask
config['hiddens'] = []
config['dueling'] = False

# per l'evaluation
config['evaluation_interval'] = 1

algo = config.build()

algo.restore(pathImpala)

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