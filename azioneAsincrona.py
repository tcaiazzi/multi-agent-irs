from abc import abstractmethod
import time

class azioneAsincrona():
    def __init__(self):
        pass
    
    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        pass

    # Dato che le mosse asincrone sono 'lente' devo far si che non siano selezionabili mentre è in atto
    def postCondizione(self,spazio,agent):
        pass

    def reset(self):
        self.tempoAttesa = self.tempoAttuazione
