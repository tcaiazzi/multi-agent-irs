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

        self.REWARD_MAP = {
            0 : (1,1,1),
            1 : (1,1,1),
            2 : (1,1,1),
            3 : (1,1,1),
            4 : (1,1,1),
            5 : (1,1,1),
            6 : (1,1,1),
            7 : (-100,-100,-10)
        }

    

    # Se l'attaccante trova il Timer <=0 non puo eseguire e per ora facciamo che ogni azione vale 1
    def preCondizioni(self,spazio,legal_moves):
        # Pscan
        self.PscanAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore',self.mosseAsincroneRunning)

        # Pvsftpd
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
        #legal_moves[7] = 1

        # Non ci sono mosse per l'attaccante
        for i in range(8,19,1):
            legal_moves[i] = 0


    def postCondizioni(self,action,spazio,agent):
        print('Mosse Asincrone in Running prima della mossa:',self.mosseAsincroneRunning)

        # Pscan
        if action == 0 :
            self.mosseAsincroneRunning.append(action)
            Thread(target=self.PscanAzione.postCondizione,args=(spazio,agent,self.mosseAsincroneRunning,action)).start()
            print('AVVIATO PSCAN...')
            # Timer
            #spazio[agent][21] -= 1
        
        # Pvsftpd
        elif action == 1 :
            self.PvsftpdAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] -= 60
        
        # Psmbd
        elif action == 2 :
            self.PsmbdAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] -= 40
        
        # Pphpcgi
        elif action == 3 :
            self.PphpcgiAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] -= 70
        
        # Pircd
        elif action == 4 :
            self.PircdAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] -= 30
        
        # Pdistccd
        elif action == 5 :
            self.PdistccdAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] -= 20
        
        # Prmi
        elif action == 6 :
            self.PrmiAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] -= 45
        
        # Noop solo per il timer
        elif action == 7 :
            spazio[agent][21] -= 1
        
        print('Mosse Asincrone in Running dopo la mossa:',self.mosseAsincroneRunning)
        
    def reward(self,action):
        calcolo = -(-self.wt*(self.REWARD_MAP[action][0]/self.tMax)-self.wc*(self.REWARD_MAP[action][1]/self.cMax)-self.wi*self.REWARD_MAP[action][2])
        #calcolo = REWARD_MAP[agent][action][0]+REWARD_MAP[agent][action][1]+REWARD_MAP[agent][action][2]
        print('Reward:',calcolo)
        return calcolo