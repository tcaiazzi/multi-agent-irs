from abc import abstractmethod
import time

class azioneAsincrona():
    
    @abstractmethod
    def preCondizione(self,spazio,legal_moves,T1,T2,agent,mosseAsincroneRunning):
        pass

    # Dato che le mosse asincrone sono 'lente' devo far si che non siano selezionabili mentre è in atto
    @abstractmethod
    def postCondizione(self,spazio,agent,mosseAsincroneRunning,action):
        pass

    def attendi(self,tempo):
        time.sleep(tempo)