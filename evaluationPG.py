from algoritmiTraining import DQN, ApexDQN,Impala,PG,PPO
from ray.rllib.algorithms.algorithm import Algorithm
from visualizzazione import visualizza_reward_mosse


# 50 training iteration: meno di 2000 partite con 1450 (? mosse), il training è meno fit di impala
# evaluation bene ma non benissimo, meglio impalaa, anche perchè con moto meno tempo
# Sembra instabile e lento a convergere e lento
#pathPG = '/home/matteo/ray_results/PG_2023-11-10_14-23-40/PG_rsp_5d2bd_00000_0_2023-11-10_14-23-40/checkpoint_000000'
# 20 training iteration
#pathPG = '/home/matteo/ray_results/PG_2023-11-13_15-27-23/PG_rsp_c341d_00000_0_2023-11-13_15-27-24/checkpoint_000000'
pathPG = '/home/matteo/ray_results/PG_2023-11-15_09-14-41/PG_rsp_06f46_00000_0_2023-11-15_09-14-41/checkpoint_000000'
############################################ PER VEDERLO GIOCARE #####################################
# Così va ma senza polisi sceglie random, ma va la logica della reward e dello stopping


# Algoritmi
config = PG().config

# Mi risolve i problemi di mismatch con la rete, non so perche, ma per l'action mask
config['hiddens'] = []
config['dueling'] = False

# per l'evaluation
config['evaluation_interval'] = 1

algo = config.build()

algo.restore(pathPG)

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
