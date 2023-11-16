from abc import abstractmethod
import time

class azioneAsincrona():
    @abstractmethod
    def preCondizioni(self):
        pass
    @abstractmethod
    def postCondizioni(self):
        pass
    def dormi(self,tempo):
        time.sleep(tempo)