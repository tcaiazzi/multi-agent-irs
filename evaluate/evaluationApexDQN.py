# se lancio dalla cartella principale
import sys
sys.path.append('./')

from  visualizzazione import visualizza_reward_mosse

from algoritmiTraining import ApexDQN

from ray.rllib.algorithms.algorithm import Algorithm



# sarebbe dovuto risultare piu veloce ma sul mio non sembra, se dqn riesco a spingermi liberamente a 20 training it.
# con apex ci mette dippiu, 30minuti per 10 trainin iteration e 100 partite(?)
# evaluation bassa
pathApexDQN = '/home/matteo/ray_results/APEX_2023-11-10_14-45-17/APEX_rsp_622c0_00000_0_2023-11-10_14-45-17/checkpoint_000000'

config = ApexDQN().config

# Mi risolve i problemi di mismatch con la rete, non so perche, ma per l'action mask
config['hiddens'] = []
config['dueling'] = False

# per l'evaluation
config['evaluation_interval'] = 1

algo = config.build()

algo.restore(pathApexDQN)

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
