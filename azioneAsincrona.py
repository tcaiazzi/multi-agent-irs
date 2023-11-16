from abc import abstractmethod

class azioneAsincrona():
    @abstractmethod
    def preCondizioni(self):
        pass
    @abstractmethod
    def postCondizioni(self):
        pass