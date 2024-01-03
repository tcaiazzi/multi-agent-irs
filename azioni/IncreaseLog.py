from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class IncreaseLog(azioneSincrona):
    def __init__(self):
        self.reward = (2,1,0.05)

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][5] < 5 and 
            (spazio[agent][14] >= T1 or spazio[agent][15] >= T1 or spazio[agent][16] >= T1 or 
             spazio[agent][17] >= T1 or spazio[agent][18] >= T1 or spazio[agent][19] >= T1 or 
             spazio[agent][20] >= T1) and spazio[agent][6] == 1 and 
             spazio[agent][10] == 0 and
             # Timer or noop attaccante
             (spazio[agent][21] <= 0 or spazio[agent][22] == 1) or  (spazio[agent][1] == 1 and spazio[agent][2] == 1 and spazio[agent][4] == 1) ) : 
            
            legal_moves[8] = 1
        else:
            legal_moves[8] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][5] += 1
