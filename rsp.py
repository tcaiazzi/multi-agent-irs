import functools

import gymnasium
import numpy as np
from gymnasium.spaces import Discrete,Box,Dict

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers



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
        
        self.MOVES = ['mossa1', 'mossa2','mossa3']
        # Questa è la truncation cosi esce per non girare all'infinito
        self.NUM_ITERS = 20
        # Mappa che in base all'azione eseguita mi da costo, impatto, ecc dell'azione
        self.REWARD_MAP = {
            'mossa1': (1, 0, 0),
            'mossa2': (2, 0, 0),
            'mossa3': (3, 0, 0)
        }
        # per la funzione di reward
        self.wt = 0.5
        self.wc = 0.5
        self.wi = 0.5
        self.tMax = 100
        self.cMax = 100

        self.possible_agents = ["attaccante","difensore"]
        # Per la logica
        self.spazio = {
            # quando tutti e 3 True invalicabili
            agent: [False,False,False]
            for agent in self.possible_agents
        }
        print('Spazii:',self.spazio)

        # optional: a mapping between agent name and ID
        """ self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        ) """

        # optional: we can define the observation and action spaces here as attributes to be used in their corresponding methods
        self._action_spaces = {agent: Discrete(3) for agent in self.possible_agents}
        self._observation_spaces = {
            agent: Discrete(10) for agent in self.possible_agents
            #agent: Dict(
                #{
                    #"observation": Box(low=0, high=1, shape=(4,), dtype=np.int8),
                    #"action_mask": Box(low=0, high=1, shape=(3,), dtype=np.int8),
                #}
            #) 
            for agent in self.possible_agents
        }
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
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        """
        if self.render_mode is None:
            gymnasium.logger.warn(
                "You are calling render method without specifying any render mode."
            )
            return

        """ if len(self.agents) == 2:
            string = "Current state: Agent1: {} , Agent2: {}".format(
                MOVES[self.state[self.agents[0]]], MOVES[self.state[self.agents[1]]]
            )
        else:
            string = "Game over" """
        print('\t')

    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return np.array(self.observations[agent])

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass

    def reset(self, seed=None, options=None):
        
        # Perla logica
        self.spazio = {
            agente:[False,False,False]
            for agente in self.possible_agents
        }
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
        if self.spazio[agent][action] == False:
            reward = self.REWARD_MAP[self.MOVES[action]]
            valReward = -(-self.wt*(reward[0]/self.tMax)-self.wc*(reward[1]/self.cMax)-self.wi*(1))
            #rewardInv = -valReward
            print('Reward:',valReward)
            if self.agent_selection == 'attaccante':
                self.rewards[self.agents[0]], self.rewards[self.agents[1]] = (valReward,0)
            else:
                self.rewards[self.agents[0]], self.rewards[self.agents[1]] = (0,valReward)
        else:
            print('Reward:',0)
            if self.agent_selection == 'attaccante':
                self.rewards[self.agents[0]], self.rewards[self.agents[1]] = (0,0)
            else:
                self.rewards[self.agents[0]], self.rewards[self.agents[1]] = (0,0)

        ######################## PRE/POST condizioni ############
        print('Prima della mossa:',self.spazio)
        # mossa 0
        if action == 0:
            self.spazio[self.agent_selection][action]=True
        # mossa 1
        elif action == 1:
            self.spazio[self.agent_selection][0]=True
            self.spazio[self.agent_selection][action]=True
        # mossa 2
        elif action == 2:
            self.spazio[self.agent_selection][0]=True
            self.spazio[self.agent_selection][1]=True
            self.spazio[self.agent_selection][action]=True
        print('Dopo la mossa:',self.spazio)
        
        # Dovrebbe arrestarlo 
        self.num_moves += 1
        self.truncations = {
            agent: self.num_moves >= self.NUM_ITERS for agent in self.agents
        }

        # NON POSSONO AVERE SEGNI DISCORDI 
        val = False
        for a in agent:
            if all(self.spazio[agent]):
                val = True
                break
        self.terminations = {
            agent: val for agent in self.agents
        }

        
        self._cumulative_rewards[agent] = 0
        print('Num Mosse:',self.num_moves)
        print('Truncation:',self.truncations)
        print('Termination:',self.terminations)


        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()

        if self.render_mode == "human":
            self.render()