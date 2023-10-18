from matplotlib import pyplot as plt
import numpy as np

# qui per ogni partita mette numero di mosse fatte e le cumulative reward finali di quella partita
reward_mosse = {
    "attaccante":[],
    "difensore":[]
}

# qui mette tutte le reward di ogni partita, le cumulative reward, ovvero i contatori
curva_partita = {
    "attaccante": [],
    "difensore":[],
}





# APPLICA L'AZIONE ALLA SPAZIO 'LOGICA'
def doAction(action,spazio,agent):
    # mossa 0
    mossaValida = False
    if agent == 'difensore':
        # una mossa una variabile
        if 0 <= action <= 13:
            if spazio['difensore'][action] == False:
                spazio['difensore'][action]=True
                mossaValida = True
    
    elif agent == 'attaccante':
        # QUESTI DUE CHECK NON SERVIREBBE SE ACTION MASK FUNZIONASSE BENE
        # mossa 0
        if action == 0:
            # verifico che ci sia almeno un True da spegnere
            for i in spazio['difensore'][:7]:
                if i:
                    # c'è una variabile da spegnere
                    mossaValida = True 
            # posso cambiare lo stato
            if mossaValida:
                # scorro e cambio lo stato che non mi son salvato le pos
                for i in range(len(spazio['difensore'][:7])):
                    spazio['difensore'][i] = False
        # mossa 1
        if action == 2:
            # verifico che ci sia almeno un True da spegnere
            for i in spazio['difensore'][7:]:
                if i:
                    # trovato
                    mossaValida = True
            # cambio lo stato
            if mossaValida:
                # scorro e cambio
                for i in range(7,len(spazio['difensore'])):  
                    spazio['difensore'][i] = False
        # mossa 3
        if action == 1:
            if spazio['difensore'][7]:
                mossaValida = True
                spazio['difensore'][7] = False
       
    return mossaValida




# VERIFICA QUANDO CALCOLARE LA REWARD, NEGLI ALTRI CASI 0
def reward(agent,spazio,action):
    # per la funzione di reward
    REWARD_MAP = {
        'attaccante':{
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
    print('Reward:',calcolo)
    return calcolo


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

