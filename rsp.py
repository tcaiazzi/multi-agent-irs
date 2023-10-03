import functools

import gymnasium
import numpy as np
from gymnasium.spaces import Discrete,Box,Dict

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

from prePost import doAction,reward

# DIFENSORE 
# difensore: 7 ATTACCHI (possibili in corso)-> NELL'OBSERVATION [0-1] FLOAT
# 14 ATTRIBUTI -> IN LOGICA, ANCHE PERCHE NON TUTTI STESSO TIPO ED IN OBSERVATION
# TERMINATION -> 7 ATTACHI PIÙ BASSI RISPETTO A QUALCOSA... 
# OGNI AZIONE MI MODIFICA LA LOGICA
# REWARD RISPETTO ALL'AZIONE

# Difensore:
#   mossa 0 spazio[0] False->True
#   mossa 1 spazio[0 e 1] False->True
#   mossa 2 spazio[0, 1 e 2] False->True
#ATTACCANTE:
#   mossa 0 spazio[0] True->False
#   mossa 1 spazio[0 e 1] True->False
# non ha mossa 2 per vedere se il difensore selezionando subito 2 vince
# partenza tutti True


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
        # mosse
        #self.MOVES = ['mossa1', 'mossa2','mossa3']

        # Questa è la truncation cosi esce per non girare all'infinito
        self.NUM_ITERS = 20

        # Mappa che in base all'azione eseguita mi da costo, impatto, ecc dell'azione

        self.possible_agents = ["attaccante","difensore"]

        # PER LA LOGICA
        """ self.spazio = {
            # quando tutti e 3 True invalicabili
            agent: [True,True,True]
            for agent in self.possible_agents
        } """
        self.spazio = {}
        self.spazio[self.possible_agents[0]] = [True,True]
        self.spazio[self.possible_agents[1]] = [True,True,True]
        print('Spazii:',self.spazio)

        # optional: a mapping between agent name and ID
        """ self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        ) """

        # optional: we can define the observation and action spaces here as attributes to be used in their corresponding methods
        # SOLITAMENTE ALGORITMI ACCETTANO TUTTI DISCRETE, 1 VAL 1 MOSSA
        self._action_spaces = {}
        self._action_spaces[self.possible_agents[0]] = Discrete(2)
        self._action_spaces[self.possible_agents[1]] = Discrete(3)
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
        self._observation_spaces[self.possible_agents[0]] = Box(low=0, high=1, shape=(2,), dtype=bool)
        self._observation_spaces[self.possible_agents[1]] = Box(low=0, high=1, shape=(3,), dtype=bool)
                    
        self.render_mode = render_mode

    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        return self._observation_spaces[agent]

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
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
        return np.stack(self.spazio[agent])
       

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass


    def reset(self, seed=None, options=None):
        
        # PER LA LOGICA
        """ self.spazio = {
            agente:[True,True,True]
            for agente in self.possible_agents
        } """
        self.spazio = {}
        self.spazio[self.possible_agents[0]] = [False,False]
        self.spazio[self.possible_agents[1]] = [True,True,True]
        
        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        #self.state = {agent: NONE for agent in self.agents}
        self.observations = {agent: 3 for agent in self.agents}
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
            self._was_dead_step(action)
            return
        
        agent = self.agent_selection
        print('Agente in azione:',agent)
        print('Mossa da eseguire:',action)

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0

        #################### REWARD ########################

        self.rewards[agent] = reward(agent,self.spazio,action)


        ######################## PRE/POST condizioni ############

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
        # termination funziona
        val = False
        if all(self.spazio[agent]):
            val = True
        self.terminations = {
            agent: val for agent in self.agents
        }

        
        self._cumulative_rewards[agent] = 0
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