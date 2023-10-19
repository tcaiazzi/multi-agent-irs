import functools
import json
import numpy as np

from gymnasium.spaces import Discrete,Box,Dict

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

from prePost import doAction,reward,terminationPartita,reward_mosse,curva_partita


# 7 attacchi (pscan,pvsftpd,psmbd,pphpcgi,pircd,pdistccd,prmi) hanno una probabilità con tui il difensore lo valuta
# 0 < T1 < T2 < 1 e p < T1 rumore, T1 < p < T2 possibile attacco (prevenzione), p > T2 attacco by IDS (contromisure),
# p=1 attacco noto e strategia da attuare
# 14 attributi influenzati dalle mie azioni
# 20ina contromisure
# tralascerei p e T

# ATTACCANTE 
# azioni : 3 (come gli attacchi).. IMPEGANTIVO OGNI VOLTA STARE A CODIFICARE UNO SCENARIO
# lo spazio monitora quello del difensore
# VINCE: per semplicità metto per ora che 2 mossE PER FARE BINGO (0 e 2: 0 da 0 a 6 e 6 da 6 a 14)

# DIFENSORE
# azioni : 14 (sono dippiù perche 1 azioni può modificare più variabili ma per ora facciamo 1 azione 1 variabile)
# 14 attributi -> observation (nel paper non tutti true/false per ora 14 bool)
# VINCE: quando spazio TUTTI TRUE, ma credo che punti a non morire mai

# L'OTTIMO PER IL DIFENSORE E FAR SALIRE SEMPRE LA REWARD PERCHE NON MUORE E RIESCE SEMPRE A DIFENDERSI
# L'ATTACCANTE DEVE TROVARE SUBITO LA COMBO VINCENTE (2 MOSSE)

# E LE SUE REWARD DIMINUISCONO COL TEMPO, PERCHÈ SE IL DIFENSORE NEL CASO OTTIMO IN AL PIÙ 13 MOSSE VINCEREBBE
# PERCHE TUTTI FALSE UN SOLO TRUE, L'ATTACCANTE SCEGLIE SEMPRE LA MOSSA DOVE HA GIA FALSE, E AD OGNI SUO TURNO
# SCEGLIE UNA MOSSA BUONA CHE GLI CAMBIA UNA VARIABILE, 
# CREDO CHE PERDA SEMPRE PER QUESTO MOTIVO, OTTIENE PIU REWARD SE RESISTE PIUTTOSTO CHE VINCERE)



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
        # per ora non lo sto usando lo spazio dell'attaccante
        #self.spazio[self.possible_agents[0]] = [False]
        # Mi serve solo per rimuovere un wrap per usare il dizionario per l'action mask MA NON LO STO USANDO
        self.spazio[self.possible_agents[1]] = [True,False,True,False,
                                                True,False,True,False,
                                                True,False,True,False,
                                                True,False]
        # spazio del difensore monitorato anche dall'attaccante per l'observation dopo un'action
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
        self._action_spaces[self.possible_agents[0]] = Discrete(3)
        self._action_spaces[self.possible_agents[1]] = Discrete(14)
        #self._action_spaces = {agent: Discrete(3) for agent in self.possible_agents}

        # DEVE ESSERE DELLA STESSA STRUTTURA DEL RITORNO DI observe() 
        self._observation_spaces = {}
        # lo spazio dell'attaccante per ora non viene utilizzato
        # Me ne basta uno solo
        self._observation_spaces[self.possible_agents[0]] = Dict(
                {
                    "observations": Box(low=0, high=1, shape=(14,), dtype=bool),
                    "action_mask": Box(low=0, high=1, shape=(14,), dtype=np.int8),
                }
            )
        # per entrambi usiamo solo quello del difensore
        self._observation_spaces[self.possible_agents[1]] = Dict(
                {
                    "observations": Box(low=0, high=1, shape=(14,), dtype=bool),
                    "action_mask": Box(low=0, high=1, shape=(14,), dtype=np.int8),
                }
            )
                    
        self.render_mode = render_mode


# SE NON ERRO OBS_SPACE E ACT_SPACE VENGONO UTILIZZATI ALL'INIZIO PER FAR SI CHE LA DEFINIZIONE DI TUTTO QUADRI
# PERCHÈ REALMENTE NEL CODICE NON VENGONO UTILIZZATI, OBBLIGATORI MA NON UTILIZZATI
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

