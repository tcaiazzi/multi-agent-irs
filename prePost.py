from matplotlib import pyplot as plt
import numpy as np
import random

from Attaccante import Attaccante
from Difensore import Difensore

from threading import Thread

attaccante = Attaccante()
difensore = Difensore()

T1 = 0.33
T2 = 0.66

mosseDifensore = ['Generate alert','FirewallActivation','BlockSourceIp','UnblockSourceIp','FlowRateLimit','UnlimitFlowRate',
                  'RedirectToHoneypot','UnRedirectToHoneypot','IncreaseLog','DecreaseLog','QuarantineHost','UnQuarantineHost',
                  'ManualResolution','SystemReboot','SystemShutdown','SystemStart','BackupHost','SoftwareUpdate','noOp']

mosseAttaccante = ['Pscan','Pvsftpd','Psmbd','Pphpcgi','Pircd','Pdistccd','Prmi', 'noOp']


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

""" lastMosse = {
    'attaccante': -1,
    'difensore': -1,
} """


# Pre condizioni codificate nell'action mask
def preCondizioni(agent,spazio,legal_moves):
    # STATO
        # [ firewall([True/False])(0), blockedip([])(1), flowlimit_ips([])(2), alert([True/False])(3), honeypot_ips([])(4),
        # log_verb([0-5])(5),
        # active([True/False])(6), quarantined([True/False])(7), rebooted([True/False])(8), backup([True/False])(9),
        # updated([True/False])(10),
        # manuallySolved([True/False])(11), everQuarantined([True/False])(12), everShutDown([True/False])(13),
        # +
        # pscan([0-1])(14), pvsftpd([0-1])(15), psmbd([0-1])(16), pphpcgi([0-1])(17), pircd([0-1])(18), pdistccd([0-1])(19), prmi([0-1])(20),]

    if agent == 'difensore':
        # pre condizioni del difensore
        difensore.preCondizioni(spazio,legal_moves)

    else:
        # pre condizioni dell'attaccante
        # In tutte ho inserito che se il software viene aggiornato neanche più il pscan si può fare 
        # altrimenti non ce la farebbe mai ad uscire perche deve decrementare i log
        attaccante.preCondizioni(spazio,legal_moves)
        

    if agent == 'difensore':
        print('-----------------------------------------------------------------------------------------')
        print(legal_moves)
        for i in range(len(mosseDifensore)):
            if legal_moves[i] == 1 :
                print(mosseDifensore[i])
    else :
        print('-----------------------------------------------------------------------------------------')
        print(legal_moves)
        for i in range(len(mosseAttaccante)):
            if legal_moves[i] == 1 :
                print(mosseAttaccante[i])



# APPLICA L'AZIONE ALLo SPAZIO 'LOGICA'
def postCondizioni(action,spazio,agent):
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
        print(mosseDifensore[action])
        Timer = difensore.postCondizioni(action,spazio,agent)
        
    elif agent == 'attaccante':
        Timer = attaccante.postCondizioni(action,spazio,'difensore')
        
    return Timer




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
            17 : (600,300,0.1),
            18 : (1000,100,100)
            # voglio scoraggiare il difensore a non fare nulla così che faccia qualcosa per salvaguardare
            # in realta basterebbe che il l'attaccante influisca ed il difensore ottenga una reward positiva (?)
            # perchese influisce l'attaccante comunque il difensore se scheglie nop non la peggiora
        }
    }
    wt = 0.16
    wc = 0.34
    wi = 0.50
    tMax = 100
    cMax = 100
    calcolo = (-wt*(REWARD_MAP[agent][action][0]/tMax)-wc*(REWARD_MAP[agent][action][1]/cMax)-wi*REWARD_MAP[agent][action][2])
    #calcolo = REWARD_MAP[agent][action][0]+REWARD_MAP[agent][action][1]+REWARD_MAP[agent][action][2]
    print('Reward:',calcolo)
    return calcolo



# CONTROLLA LO STATE PER TERMINAR EO MENO
def terminationPartita(spazio):
    val = False
    check = 0
    # clean system state + esclusione degli altri parametri (lascio solo il check degli attacchi sotto T1 
    # come se gli altri fossero altri subsets states con minace in sicurezza)
    # stato terminale attaccante con tutti attacchi on
    # Consigliata dal professore
    if ((spazio['difensore'][14] < T1 and spazio['difensore'][15] < T1 and spazio['difensore'][16] < T1 and spazio['difensore'][17] < T1 and spazio['difensore'][18] < T1 and spazio['difensore'][19] < T1 and spazio['difensore'] [20] < T1 
        and spazio['difensore'] [1] == 0 and spazio['difensore'][2] == 0 and spazio['difensore'][4] == 0 and spazio['difensore'][5] == 0 and spazio['difensore'][6] == 1 and spazio['difensore'][7] == 0) or 
        (spazio['difensore'][14] == 1 and spazio['difensore'][15] == 1 and spazio['difensore'][16] == 1 and spazio['difensore'][17] == 1 and spazio['difensore'][18] == 1 and spazio['difensore'][19] == 1 and spazio['difensore'] [20] == 1)):
        val = True
    return val

# Randomicità dello stato
def generazioneSpazioRandom():
    # STATO CHE AVEVO SUPPOSTO IO DI PARTENZA
    spazio = [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    """ for i in range(21):
        if i == 5:
            spazio[i] = random.randint(0,5)
        else:
            spazio[i] = random.randint(0,1) """
    return spazio

