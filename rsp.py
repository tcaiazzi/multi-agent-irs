import functools

import gymnasium
import numpy as np
from gymnasium.spaces import Discrete,Box,Dict

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

from prePost import doAction,reward,terminationPartita

# 7 attacchi (pscan,pvsftpd,psmbd,pphpcgi,pircd,pdistccd,prmi) hanno una probabilità con tui il difensore lo valuta
# 0 < T1 < T2 < 1 e p < T1 rumore, T1 < p < T2 possibile attacco (prevenzione), p > T2 attacco by IDS (contromisure),
# p=1 attacco noto e strategia da attuare
# 14 attributi influenzati dalle mie azioni
# 20ina contromisure
# tralascerei p e T

# ATTACCANTE 
# azioni : 7 (come gli attacchi)
# lo spazio monitora quello del difensore
# VINCE: per semplicità metto per ora che 1 mossa VINCE tutto

# DIFENSORE
# azioni : 14 (sono dippiù perche 1 azioni può modificare più variabili ma per ora facciamo 1 azione 1 variabile)
# 14 attributi -> observation (nel paper non tutti true/false per ora 14 bool)
# VINCE: quando spazio tutti TRUE

# OLD
#ATTACCANTE:
#   mossa 0 spazio[difensore][0] True->False
#   mossa 1 spazio[difensore][1] True->False
#   mossa 2 spazio[difensore][0,1,2 e 3] True->False
# Difensore:
#   mossa 0 spazio[difensore][0] False->True
#   mossa 1 spazio[difensore][1] False->True
#   mossa 2 spazio[difensore][2] False->True
#   mossa 3 spazio[difensore][0,1, 2 e 3] False->True 
# termna o difensore tutti true o tutti false
# partenza difensore mista


