from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Quarantine(azioneSincrona):
    def __init__(self):
        self.reward = (5,5,1)

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][7] == 0 and 
            (spazio[agent][14] > T2 or spazio[agent][15] > T2 or spazio[agent][16] > T2 or 
             spazio[agent][17] > T2 or spazio[agent][18] > T2 or spazio[agent][19] > T2 or 
             spazio[agent][20] > T2 ) 
            and spazio[agent][0] == 1 and spazio[agent][3] == 1 and spazio[agent][5] >= 3 
            and spazio[agent][6] == 1 and spazio[agent][10] == 0 and
            # Timer or noop attaccante
            (spazio[agent][21] <= 0 or spazio[agent][22] == 1)) :
            legal_moves[10] = 1
        else:
            legal_moves[10] = 0  

    def postCondizione(self,spazio,agent):
        spazio[agent][12] = 1
        spazio[agent][7] = 1
