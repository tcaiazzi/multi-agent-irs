#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class DecreaseLog(azioneAsincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if (spazio['difensore'][5] > 0 and 
            (spazio['difensore'][14] < T2 or spazio['difensore'][15] < T2 or spazio['difensore'][16] < T2 or 
             spazio['difensore'][17] < T2 or spazio['difensore'][18] < T2 or spazio['difensore'][19] < T2 or 
             spazio['difensore'][20] < T2) and spazio['difensore'][6] == 1 and Timer <=0) : 
            legal_moves[9] = 1
        else:
            legal_moves[9] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][5] -= 1
