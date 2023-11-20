from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time
import random

class ShutDown(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if (spazio['difensore'][11] == 0 and spazio['difensore'][6] == 1 and 
            (spazio['difensore'][14] == 1 or spazio['difensore'][15] == 1 or spazio['difensore'][16] == 1 or spazio['difensore'][17] == 1 or 
             spazio['difensore'][18] == 1 or spazio['difensore'][19] == 1 or spazio['difensore'][20] == 1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 1 
            and spazio['difensore'][3] == 1 and Timer <=0) :
            legal_moves[14] = 1
        else:
            legal_moves[14] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][13] = 1
        spazio[agent][6] = 0
        # Tutti gli attacchi a 0 con una prob
        p = random.random()
        if p < 0.3 :
            # Scalare gli attacchi con una prob
            spazio[agent][14] = 0
            spazio[agent][15] = 0
            spazio[agent][16] = 0
            spazio[agent][17] = 0
            spazio[agent][18] = 0
            spazio[agent][19] = 0
            spazio[agent][20] = 0