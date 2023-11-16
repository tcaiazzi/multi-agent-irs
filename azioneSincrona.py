from abc import abstractmethod

class azioneSincrona():
    @abstractmethod
    def preCondizione():
        pass
    @abstractmethod
    def postCondizione(self,spazio):
        pass