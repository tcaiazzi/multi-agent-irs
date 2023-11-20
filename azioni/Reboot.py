#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time
import random

class Reboot(azioneAsincrona):
    
    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if (spazio['difensore'][11] == 0 and spazio['difensore'][6] == 1 and 
            (spazio['difensore'][14] == 1 or spazio['difensore'][15] == 1 or spazio['difensore'][16] == 1 or spazio['difensore'][17] == 1 or 
             spazio['difensore'][18] == 1 or spazio['difensore'][19] == 1 or spazio['difensore'][20] == 1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 1 
            and spazio['difensore'][3] == 1 and Timer <=0) :
            legal_moves[13] = 1
        else:
            legal_moves[13] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][8] = 1
        Timer = 1
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