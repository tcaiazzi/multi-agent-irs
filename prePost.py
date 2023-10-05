# qui per ogni partita mette numero di mosse fatte e le cumulative reward finali di quella partita
reward_mosse = {
    'attaccante':[],
    'difensore':[]
}

# qui mette tutte le reward di ogni partita, le cumulative reward, ovvero i contatori
curva_partita = {
    'attaccante': [],
    'difensore':[],
}

# APPLICA L'AZIONE ALLA SPOZIO 'LOGICA'
def doAction(action,spazio,agent):
    # mossa 0
    if agent == 'difensore':
        if 0 <= action <= 13:
            spazio['difensore'][action]=True
        """ elif action == 13:
            for i in range(14):
                spazio['difensore'][i]=True """
    
    elif agent == 'attaccante':
        if 1 <= action <=5:
            spazio['difensore'][action]=False
        # mossa 1
        elif action == 6 :
            for i in range(6,14):
                spazio['difensore'][i]=False
        elif action == 0 :
            for i in range(0,6):
                spazio['difensore'][i]=False

    return spazio


# APPLICA LA FUNZIONE DI REWARD IN BASE ALLA MOSSA PASSATA
def calcola(action,agent):
    # per la funzione di reward
    REWARD_MAP = {
        'attaccante':{
            0 : (10,10,10),
            1 : (1,1,1),
            2 : (1,1,1),
            3 : (1,1,1),
            4 : (1,1,1),
            5 : (1,1,1),
            6 : (10, 10, 10),
            },
        'difensore':{
            0 : (1,1,1),
            1 : (1,1,1),
            2 : (1,1,1),
            3 : (1,1,1),
            4 : (1,1,1),
            5 : (1,1,1),
            6 : (1,1,1),
            7 : (1,1,1),
            8 : (1,1,1),
            9 : (1,1,1),
            10 : (1,1,1),
            11 : (1,1,1),
            12 : (1,1,1),
            13 : (1,1,1),
            }
        }
    wt = 0.5
    wc = 0.5
    wi = 0.5
    tMax = 100
    cMax = 100
    #calcolo = -(-wt*(REWARD_MAP[agent][action][0]/tMax)-wc*(REWARD_MAP[agent][action][1]/cMax)-wi*(1))
    calcolo = REWARD_MAP[agent][action][0]+REWARD_MAP[agent][action][1]+REWARD_MAP[agent][action][2]
    return calcolo


# VERIFICA QUANDO CALCOLARE LA REWARD, NEGLI ALTRI CASI 0
def reward(agent,spazio,action):
    # LA REWARD LA OTTIENE AD OGNI MOSSA CHE PROVOCA EFFETTO DI VARIAZIONE DI STATO
    # HO MESSO LA REWARD QUANDO VINCE PERCHÈ CON DQN SCEGLIEVANO SEMPRE LE STESSE MOSSE MA IN REALTA CREDO 
    # CHE ABBIA BISOGNO SOLO DI PIÙ ADDESTRAMENTO PERCHÈ CON PG VA BENE
    reward = 0
    if agent == 'difensore':
        # IL DIFENSORE OTTIENE LA REWARD SOLO QUANDO È FALSE, OVVERO PUÒ ACCENDERE, QUINDI LA MOSSA HA EFFETTO
        if spazio[agent][action] == False:
            reward = calcola(action,agent)

    elif agent == 'attaccante':
        # L'AZIONE 6 MI SWITCHA GLI ELEMENTI DA 6 A 14 DA TRUE A FALSE
        if action == 6:
            app = []
            # VEDO CHE NON SIANO TUTTI FALSE ALTRIMENTI NIENTE RICOMPENSA
            for i in range(6,14):
                app.append(not(spazio['difensore'][i]))
            if not(all(app)):
                reward = calcola(action,agent)
        # L'AZIONE 0 MI SWITCHA GLI ELEMENTI DA 0 A 6 DA TRUE A FALSE
        if action == 0:
            app = []
            # VEDO CHE NON SIANO TUTTI FALSE ALTRIMENTI NIENTE RICOMPENSA
            for i in range(0,6):
                app.append(not(spazio['difensore'][i]))
            if not(all(app)):
                reward = calcola(action,agent)
        # PER QUALUNQUE ALTRA MOSSA DELL'ATTACCANTE MI CAMBIA SOLO 1 POSIZIONE
        elif spazio['difensore'][action] == True:
            reward = calcola(action,agent)
    
    print('Reward:',reward)
    return reward


# CONTROLLA LO STATE PER TERMINAR EO MENO
def terminationPartita(val,spazio):
    check = []
    if all(spazio['difensore']):
        val = True
    else:
        for i in range(len(spazio['difensore'])):
            check.append(not(spazio['difensore'][i]))
        if all(check):
            val = True
    return val

