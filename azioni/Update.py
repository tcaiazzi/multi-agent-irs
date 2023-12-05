from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Update(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][6] == 1 and spazio[agent][10] == 0 and spazio[agent][9] == 1 and 
            # Timer or noop attaccante
            (spazio[agent][21] <= 0 or spazio[agent][22] == 1) and 
            (spazio[agent][15] > T1 or spazio[agent][16] > T1 or spazio[agent][17] > T1 or 
             spazio[agent][18] > T1 or spazio[agent][19] > T1 or spazio[agent][20] > T1)) :
            legal_moves[17] = 1
        else:
            legal_moves[17] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][10] = 1
        spazio[agent][14] = 0
        spazio[agent][15] = 0
        spazio[agent][16] = 0
        spazio[agent][17] = 0
        spazio[agent][18] = 0
        spazio[agent][19] = 0
        spazio[agent][20] = 0