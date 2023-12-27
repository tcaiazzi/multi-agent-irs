from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class UnLimitFlowRate(azioneSincrona):
    def __init__(self):
        self.reward = (3,1,0)

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][14] < T1 and spazio[agent][0] ==1 and
            spazio[agent][6] == 1 and spazio[agent][2] == 1 and spazio[agent][5] > 0 and 
            spazio[agent][10] == 0 and
            # Timer or noop attaccante
            (spazio[agent][21] <= 0 or spazio[agent][22] == 1)):
            legal_moves[5] = 1
        else:
            legal_moves[5] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][2] = 0
