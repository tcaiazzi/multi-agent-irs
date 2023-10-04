# APPLICA L'AZIONE ALLA SPOZIO 'LOGICA'
def doAction(action,spazio,agent):
    # mossa 0
    if agent == 'difensore':
        if action == 0:
            spazio['difensore'][action]=True
        # mossa 1
        elif action == 1:
            spazio['difensore'][action]=True
        # mossa 2
        elif action == 2:
            spazio['difensore'][action]=True
        elif action == 3:
            spazio['difensore'][0]=True
            spazio['difensore'][1]=True
            spazio['difensore'][2]=True
            spazio['difensore'][action]=True
    elif agent == 'attaccante':
        if action == 0:
            spazio['difensore'][action]=False
        # mossa 1
        elif action == 1:
            spazio['difensore'][action]=False
        # mossa 2
        elif action == 2:
            spazio['difensore'][0]=False
            spazio['difensore'][1]=False
            spazio['difensore'][action]=False
            spazio['difensore'][3]=False
    return spazio


# APPLICA LA FUNZIONE DI REWARD IN BASE ALLA MOSSA PASSATA
def calcola(action,agent):
    # per la funzione di reward
    REWARD_MAP = {
        'attaccante':{
            0 : (1, 1, 1),
            1 : (1, 1, 1),
            2 : (20, 20, 20),
            },
        'difensore':{
            0 : (1, 1, 1),
            1 : (1, 1, 1),
            2 : (1, 1, 1),
            3 : (20, 20, 20)
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
        if spazio['difensore'][action] == True:
            reward = calcola(action,agent)
    # LA  REWARD LA OTTIENE QUANDO VINCE
    """ if action == 2 and agent == 'attaccante':
        reward = calcola(action)
    elif action ==3 and agent == 'difensore':
        reward = calcola(action) """
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