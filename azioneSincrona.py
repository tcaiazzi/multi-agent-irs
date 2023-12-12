from abc import abstractmethod

class azioneSincrona():

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        pass
    
    def postCondizione(self,spazio,agent):
        pass

    def reset(self):
        pass