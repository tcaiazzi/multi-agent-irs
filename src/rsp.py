import functools
import json
import os
import sys
import time

import numpy as np
from gymnasium.spaces import Box, Dict, Discrete
from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

from prePost import (generazioneSpazioRandom, postCondizioni,
                     preCondizioni, reset, reward, reward_mosse,
                     terminationPartita)


# ------------------------------------- Lettura conf ---------------------------------#
def parse_configruartion():
    conf = open("conf.txt", "r")
    lines = conf.readlines()
    conf.close()

    print(lines)
    for i in range(len(lines)):
        p = lines[i].strip().split('= ')
        print(int(p[1]))
        lines[i] = int(p[1])

    configuration = {
        'num_agents': int(lines[0]),
        'num_att_actions': int(lines[1]),
        'k_att': int(lines[2]) / 10,
        'num_def_actions': int(lines[3]),
        'k_def': int(lines[4]) / 10
    }

    configuration['num_sync_att_actions'] = int((configuration['num_att_actions'] * configuration['k_att']))
    configuration['num_async_att_actions'] = configuration['num_att_actions'] - configuration['num_sync_att_actions']

    configuration['num_sync_def_actions'] = int((configuration['num_def_actions'] * configuration['k_def']))
    configuration['num_async_def_actions'] = configuration['num_def_actions'] - configuration['num_sync_def_actions']

    # # dimensione dello stato, tutte variabili booleane + timer
    # dim_obs = 0
    # # azioni attaccante e dfensore uguali, + noop (ma in numero sincrone ed asincrone puo variare)
    # n_azioni = 0
    # # posizione del timer nello spazio
    # timer = 0
    if ((configuration['num_att_actions']) == (configuration['num_def_actions']) and (10 >= configuration['k_att'] >= 0)
            and (10 >= configuration['k_def'] >= 0)):
        # ogni azione una var dello stato + timer
        configuration['dim_obs'] = configuration['num_def_actions'] + 1
        # mosse totali somma asincrone e sincrone + noop + wait
        configuration['n_actions'] = configuration['num_def_actions'] + 2
        # set timer
        configuration['timer'] = configuration['dim_obs'] - 1

    else:
        # esce se in numero tot le mosse dell'attaccante e del difensore non sono uguali
        sys.exit('la somma delle azioni sincrone ed asincrone di ciascun agente deve essere la stessa')

    configuration['moves'] = {
        'attacker': {
            'sync': configuration['num_sync_att_actions'],
            'async': configuration['num_async_att_actions'],
        },
        'defender': {
            'sync': configuration['num_sync_def_actions'],
            'async': configuration['num_async_def_actions'],
        }
    }
    configuration['legal_moves'] = np.zeros(configuration['n_actions'], 'int8')
    start = 0

    return configuration


# -------------------------------------- Lettura conf ----------------------------------#

