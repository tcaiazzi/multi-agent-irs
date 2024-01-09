from azioneSincrona import azioneSincrona
import time

class Wait(azioneSincrona):
    def __init__(self):
        self.reward = (0,0,0)
    
    def preCondizione(self, spazio, legal_moves, T1, T2, agent):
        lm = [not(i) for i in legal_moves]
        #all(lm) or
        if (all(lm) and 
            # Timer or noop attaccante
            (spazio[agent][21] <= 0 or spazio[agent][22] == 1)):
            legal_moves[19] = 1
        else :
            legal_moves[19] = 0

    
    def postCondizione(self, spazio, agent):
        pass