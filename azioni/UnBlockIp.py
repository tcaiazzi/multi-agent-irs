from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class UnBlockIp(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][14] < T2 and spazio[agent][0] == 1  and
            spazio[agent][6] == 1 and spazio[agent][1] == 1  and
            spazio[agent][5] > 1 and 
            # Timer 
            spazio[agent][21] <=0) :
            legal_moves[3] = 1
        else:
            legal_moves[3] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][1] = 0