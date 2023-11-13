from algoritmiTraining import DQN, ApexDQN,Impala,PG,PPO
from ray.rllib.algorithms.algorithm import Algorithm
from visualizzazione import visualizza_reward_mosse


# 20 training iteration
pathDQN = '/home/matteo/ray_results/DQN_2023-11-10_12-40-26/DQN_rsp_f0eb6_00000_0_2023-11-10_12-40-26/checkpoint_000000'
# 1 iteration
#pathDQN = '/home/matteo/ray_results/DQN_2023-11-10_13-31-51/DQN_rsp_2008b_00000_0_2023-11-10_13-31-51/checkpoint_000000'

# sarebbe dovuto risultare piu veloce ma sul mio non sembra, se dqn riesco a spingermi liberamente a 20 training it.
# con apex ci mette dippiu, 30minuti per 10 trainin iteration e 100 partite(?)
# evaluation bassa
pathApexDQN = '/home/matteo/ray_results/APEX_2023-11-10_14-45-17/APEX_rsp_622c0_00000_0_2023-11-10_14-45-17/checkpoint_000000'

# 10 training operation: circa 1500 partite con un totale di 7600 mosse circa, molto bene (anche meno ma ci ha messo poco
# ad addestrarsi, i valori anche nel training molto bene)
# sembra instabile ma veloce a convergere ed è veloce
#pathImpala = '/home/matteo/ray_results/IMPALA_2023-11-10_14-12-54/IMPALA_rsp_dbbe5_00000_0_2023-11-10_14-12-54/checkpoint_000000'
# 20 training iteration
pathImpala = '/home/matteo/ray_results/IMPALA_2023-11-13_15-21-42/IMPALA_rsp_f7fb3_00000_0_2023-11-13_15-21-43/checkpoint_000000'

# 50 training iteration: meno di 2000 partite con 1450 (? mosse), il training è meno fit di impala
# evaluation bene ma non benissimo, meglio impalaa, anche perchè con moto meno tempo
# Sembra instabile e lento a convergere e lento
#pathPG = '/home/matteo/ray_results/PG_2023-11-10_14-23-40/PG_rsp_5d2bd_00000_0_2023-11-10_14-23-40/checkpoint_000000'
# 20 training iteration
pathPG = '/home/matteo/ray_results/PG_2023-11-13_15-27-23/PG_rsp_c341d_00000_0_2023-11-13_15-27-24/checkpoint_000000'

# per 20 mi sembra che ci stia mettendo anche piu tempo di PG dopo prendi i tempi
# Sembra partire meglio fin da subito, ovvero sembra piu stabile il grafico ma converge piu lentamente
# in realta con 200 partite ha fatto sia la convergena e con piu stabilità rispetto agli altri
# pero piu lento in realta pero nell'evaluation fa 6 mosse e non 4 mmmh
#pathPPO =  '/home/matteo/ray_results/PPO_2023-11-10_14-32-44/PPO_rsp_a15d1_00000_0_2023-11-10_14-32-44/checkpoint_000000'
# 20 training iteration
pathPPO = '/home/matteo/ray_results/PPO_2023-11-13_15-29-22/PPO_rsp_09b75_00000_0_2023-11-13_15-29-22/checkpoint_000000'

############################################ PER VEDERLO GIOCARE #####################################
# Così va ma senza polisi sceglie random, ma va la logica della reward e dello stopping


# Algoritmi
#config = DQN().config
#config = ApexDQN().config
#config = Impala().config
#config = PG().config
config = PPO().config

# Mi risolve i problemi di mismatch con la rete, non so perche, ma per l'action mask
config['hiddens'] = []
config['dueling'] = False

# per l'evaluation
config['evaluation_interval'] = 1

algo = config.build()

#algo.restore(pathDQN)
#algo.restore(pathApexDQN)
#algo.restore(pathImpala)
#algo.restore(pathPG)
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