# INVECE MOLTO IMPORTANTE OBSERVE CHE FA TORNRE L'OSSERVAZIONE IN BASE ALLA MOSSA
# IN FATTI STO USANDO LA VARIABILE SPAZIO CHE ERA SATATA PROGETTATA PER LA MIA LOGICA INTERNA, IL COMPORTAMENTO
    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        # SERVE A FAR SI CHE IN UNO STATO ALCUNE AZIONI NON SIANO SELEZIONABILI
        legal_moves = np.zeros(14,'int8')

        if agent == 'difensore':
            for i in range(len(self.spazio['difensore'])):
                if self.spazio['difensore'][i] == False:
                        legal_moves[i]=1
                else:
                        legal_moves[i]=0
        else:
            # mossa 0 nel caso anche solo uno dei primi 6 TRUE
            for i in self.spazio['difensore'][:7]:
                if i:
                    legal_moves[0] = 1
            # mossa 2 nel caso anche solo uno dei secondi 6 TRUE
            for i in self.spazio['difensore'][7:]:
                if i :
                    legal_moves[2] = 1
            # qualcosa fa
            if self.spazio['difensore'][7]:
                legal_moves[1] = 1




        print('\t')
        print('Observe agent:',agent)
        print('Observe observation:',self.spazio['difensore'])
        print('Observe action mask/legal moves:',legal_moves)

        # in observation sto facendo tornare lo stato attuale ovvero spazio che uso per la mia logica interna,
        # dato che mi stabilisce sia reward e mossa
        # SIA ALL'ATTACCANTE CHE AL DIFENSORE STO FACENDO TORNARE LO STESSO SPAZIO COSÌ CHE
        # NE SIA PRESENTE UNO UNICO CONDIVISO E NON DUE REPLICATI
        #return np.stack(self.spazio['difensore'])
        # HO AGGIUNTO L'ACTION MASK PER IMPEDIRE LA SCELTA DI ALCUNE MOSSE PRECONDIZIONI
        return {
                'observations':np.stack(self.spazio['difensore']),
                'action_mask':np.stack(legal_moves),
                }
       

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
        self.spazio[self.possible_agents[0]] = [True,False,True,False,
                                                True,False,True,False,
                                                True,False,True,False,
                                                True,False]
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
            #or self.truncations[self.agent_selection]
        ):
            # DI OGNI PARTITA SALVO LE REWARD OTTENUTE TOTALI E IL NUMERO DI MOSSE ASSOCIATE
            reward_mosse[self.agent_selection].append((self.num_moves,self._cumulative_rewards[self.agent_selection]))
            
            # SALVOLE INFO NEI FILE
            #visualizza()
            file_uno = open("/home/matteo/Documenti/GitHub/tesiMagistrale/reward_mosse.txt", "w")
            file_due = open("/home/matteo/Documenti/GitHub/tesiMagistrale/curva_partita.txt", "w")
            file_uno.write(json.dumps(reward_mosse))
            file_due.write(json.dumps(curva_partita))
            file_uno.close()
            file_due.close()
            
            print('Action dead:',action)
            print('Rewards dead:',self._cumulative_rewards)
            self._was_dead_step(action)
            return
        
        
        agent = self.agent_selection
        #print('Agente in azione:',agent)
        print('Mossa da eseguire:',action)

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0

        ######################## PRE(con action mask solo post)/POST condizioni #####################################################

        #print('Prima della mossa:',self.spazio)
        mossaValida = doAction(action,self.spazio,self.agent_selection)
        print('Dopo la mossa:',self.spazio['difensore'])

        ############################################## REWARD ###########################################

        # SI INFLUENZANO LE REWARD A VICENDA
        print('Mossa valida:',mossaValida)
        if mossaValida:
            rw = reward(agent,self.spazio,action)
            self.rewards[agent] = rw
        
        # VOLEVO FORZARE A FARLI SCEGLIERE SUBITO LE MOSSE MIGLIORI, PERCHÈ CON L'AUMENTARE DI MOSSE MENO REWARD
        # PERÒ SOLO PER L'ATTCCANTE, PERCHÈ DEVE SBRIGARSI PRIMA CHE IL DIFENSORE LE BLOCCHI TUTTE
        # PER IL DIFENSORE DATO CHE NON HA UNA SUPER MOSSA BASTA CHE NEL TEMPO NON PRENDA MOSSE INEFFICIENTI
        """ if agent == 'attaccante':
            if self.num_moves > 0:
                # Reward attaccante dipendente dal tempo
                #rw = rw/ (self.num_moves)
                rw = rw
        else:
            rw = rw """
                 
        
        #print('rw:',rw)
        
        # PER NON MANDARE LA REWARD TOTALE NEGATIVA
        """ if agent == 'attaccante':
            self.rewards[agent] = rw
            # Mi influenza la reward dell'avversario
            if self._cumulative_rewards['difensore'] >= rw:
                self.rewards['difensore'] = (-rw)
            else:
                self.rewards['difensore'] = (-self.rewards['difensore'])
           
        elif agent == 'difensore':
            self.rewards[agent] = rw
            # Mi influenza la reward dell'avversario
            if self._cumulative_rewards['attaccante'] >= rw:
                self.rewards['attaccante'] = (-rw)
            else:
                self.rewards['attaccante'] = (-self.rewards['attaccante'])         
        """ 
        
        ############################# CHECK ARRESTO (se sono nello stato sicuro) #########################
        
        # NON POSSONO AVERE VALORI DISCORDI GLI AGENTI delle terminations e troncation
        # Dovrebbe arrestarlo 
        self.num_moves += 1
        """ self.truncations = {
            agent: self.num_moves >= self.NUM_ITERS for agent in self.agents
        } """
        val = terminationPartita(False,self.spazio)
        self.terminations = {
            agent: val for agent in self.agents
        }

        ##################################################################################################
       
        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        # PER FORZA QUI PERCHÈ LE REWARDS SI AZZERA OGNI VOLTA CHE SCAMBIA IL GIOCATORE
        # ANNULLARE LE REWARD NEL CASO FINISCANO PARI
        """ if self.num_moves < 100:
            self._accumulate_rewards()
        else:
            self.rewards['attaccante'] = -self._cumulative_rewards['attaccante']
            self.rewards['difensore'] = -self._cumulative_rewards['difensore'] """
        
        # SALVE TUTTE LE REWARD CUMULATIVE DI TUTTE LE PARTITE
        curva_partita['attaccante'].append((self.num_moves,self._cumulative_rewards['attaccante']))
        curva_partita['difensore'].append((self.num_moves,self._cumulative_rewards['difensore']))


        self._accumulate_rewards()

        # PERCHÈ L'AVEVANO MESSA?? SE LA METTO AD OGNI ROUND MI SI AZZERA
        #self._cumulative_rewards[agent] = 0
        print('Num Mosse:',self.num_moves)
        print('Truncation:',self.truncations)
        print('Termination:',self.terminations)
        print('reward cumulative:',self._cumulative_rewards)
        
        if self.render_mode == "human":
            self.render()
