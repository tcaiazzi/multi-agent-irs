from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class BlockIp(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][14] >= T2 and spazio[agent][0] == 1 and
            spazio[agent][6] == 1 and spazio[agent][1] == 0 and spazio[agent][3] == 1 and
            spazio[agent][5] > 1 and spazio[agent][7] == 0 and 
            # Timer
            spazio[agent][21] <=0) : 
            legal_moves[2] = 1
        else:
            legal_moves[2] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][1] = 1
        spazio[agent][14] = 0
