from abc import abstractmethod

class azioneSincrona():
    @abstractmethod
    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        pass
    @abstractmethod
    def postCondizione(self,spazio,agent):
        pass