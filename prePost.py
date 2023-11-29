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
    calcolo = 0
    if agent == 'attaccante':
        calcolo = attaccante.reward(action)
    else:
        calcolo = difensore.reward(action)
    return calcolo



# CONTROLLA LO STATE PER TERMINAR EO MENO
def terminationPartita(spazio,lm,num_moves,NUM_ITERS):
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

    else:
            # prova a fermarlo il fatto che le ultime due mosse se sono nop e nop (att e diff) allora basta 
            # non possono fare piu niente
            # La differenza la uso per verificare che i due non possano più fare niente INSIEME
            # altrimenti attaccante noOp assoluto al punto 10 poi attaccante fa una mosse e sblocca qualche attacco
            # attaccante agisce perche difensore non aveva il nop assoluto e quando cel'ha magari al 50 l'altro era al 10 
            # ed esce
            differenza = lm['attaccante']['nmosse']-lm['difensore']['nmosse']
            print('DIFFERENZA tempo noOp-noOp:',differenza)
            if differenza == 1 or differenza == -1:
                val = True
            # se non puo arrestarlo neanche quello provo a vedere il num di mosse
            # con noOp sempre selezionabili mi dovrebbe uscire con la condizione nell'if
            else:
                val = num_moves >= NUM_ITERS
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

def resetAgenti():
    attaccante.mosseAsincroneRunning = []
    difensore.mosseAsincroneRunning = []