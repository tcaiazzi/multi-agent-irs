from abc import abstractmethod
import time

class azioneAsincrona():
    def __init__(self):
        pass
    
    @abstractmethod
    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        pass

    # Dato che le mosse asincrone sono 'lente' devo far si che non siano selezionabili mentre è in atto
    @abstractmethod
    def postCondizione(self,spazio,agent):
        pass
