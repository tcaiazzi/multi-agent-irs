from abc import abstractmethod
import time

class azioneAsincrona():
    @abstractmethod
    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        pass
    @abstractmethod
    def postCondizione(self,spazio,agent):
        pass
    def dormi(self,tempo):
        time.sleep(tempo)