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

T1 = 0.33
T2 = 0.66



# APPLICA L'AZIONE ALLo SPAZIO 'LOGICA'
def doAction(action,spazio,agent):
    # Post COndizioni
    # STATO
    # [ firewall([True/False])(0), blockedip([])(1), flowlimit_ips([])(2), alert([True/False])(3), honeypot_ips([])(4),
    # log_verb([0-5])(5),
    # active([True/False])(6), quarantined([True/False])(7), rebooted([True/False])(8), backup([True/False])(9),
    # updated([True/False])(10),
    # manuallySolved([True/False])(11), everQuarantined([True/False])(12), everShutDown([True/False])(13),
    # +
    # pscan([0-1])(14), pvsftpd([0-1])(15), psmbd([0-1])(16), pphpcgi([0-1])(17), pircd([0-1])(18), pdistccd([0-1])(19), prmi([0-1])(20),]


    mossaValida = True
    if agent == 'difensore':
        # GenerateAlert
        if action == 0 :
            spazio[agent][3] = 1
        # FirewallActivation
        elif action == 1 :
            spazio[agent][0] = 1
        # BlockSourceIp
        elif action == 2 :
            spazio[agent][1] = 1
            spazio[agent][14] = 0
        # UnblockSourceIp
        elif action == 3 :
            spazio[agent][1] = 0
        # FlowRateLimit
        elif action == 4 :
            spazio[agent][2] = 1
            # prob 0.5
            spazio[agent][14] = 0
        # UnlimitFlowRate
        elif action == 5 :
            spazio[agent][2] = 0
        # RedirectToHoneypot
        elif action == 6 :
            spazio[agent][4] = 1
            # Pxxx da scalare con prob 0.5
        # UnHoneypot
        elif action == 7 :
            spazio[agent][4] = 0
        # IncreaseLog
        elif action == 8 :
            spazio[agent][5] += 1
        # DecreaseLog
        elif action == 9 :
            spazio[agent][5] -= 1
        # QuarantineHost
        elif action == 10 :
            spazio[agent][12] = 1
            spazio[agent][7] = 1
            # Pxx da scalare con prob
        # UnQuarantineHost
        elif action == 11 :
            spazio[agent][7] = 0
        # ManualResolution
        elif action == 12 :
            spazio[agent][11] = 1
            # Pxx da scalare con prob
        # SystemReboot
        elif action == 13 :
            # Scalare gli attacchi con una prob
            spazio[agent][14] = 0
            spazio[agent][15] = 0
            spazio[agent][16] = 0
            spazio[agent][17] = 0
            spazio[agent][18] = 0
            spazio[agent][19] = 0
            spazio[agent][20] = 0
        # SystemShutdown
        elif action == 14 :
            spazio[agent][13] = 1
            spazio[agent][6] = 0
            # Tutti gli attacchi a 0 con una prob
            spazio[agent][14] = 0
            spazio[agent][15] = 0
            spazio[agent][16] = 0
            spazio[agent][17] = 0
            spazio[agent][18] = 0
            spazio[agent][19] = 0
            spazio[agent][20] = 0
        # SystemStart
        elif action == 15 :
            spazio[agent][6] = 1
        # BackupHost
        elif action == 16 :
            spazio[agent][9] = 1
        # SoftwareUpdate
        elif action == 17 :
            spazio[agent][10] = 1

    
    elif agent == 'attaccante':
        # Pscan
        if action == 0 :
            spazio['difensore'][14] = 1
        # Pvsftpd
        elif action == 1 :
            spazio['difensore'][15] = 1
        # Psmbd
        elif action == 2 :
            spazio['difensore'][16] = 1
        # Pphpcgi
        elif action == 3 :
            spazio['difensore'][17] = 1
        # Pircd
        elif action == 4 :
            spazio['difensore'][18] = 1
        # Pdistccd
        elif action == 5 :
            spazio['difensore'][19] = 1
        # Prmi
        elif action == 6 :
            spazio['difensore'][20] = 1
       
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
            7 : (0,0,0)
        },
        'difensore':{
            0 : (1,1,0),
            1 : (2,1,0),
            2 : (1,3,0.3),
            3 : (1,3,0),
            4 : (3,1,0.2),
            5 : (3,1,0),
            6 : (3,3,0.1),
            7 : (3,3,0),
            8 : (2,1,0.05),
            9 : (1,1,0),
            10 : (5,5,1),
            11 : (5,5,0),
            12 : (3600,200,0),
            13 : (60,6,0.7),
            14 : (30,6,1),
            15 : (30,6,0),
            16 : (3600,10,0.1),
            17 : (600,300,0.1)
        }
    }
    wt = 0.5
    wc = 0.5
    wi = 0.5
    tMax = 100
    cMax = 100
    calcolo = -(-wt*(REWARD_MAP[agent][action][0]/tMax)-wc*(REWARD_MAP[agent][action][1]/cMax)-wi*(1))
    #calcolo = REWARD_MAP[agent][action][0]+REWARD_MAP[agent][action][1]+REWARD_MAP[agent][action][2]
    print('Reward:',calcolo)
    return calcolo



# CONTROLLA LO STATE PER TERMINAR EO MENO
def terminationPartita(spazio):
    val = False
    check = 0

    if spazio['difensore'][14] < T1 and spazio['difensore'][15] < T1 and spazio['difensore'][16] < T1 and spazio['difensore'][17] < T1 and spazio['difensore'][18] < T1 and spazio['difensore'][19] < T1 and spazio['difensore'] [20] < T1 and spazio['difensore'] [1] == 0 and spazio['difensore'][2] == 0 and spazio['difensore'][4] == 0 and spazio['difensore'][5] == 0 and spazio['difensore'][6] == 1 and spazio['difensore'][7] == 0:
        val = True
    return val

