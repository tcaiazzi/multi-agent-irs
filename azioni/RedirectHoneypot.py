from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class RedirectHoneypot(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][4] == 0 and
            (spazio[agent][15] >= T1 or spazio[agent][16] >= T1 or spazio[agent][17] >= T1 or 
             spazio[agent][18] >= T1 or spazio[agent][19] >= T1 or spazio[agent][20] >= T1) 
            and spazio[agent][0] == 1 and  spazio[agent][7] == 0 and spazio[agent][6] == 1 and 
            # Timer
            spazio[agent][21] <=0) :
            legal_moves[6] = 1
        else:
            legal_moves[6] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][14] = 0
        spazio[agent][4] = 1
