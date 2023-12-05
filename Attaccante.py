from Agente import Agente

from azioni.Pscan import Pscan
from azioni.Pvsftpd import Pvsftpd
from azioni.Psmbd import Psmbd
from azioni.Pphpcgi import Pphpcgi
from azioni.Pircd import Pircd
from azioni.Pdistccd import Pdistccd
from azioni.Prmi import Prmi
from azioni.noOp import noOp

from agenteMossaAsincrona import agenteMossaAsincrona

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

        self.REWARD_MAP = {
            0 : (1,1,1),
            1 : (1,1,1),
            2 : (1,1,1),
            3 : (1,1,1),
            4 : (1,1,1),
            5 : (1,1,1),
            6 : (1,1,1),
            7 : (0,0,0)
        }

        # Per le mosse asincrone, per il calcolo del tempo del difensore
        self.lastTimer = 0
    

    # Se l'attaccante trova il Timer <=0 non puo eseguire e per ora facciamo che ogni azione vale 1
    def preCondizioni(self,spazio,legal_moves):
        # Pscan
        self.PscanAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')

        # Pvsftpd
        if not(any(tupla[1] == 1 for tupla in self.mosseAsincroneRunning)):
            self.PvsftpdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # Psmbd
        self.PsmbdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # Pphpcgi
        self.PphpcgiAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # Pircd
        self.PircdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # Pdistccd
        self.PdistccdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # Prmi
        self.PrmiAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')

        # noOp
        self.noOp.preCondizione(spazio,legal_moves,self.T1,self.T2,self.__class__.__name__)

        # Non ci sono mosse per l'attaccante
        for i in range(8,19,1):
            legal_moves[i] = 0


    def postCondizioni(self,action,spazio,agent):
        print('Mosse Asincrone in Running prima della mossa:',self.mosseAsincroneRunning)

        # tempo appicazione della mossa sincrona
        t = 0
        # nuovo agente asincrono
        agente = 0
        # tempo mossa difensore turno precedente
        delta = abs(spazio[agent][21]-self.lastTimer)

        # Pscan
        if action == 0 :
            """ self.mosseAsincroneRunning.append(action)
            Thread(target=self.PscanAzione.postCondizione,args=(spazio,agent,self.mosseAsincroneRunning,action)).start()
            print('AVVIATO PSCAN...')
             """
            self.PscanAzione.postCondizione(spazio,agent)
            # Timer
            t = 40
        
        # Pvsftpd
        elif action == 1 :
            agente = agenteMossaAsincrona(60,self.PvsftpdAzione,action,spazio,agent)
            #self.PvsftpdAzione.postCondizione(spazio,agent)
            # Timer
            #t = 60
        
        # Psmbd
        elif action == 2 :
            self.PsmbdAzione.postCondizione(spazio,agent)
            # Timer
            t = 40
        
        # Pphpcgi
        elif action == 3 :
            self.PphpcgiAzione.postCondizione(spazio,agent)
            # Timer
            t = 70
        
        # Pircd
        elif action == 4 :
            self.PircdAzione.postCondizione(spazio,agent)
            # Timer
            t = 30
        
        # Pdistccd
        elif action == 5 :
            self.PdistccdAzione.postCondizione(spazio,agent)
            # Timer
            t = 20
        
        # Prmi
        elif action == 6 :
            self.PrmiAzione.postCondizione(spazio,agent)
            # Timer
            t = 45
        
        # Noop solo per il timer
        """ elif action == 7 :
            t = 1 """
        
        spazio[agent][21] -= t
        
        #----------------------------------------------------------------------------
        # Questo mi servirebbe a far scattare il tempo delle mosse asincrone
        # calcolo anche il delta della mossa del difensore + dell'attaccante
        for x,i in self.mosseAsincroneRunning:
            x.stepSuccessivo(delta+t,self.mosseAsincroneRunning,(x,i))

        # La metto qui perche altrimenti anche quelle appena create mi subiscono il delta del difensore
        # del turno prima
        if agente != 0:
            self.mosseAsincroneRunning.append((agente,action))

        self.lastTimer = spazio[agent][21]
        #----------------------------------------------------------------------------

        print('Mosse Asincrone in Running dopo la mossa:',self.mosseAsincroneRunning)
        

    
    
    def reset(self):
        self.mosseAsincroneRunning = []
        