def env(render_mode=None):
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = raw_env(render_mode=internal_render_mode)
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

    def __init__(self, render_mode=None):

        # Questa è la truncation cosi esce per non girare all'infinito
        self.NUM_ITERS = 100

        # Mappa che in base all'azione eseguita mi da costo, impatto, ecc dell'azione

        self.possible_agents = ["attaccante","difensore"]

        # PER LA LOGICA
        """ self.spazio = {
            # quando tutti e 3 True invalicabili
            agent: [True,True,True]
            for agent in self.possible_agents
        } """
        self.spazio = {}
        self.spazio[self.possible_agents[0]] = [False]
        self.spazio[self.possible_agents[1]] = [True,False,True,False,
                                                True,False,True,False,
                                                True,False,True,False,
                                                True,False]
        print('Spazii:',self.spazio)

        # optional: a mapping between agent name and ID
        """ self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        ) """

        # optional: we can define the observation and action spaces here as attributes to be used in their corresponding methods
        # SOLITAMENTE ALGORITMI ACCETTANO TUTTI DISCRETE, 1 VAL 1 MOSSA
        self._action_spaces = {}
        self._action_spaces[self.possible_agents[0]] = Discrete(7)
        self._action_spaces[self.possible_agents[1]] = Discrete(14)
        #self._action_spaces = {agent: Discrete(3) for agent in self.possible_agents}

        # DEVE ESSERE DELLA STESSA STRUTTURA DEL RITORNO DI observe() 
        """ self._observation_spaces = {
            agent: Dict(
                {
                    "observation": Box(low=0, high=1, shape=(3,), dtype=bool),
                    "action_mask": Box(low=0, high=1, shape=(3,), dtype=np.int8),
                }
            ) 
            for agent in self.possible_agents
        } """
        self._observation_spaces = {}
        self._observation_spaces[self.possible_agents[0]] = Box(low=0, high=1, shape=(1,), dtype=bool)
        self._observation_spaces[self.possible_agents[1]] = Box(low=0, high=1, shape=(14,), dtype=bool)
                    
        self.render_mode = render_mode

    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        print('QUI')
        return self._observation_spaces[agent]

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        print('QUO')
        return self._action_spaces[agent]

    def render(self):
        print('')

    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        #return np.array(self.observations[agent])
        # return {"observation":self._observation_spaces[agent]["observation"].sample(),"action_mask":self._observation_spaces[agent]["action_mask"].sample()}
        legal_moves = []
        for i in range(len(self.spazio[agent])):
            if self.spazio[agent][i] == False:
                legal_moves.append(1)
            else:
                legal_moves.append(0)
        print('\t')
        print('Observe agent:',agent)
        print('Observe observation:',self.spazio[agent])
        #print('Observe legal_moves:',legal_moves)
        # in observation sto facendo tornare lo stato attuale ovvero spazio che uso per la mia logica interna,
        # dato che mi stabilisce sia reward e mossa
        # in action dove l'azione puo ancora agire, lo calcolo qui al volo
        """ return {
                    "observation":np.stack(self.spazio[agent]),
                    "action_mask":np.ndarray(shape=(len(legal_moves)),buffer=np.array(legal_moves),dtype=np.int8)
                } """
        # SIA ALL'ATTACCANTE CHE AL DIFENSORE STO FACENDO TORNARE LO STESSO SPAZIO COSÌ CHE
        # NE SIA PRESENTE UNO UNICO CONDIVISO E NON DUE REPLICATI
        return np.stack(self.spazio['difensore'])
       

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass


    def reset(self, seed=None, options=None):
        
        # PER LA LOGICA
        self.spazio = {}
        self.spazio[self.possible_agents[0]] = [False]
        self.spazio[self.possible_agents[1]] = [True,False,True,False,
                                                True,False,True,False,
                                                True,False,True,False,
                                                True,False]
    
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
        #self.state = {agent: NONE for agent in self.agents
        #self.observations = {agent: 3 for agent in self.agents}

        self.num_moves = 0
        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()




    def step(self, action):
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            print('Action dead:',action)
            print('Rewards dead:',self.rewards)
            self._was_dead_step(action)
            return
        
        agent = self.agent_selection
        print('Agente in azione:',agent)
        print('Mossa da eseguire:',action)

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0

        ############################################## REWARD ###########################################

        # SI INFLUENZANO LE REWARD A VICENDA
        rw = reward(agent,self.spazio,action)
        
        # VOLEVO FORZARE A FARLI SCEGLIERE SUBITO LE MOSSE MIGLIORI, PERCHÈ CON L'AUMENTARE DI MOSSE MENO REWARD
        if self.num_moves > 0:
            rw = int(rw/ (self.num_moves*2))
                 
        self.rewards[agent] = rw
        print('rw:',rw)
        
        # PER NON MANDARE LA REWARD TOTALE NEGATIVA
        if agent == 'attaccante':
            self.rewards[agent] = rw
            if self._cumulative_rewards['difensore'] >= rw:
                self.rewards['difensore'] = (-rw)
            else:
                self.rewards['difensore'] = (-self.rewards['difensore'])

        elif agent == 'difensore':
            self.rewards[agent] = rw
            if self._cumulative_rewards['attaccante'] >= rw:
                self.rewards['attaccante'] = (-rw)
            else:
                self.rewards['attaccante'] = (-self.rewards['attaccante'])         

        ######################## PRE/POST condizioni #####################################################

        print('Prima della mossa:',self.spazio)
        self.spazio = doAction(action,self.spazio,self.agent_selection)
        print('Dopo la mossa:',self.spazio)
        
        ############################# CHECK ARRESTO (se sono nello stato sicuro) #########################
        
        # NON POSSONO AVERE VALORI DISCORDI GLI AGENTI delle terminations e troncation
        # Dovrebbe arrestarlo 
        self.num_moves += 1
        self.truncations = {
            agent: self.num_moves >= self.NUM_ITERS for agent in self.agents
        }
        val = terminationPartita(False,self.spazio)
        self.terminations = {
            agent: val for agent in self.agents
        }

        ##################################################################################################
        # PERCHÈ L'AVEVANO MESSA?? SE LA METTO AD OGNI ROUND MI SI AZZERA
        #self._cumulative_rewards[agent] = 0
        print('Num Mosse:',self.num_moves)
        print('Truncation:',self.truncations)
        print('Termination:',self.terminations)
        print('Accumulative reward:',self._cumulative_rewards)

        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()

        if self.render_mode == "human":
            self.render()