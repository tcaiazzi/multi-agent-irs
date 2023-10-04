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
            0 : (100,100,100),
            1 : (1,1,1),
            2 : (1,1,1),
            3 : (1,1,1),
            4 : (1,1,1),
            5 : (1,1,1),
            6 : (100, 100, 100),
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
        if spazio[agent][action] == False:
            reward = calcola(action,agent)

    elif agent == 'attaccante':
        if action == 6:
            reward = calcola(action,agent)
        elif spazio['difensore'][action] == True:
            reward = calcola(action,agent)
    # LA  REWARD LA OTTIENE QUANDO VINCE
    """ if action == 2 and agent == 'attaccante':
        reward = calcola(action,agent)
    elif action ==3 and agent == 'difensore':
        reward = calcola(action,agent) """
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