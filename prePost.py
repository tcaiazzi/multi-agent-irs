def doAction(action,spazio,agent):
    # mossa 0
    if agent == 'difensore':
        if action == 0:
            spazio['difensore'][action]=True
        # mossa 1
        elif action == 1:
            spazio['difensore'][0]=True
            spazio['difensore'][action]=True
        # mossa 2
        elif action == 2:
            spazio['difensore'][0]=True
            spazio['difensore'][1]=True
            spazio['difensore'][action]=True
    elif agent == 'attaccante':
        if action == 0:
            spazio['difensore'][action]=False
        # mossa 1
        elif action == 1:
            spazio['difensore'][0]=False
            spazio['difensore'][action]=False
        # mossa 2
        """ elif action == 2:
            spazio['difensore'][0]=False
            spazio['difensore'][1]=False
            spazio['difensore'][action]=False """
    return spazio

def calcola(action):
    # per la funzione di reward
    REWARD_MAP = {
            0 : (1, 1, 1),
            1 : (15, 15, 15),
            2 : (30, 30, 30)
        }
    wt = 0.5
    wc = 0.5
    wi = 0.5
    tMax = 100
    cMax = 100
    calcolo = -(-wt*(REWARD_MAP[action][0]/tMax)-wc*(REWARD_MAP[action][1]/cMax)-wi*(1))
    return calcolo

def reward(agent,spazio,action):
    reward = 0
    if agent == 'difensore':
        if spazio[agent][action] == False:
            reward = calcola(action)
    elif agent == 'attaccante':
        if spazio['difensore'][action] == True:
            reward = calcola(action)
    print('Reward:',reward)
    return reward