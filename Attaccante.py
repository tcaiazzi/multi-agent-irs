from Agente import Agente

from azioni.Pscan import Pscan
from azioni.Pvsftpd import Pvsftpd
from azioni.Psmbd import Psmbd
from azioni.Pphpcgi import Pphpcgi
from azioni.Pircd import Pircd
from azioni.Pdistccd import Pdistccd
from azioni.Prmi import Prmi
from azioni.noOp import noOp

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
        self.noOp = noOp()

    

    # Se l'attaccante trova il Timer <=0 non puo eseguire e per ora facciamo che ogni azione vale 1
    def preCondizioni(self,spazio,legal_moves,Timer):
        # Pscan
        self.PscanAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer,self.mosseAsincroneRunning)
       
        # Pvsftpd
        self.PvsftpdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        
        # Psmbd
        self.PsmbdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        
        # Pphpcgi
        self.PphpcgiAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        
        # Pircd
        self.PircdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        
        # Pdistccd
        self.PdistccdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        
        # Prmi
        self.PrmiAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)

        # noOp
        self.noOp.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer,self.__class__.__name__)
        #legal_moves[7] = 1

        # Non ci sono mosse per l'attaccante
        for i in range(8,19,1):
            legal_moves[i] = 0

    def postCondizioni(self,action,spazio,agent,Timer):
        print('Mosse Asincrone in Running prima della mossa:',self.mosseAsincroneRunning)

        # Pscan
        if action == 0 :
            self.mosseAsincroneRunning.append(action)
            Thread(target=self.PscanAzione.postCondizione,args=(spazio,agent,self.mosseAsincroneRunning,action)).start()
            print('AVVIATO PSCAN...')
            Timer -= 1
        
        # Pvsftpd
        elif action == 1 :
            self.PvsftpdAzione.postCondizione(spazio,agent)
            Timer -= 1
        
        # Psmbd
        elif action == 2 :
            self.PsmbdAzione.postCondizione(spazio,agent)
            Timer -= 1
        
        # Pphpcgi
        elif action == 3 :
            self.PphpcgiAzione.postCondizione(spazio,agent)
            Timer -= 1
        
        # Pircd
        elif action == 4 :
            self.PircdAzione.postCondizione(spazio,agent)
            Timer -= 1
        
        # Pdistccd
        elif action == 5 :
            self.PdistccdAzione.postCondizione(spazio,agent)
            Timer -= 1
        
        # Prmi
        elif action == 6 :
            self.PrmiAzione.postCondizione(spazio,agent)
            Timer -= 1
            
        return Timer