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



    # Se l'attaccante trova il Timer <=0 non puo eseguire e per ora facciamo che ogni azione vale 1
    def preCondizioni(self,spazio,legal_moves):

        # Pscan
        self.PscanAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')

        # Pvsftpd
        if not(any(tupla[1] == 1 for tupla in self.mosseAsincroneRunning)):
            self.PvsftpdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # Psmbd
        if not(any(tupla[1] == 2 for tupla in self.mosseAsincroneRunning)):
            self.PsmbdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # Pphpcgi
        if not(any(tupla[1] == 3 for tupla in self.mosseAsincroneRunning)):
            self.PphpcgiAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # Pircd
        if not(any(tupla[1] == 4 for tupla in self.mosseAsincroneRunning)):
            self.PircdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # Pdistccd
        if not(any(tupla[1] == 5 for tupla in self.mosseAsincroneRunning)):
            self.PdistccdAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # Prmi
        if not(any(tupla[1] == 6 for tupla in self.mosseAsincroneRunning)):
            self.PrmiAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')

        # noOp
        self.noOp.preCondizione(spazio,legal_moves,self.T1,self.T2,self.__class__.__name__)

        # Non ci sono mosse per l'attaccante
        for i in range(8,19,1):
            legal_moves[i] = 0


    def postCondizioni(self,action,spazio,agent):
       
        #-----------------------------------------------------
        # tempo appicazione della mossa sincrona
        t = 0
        # nuovo agente asincrono
        agente = 0
        # tempo mossa difensore turno precedente
        delta = abs(spazio[agent][21]-self.lastTimer)
        # azzero i nop
        spazio[agent][22] = 0
        #-----------------------------------------------------

        # Pscan
        if action == 0 :
            """ self.mosseAsincroneRunning.append(action)
            Thread(target=self.PscanAzione.postCondizione,args=(spazio,agent,self.mosseAsincroneRunning,action)).start()
            print('AVVIATO PSCAN...')
             """
            self.PscanAzione.postCondizione(spazio,agent)
            # Timer
            t = self.PscanAzione.reward[0]
        
        # Pvsftpd
        elif action == 1 :
            agente = agenteMossaAsincrona(self.PvsftpdAzione,action,spazio,agent)
            #self.PvsftpdAzione.postCondizione(spazio,agent)
            # Timer
            #t = 60
        
        # Psmbd
        elif action == 2 :
            agente = agenteMossaAsincrona(self.PsmbdAzione,action,spazio,agent)
            #self.PsmbdAzione.postCondizione(spazio,agent)
            # Timer
            #t = 40
        
        # Pphpcgi
        elif action == 3 :
            agente = agenteMossaAsincrona(self.PphpcgiAzione,action,spazio,agent)
            #self.PphpcgiAzione.postCondizione(spazio,agent)
            # Timer
            #t = 70
        
        # Pircd
        elif action == 4 :
            agente = agenteMossaAsincrona(self.PircdAzione,action,spazio,agent)
            #self.PircdAzione.postCondizione(spazio,agent)
            # Timer
            #t = 30
        
        # Pdistccd
        elif action == 5 :
            agente = agenteMossaAsincrona(self.PdistccdAzione,action,spazio,agent)
            #self.PdistccdAzione.postCondizione(spazio,agent)
            # Timer
            #t = 20
        
        # Prmi
        elif action == 6 :
            agente = agenteMossaAsincrona(self.PrmiAzione,action,spazio,agent)
            #self.PrmiAzione.postCondizione(spazio,agent)
            # Timer
            #t = 45
        
        # Noop solo per il timer
        elif action == 7 :
            self.noOp.postCondizione(spazio,self.__class__.__name__)
        
        spazio[agent][21] -= round(t,2)
        
        #----------------------------------------------------------------------------
        self.aggiornaMosseAsincrone(round(delta+t,2),agente,action)

        self.lastTimer = round(spazio[agent][21],2)
        #----------------------------------------------------------------------------

    def reward(self, action):
        azione = 0
        # Pscan
        if action == 0 :
            azione = self.PscanAzione.reward
        
        # Pvsftpd
        elif action == 1 :
            azione =  self.PvsftpdAzione.reward
            
        # Psmbd
        elif action == 2 :
            azione = self.PsmbdAzione.reward
         
        # Pphpcgi
        elif action == 3 :
            azione = self.PphpcgiAzione.reward
          
        # Pircd
        elif action == 4 :
            azione = self.PircdAzione.reward
            
        # Pdistccd
        elif action == 5 :
            azione = self.PdistccdAzione.reward
          
        # Prmi
        elif action == 6 :
            azione = self.PrmiAzione.reward
        
        # Noop solo per il timer
        elif action == 7 :
            azione = self.noOp.rewardAtt

        return super().reward(azione)
        
    def reset(self):
        super().reset()
        self.PscanAzione.reset()
        self.PvsftpdAzione.reset()
        self.PsmbdAzione.reset()
        self.PphpcgiAzione.reset()
        self.PircdAzione.reset()
        self.PdistccdAzione.reset()
        self.PrmiAzione.reset()
        