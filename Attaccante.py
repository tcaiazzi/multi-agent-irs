from Agente import Agente

from azioni.Pscan import Pscan
from azioni.Pvsftpd import Pvsftpd
from azioni.Psmbd import Psmbd
from azioni.Pphpcgi import Pphpcgi
from azioni.Pircd import Pircd
from azioni.Pdistccd import Pdistccd
from azioni.Prmi import Prmi

from threading import Thread


class Attaccante(Agente):
    def __init__(self):
        super().__init__()
        self.PscanAzione = Pscan()
        self.PvsftpdAzione = Pvsftpd()
        self.PsmbdAzione = Psmbd()
        self.PphpcgiAzione = Pphpcgi()
        self.PircdAzione = Pircd()
        self.PdistccdAzione = Pdistccd()
        self.PrmiAzione = Prmi()
    

    # Se l'attaccante trova il Timer <=0 non puo eseguire e per ora facciamo che ogni azione vale 1
    def preCondizioni(self,spazio,legal_moves,Timer):
        # Pscan
        self.PscanAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if spazio['difensore'][14] < self.T1 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0:
            legal_moves[0] = 1 
        else:
            legal_moves[0] = 0
        """
        # Pvsftpd
        self.PvsftpdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if spazio['difensore'][15] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0: 
            legal_moves[1] = 1
        else:
            legal_moves[1] = 0 """
        # Psmbd
        self.PsmbdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if spazio['difensore'][16] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0:
            legal_moves[2] = 1
        else:
            legal_moves[2] = 0 """
        # Pphpcgi
        self.PphpcgiAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if spazio['difensore'][17] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0:
            legal_moves[3] = 1
        else:
            legal_moves[3] = 0 """
        # Pircd
        self.PircdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if spazio['difensore'][18] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0:
            legal_moves[4] = 1
        else:
            legal_moves[4] = 0 """
        # Pdistccd
        self.PdistccdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if spazio['difensore'][19] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0:
            legal_moves[5] = 1
        else:
            legal_moves[5] = 0 """
        # Prmi
        self.PrmiAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if spazio['difensore'][20] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0:
            legal_moves[6] = 1
        else:
            legal_moves[6] = 0 """
        legal_moves[7] = 1

        # Non ci sono mosse per l'attaccante
        for i in range(8,19,1):
            legal_moves[i] = 0

    def postCondizioni(self,action,spazio,agent,Timer):

        # Pscan
        if action == 0 :
            #spazio['difensore'][14] = 1
            #self.PscanAzione.postCondizione(spazio)
            self.azioniAsincroneRun.append(action)
            Thread(target=self.PscanAzione.postCondizione,args=(spazio,agent,)).start()
            print('AVVIATO PSCAN...')
            Timer -= 1
        # Pvsftpd
        elif action == 1 :
            #spazio[agent][15] = 1
            self.PvsftpdAzione.postCondizione(spazio,agent)
            Timer -= 1
        # Psmbd
        elif action == 2 :
            #spazio[agent][16] = 1
            self.PsmbdAzione.postCondizione(spazio,agent)
            Timer -= 1
        # Pphpcgi
        elif action == 3 :
            #spazio[agent][17] = 1
            self.PphpcgiAzione.postCondizione(spazio,agent)
            Timer -= 1
        # Pircd
        elif action == 4 :
            #spazio[agent][18] = 1
            self.PircdAzione.postCondizione(spazio,agent)
            Timer -= 1
        # Pdistccd
        elif action == 5 :
            #spazio[agent][19] = 1
            self.PdistccdAzione.postCondizione(spazio,agent)
            Timer -= 1
        # Prmi
        elif action == 6 :
            #spazio[agent][20] = 1
            self.PrmiAzione.postCondizione(spazio,agent)
            Timer -= 1
            
        return Timer