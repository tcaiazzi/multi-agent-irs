from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class GenerateAlert(azioneSincrona):
    
    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if ((spazio[agent][14] >= T1 or spazio[agent][15] >= T1 or spazio[agent][16] >= T1 or
            spazio[agent][17] >= T1 or spazio[agent][18] >= T1 or spazio[agent][19] >= T1 or 
            spazio[agent][20] >= T1) and spazio[agent][3] == 0 and spazio[agent][6] == 1 and 
            #Timer
            spazio[agent][21] <=0):
            legal_moves[0] = 1
        else:
            legal_moves[0] = 0
    
    def postCondizione(self,spazio,agent):
        spazio[agent][3] = 1
