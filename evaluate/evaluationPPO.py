# se lancio dalla cartella principale
import sys 

sys.path.append('./')

from  visualizzazione import visualizza_reward_mosse


from algoritmiTraining import PPO

from ray.rllib.algorithms.algorithm import Algorithm



# per 20 mi sembra che ci stia mettendo anche piu tempo di PG dopo prendi i tempi
# Sembra partire meglio fin da subito, ovvero sembra piu stabile il grafico ma converge piu lentamente
# in realta con 200 partite ha fatto sia la convergena e con piu stabilità rispetto agli altri
# pero piu lento in realta pero nell'evaluation fa 6 mosse e non 4 mmmh
#pathPPO =  '/home/matteo/ray_results/PPO_2023-11-10_14-32-44/PPO_rsp_a15d1_00000_0_2023-11-10_14-32-44/checkpoint_000000'
# 20 training iteration
#pathPPO = '/home/matteo/ray_results/PPO_2023-11-13_15-29-22/PPO_rsp_09b75_00000_0_2023-11-13_15-29-22/checkpoint_000000'
#pathPPO = '/home/matteo/ray_results/PPO_2023-11-14_12-11-47/PPO_rsp_9a365_00000_0_2023-11-14_12-11-47/checkpoint_000000'
pathPPO = sys.argv[1]
############################################ PER VEDERLO GIOCARE #####################################
# Così va ma senza polisi sceglie random, ma va la logica della reward e dello stopping


# Algoritmi
config = PPO().config

# Mi risolve i problemi di mismatch con la rete, non so perche, ma per l'action mask
config['hiddens'] = []
config['dueling'] = False

# per l'evaluation
config['evaluation_interval'] = 1

algo = config.build()

algo.restore(pathPPO)

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