def env(algorithm, type_of_test, render_mode=None):
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    configuration = parse_configruartion()
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = raw_env(algorithm, configuration, type_of_test, render_mode=internal_render_mode)
    # This wrapper is only for environments which print results to the terminal
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    # this wrapper helps error handling for discrete action spaces
    env = wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv):
    """
    The metadata holds environment constants. From gymnasium, we inherit the "render_modes",
    metadata which specifies which modes can be put into the render() method.
    At least human mode should be supported.
    The "name" metadata allows the environment to be pretty printed.
    """
    metadata = {"render_modes": ["human"], "name": "rps_v2"}

    def __init__(self, algorithm, configuration, type_of_test, render_mode=None):
        super().__init__()
        self.configuration = configuration
        self.start = time.time()
        self.algorithm = algorithm
        self.type_of_test = type_of_test

        # Questa è la truncation cosi esce per non girare all'infinito
        self.NUM_ITERS = 2000
        self.lastTimer = 0
        # Lo utilizzo affinche termini quando entrambi i due agenti, in maniera conseutiva hanno a disposizione
        # solo mosse noop selezionabili:
        # nmosse è il numero di mossa della partita in cui hanno solo noop
        # in mosse salvo l'actionmask per la verifica
        # nmosse lo uso per la sequenzialità dei noop-noop

        # self.possible_agents = [f'agente{i}' for i in range(n_agenti)]
        self.possible_agents = ['defender', 'attacker']

        self.lm = {
            i: {
                'nmosse': -1,
                'mosse': []
            } for i in self.possible_agents
        }

        # spazio del difensore monitorato anche dall'attaccante per l'observation dopo un'action
        self.spazio = {
            i: generazioneSpazioRandom(self.configuration['dim_obs'])
            for i in self.possible_agents
        }

        # STATO
        # [per ogni var 1 attacco diff e att,...,timer]

        print('Spazio:', self.spazio)

        # optional: we can define the observation and action spaces here as attributes to be used in their corresponding methods
        # SOLITAMENTE ALGORITMI ACCETTANO TUTTI DISCRETE, 1 VAL 1 MOSSA
        self._action_spaces = {}

        """ self._action_spaces = {
                Discrete(n_azioni_) for i in self.possible_agents
            } """

        # ATTACCANTE: attacchi=[nSinc + mAsinc]
        self._action_spaces[self.possible_agents[0]] = Discrete(self.configuration['n_actions'])

        # DIFENSORE:  azioni= [xSinc + yAsinc]
        self._action_spaces[self.possible_agents[1]] = Discrete(self.configuration['n_actions'])

        # DEVE ESSERE DELLA STESSA STRUTTURA DEL RITORNO DI observe() 
        self._observation_spaces = {}
        # lo spazio dell'attaccante per ora non viene utilizzato
        # Me ne basta uno solo

        # [n+mVar + timer]

        self._observation_spaces = {
            i: Dict(
                {
                    "observations": Box(low=-1000, high=1000, shape=(self.configuration['dim_obs'],), dtype=float),
                    "action_mask": Box(low=0, high=1, shape=(self.configuration['n_actions'],), dtype=np.int8),
                }
            ) for i in self.possible_agents
        }

        self.render_mode = render_mode

    # SE NON ERRO OBS_SPACE E ACT_SPACE VENGONO UTILIZZATI ALL'INIZIO PER FAR SI CHE LA DEFINIZIONE DI TUTTO QUADRI
    # PERCHÈ REALMENTE NEL CODICE NON VENGONO UTILIZZATI, OBBLIGATORI MA NON UTILIZZATI
    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        print('Observation Space', self._observation_spaces[agent])
        return self._observation_spaces[agent]

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        print("Action Space", self._action_spaces[agent])
        return self._action_spaces[agent]

    def render(self):
        print('')

    # INVECE MOLTO IMPORTANTE OBSERVE CHE FA TORNRE L'OSSERVAZIONE IN BASE ALLA MOSSA
    # IN FATTI STO USANDO LA VARIABILE SPAZIO CHE ERA SATATA PROGETTATA PER LA MIA LOGICA INTERNA, IL COMPORTAMENTO
    def observe(self, agent):
        # PRE CONDIZIONI

        legal_moves = np.zeros(self.configuration['n_actions'], 'int8')

        preCondizioni(agent, self.spazio, legal_moves, self.configuration['moves'], self.configuration['timer'])
        self.lm[agent]['mosse'] = np.copy(legal_moves)

        print('\t')
        print('Observe agent:', agent)
        print('Observe observation:', self.spazio['defender'])
        print('Observe action mask/legal moves:', legal_moves)

        # in observation sto facendo tornare lo stato attuale ovvero spazio che uso per la mia logica interna,
        # dato che mi stabilisce sia reward e mossa
        # SIA ALL'ATTACCANTE CHE AL DIFENSORE STO FACENDO TORNARE LO STESSO SPAZIO COSÌ CHE
        # NE SIA PRESENTE UNO UNICO CONDIVISO E NON DUE REPLICATI
        # return np.stack(self.spazio['defender'])
        # HO AGGIUNTO L'ACTION MASK PER IMPEDIRE LA SCELTA DI ALCUNE MOSSE PRECONDIZIONI
        return {
            'observations': np.stack(self.spazio['defender']),
            'action_mask': np.stack(legal_moves),
        }

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass

    def reset(self, seed=None, options=None):
        # prePost Reset per attaccante e difensore
        reset()
        self.lastTimer = 0

        self.lm = {
            i: {
                'nmosse': -1,
                'mosse': []
            } for i in self.possible_agents
        }

        # spazio del difensore monitorato anche dall'attaccante per l'observation dopo un'action
        self.spazio = {
            i: generazioneSpazioRandom(self.configuration['dim_obs'])
            for i in self.possible_agents
        }

        self.agents = self.possible_agents[:]

        # CI SONO LE REWARD DI ENTRAMBI GLI AGENTI CHE VENGONO AGGIUNTE ALLE CUMULATIVE OGNI VOLTA CHE UNO DEI DUE 
        # FA UN'AZIONE: ATTACANTE AGISCE, GENERE 2 REWARD (ATT,DIFF) E LE METTE ALLE ACCUMULATIVE, TEMPORANEE
        self.rewards = {agent: 0 for agent in self.agents}

        # CI SONO TUTTE LE REWARD DI OGNI STEP, OVVERO DI OGNI VOLTA CHE UN AGENTE FA UN'AZIONE
        # DUE UNA PARTITA FINCHE NON ESCE UN VINCITORE
        self._cumulative_rewards = {agent: 0 for agent in self.agents}

        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}

        # ANCORA MAI USATO 
        self.infos = {agent: {} for agent in self.agents}

        # SE SERVE POTREI SALVARCI GLI STATI INTERMEDI DEL DIFF
        # self.state = {agent: NONE for agent in self.agents
        # self.observations = {agent: 3 for agent in self.agents}

        self.num_moves = 0
        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

    def step(self, action):
        if (
                self.terminations[self.agent_selection]
                # or self.truncations[self.agent_selection]
        ):
            self.end = time.time()
            print('START:', self.start)
            print('END:', self.end)
            print(self.end - self.start)
            # DI OGNI PARTITA SALVO LE REWARD OTTENUTE TOTALI E IL NUMERO DI MOSSE ASSOCIATE
            reward_mosse[self.agent_selection].append(
                (self.num_moves, self._cumulative_rewards[self.agent_selection], int((self.end - self.start))))

            # SALVOLE INFO NEI FILE
            # apro in write perche butto dentro la struttura dati in prePost
            # che mi tiene tutto ed alla fine ho i dati di

            results_path = os.path.join(os.path.dirname(__file__), "..", "results", self.type_of_test)
            os.makedirs(results_path, exist_ok=True)
            file_uno = open(os.path.join(results_path, f"{self.algorithm}.json"), "w")
            # file_due = open("/home/matteo/Documenti/GitHub/tesiMagistrale/fileGrafici/curva_partita.txt", "w")
            file_uno.write(json.dumps(reward_mosse))
            # file_due.write(json.dumps(curva_partita))
            file_uno.close()
            # file_due.close()

            print('Action dead:', action)
            print('Rewards dead:', self._cumulative_rewards)
            self._was_dead_step(action)
            return

        agent = self.agent_selection
        # print('Agente in azione:',agent)
        print('Mossa da eseguire:', action)
        print('Timer Prima:', self.spazio['defender'][self.configuration['timer']])

        ############################################## REWARD ###########################################

        # SI INFLUENZANO LE REWARD A VICENDA
        """ print('Mossa valida:',mossaValida)
        if mossaValida: """
        rw = reward(agent, action, self.spazio['defender'], self.configuration['n_actions'],
                    self.configuration['num_sync_att_actions'],
                    self.configuration['num_sync_def_actions'], self.configuration['timer'])
        # if agent == 'defender':
        self.rewards[agent] += rw

        ######################## PRE(con action mask solo post)/POST condizioni #####################################################

        # print('Prima della mossa:',self.spazio)
        self.lastTimer = postCondizioni(action, self.spazio, self.agent_selection, self.configuration['moves'],
                                        self.configuration['timer'], self.lastTimer)
        self.spazio['defender'][self.configuration['timer']] = round(
            self.spazio['defender'][self.configuration['timer']], 3)
        print('Dopo la mossa:', self.spazio['defender'])

        ############################# CHECK ARRESTO (se sono nello stato sicuro) #########################

        # COSA STO FACENDO
        # NOOP-NOOP MI TERMINA
        # MASOLO NEL CASO FOSSERO LE ULTIME DUE MOSSE RIMASTE
        # VOGLIO VEDERE SE MIGLIORA IL TRAINING
        # aggiungo la sequenialità delle noop-noop mel'ero dimenticataa

        """ if agent == 'attacker':
            # solo noop puo fare se true
            att = [not(i) for i in self.lm['attacker']['mosse']]
            #print('att:',att)
            if all(att[:n_azioni-2]):
                #print('ENTRATOatt')
                self.lm[agent]['nmosse'] = self.num_moves
        else:
            # solo noop puo fare se true
            diff = [not(i) for i in self.lm['defender']['mosse']]
            #print('diff:',diff)
            if all(diff[:n_azioni-2]):
                #print('ENTRATOdiff')
                self.lm[agent]['nmosse'] = self.num_moves """

        # NON POSSONO AVERE VALORI DISCORDI GLI AGENTI delle terminations e troncation
        mAtt = (self.configuration['num_sync_att_actions'] + self.configuration['num_async_att_actions'])
        mDiff = (self.configuration['num_sync_def_actions'] + self.configuration['num_async_def_actions'])
        val = terminationPartita(self.spazio, self.configuration['legal_moves'], self.num_moves, self.NUM_ITERS, mAtt,
                                 mDiff)
        # se la condizione di aresto generale lo ferma bene altrimenti...
        self.terminations = {
            agent: val for agent in self.agents
        }

        ##################################################################################################

        # SALVE TUTTE LE REWARD CUMULATIVE DI TUTTE LE PARTITE
        # curva_partita['attacker'].append((self.num_moves,self._cumulative_rewards['attacker']))
        # curva_partita['defender'].append((self.num_moves,self._cumulative_rewards['defender']))

        self._accumulate_rewards()

        print('Timer Dopo:', self.spazio['defender'][self.configuration['timer']])
        print('Num Mosse:', self.num_moves)
        print('Truncation:', self.truncations)
        print('Termination:', self.terminations)
        print('Rewards:', self.rewards)

        self._cumulative_rewards[agent] = round(self._cumulative_rewards[agent], 2)
        print('reward cumulative:', self._cumulative_rewards)

        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        self.num_moves += 1
        self.rewards[agent] = 0

        if self.render_mode == "human":
            self.render()
