#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class ManualResolution(azioneAsincrona):
    
    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if (spazio['difensore'][11] == 0 and 
            (spazio['difensore'][15] == 1 or spazio['difensore'][16] == 1 or spazio['difensore'][17] == 1 or 
             spazio['difensore'][18] == 1 or spazio['difensore'][19] == 1 or spazio['difensore'][20] == 1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 1 and spazio['difensore'][8] == 1 
            and spazio['difensore'][10] == 1 and spazio['difensore'][3] == 1 and spazio['difensore'][9] == 1 
            and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[12] = 1
        else:
            legal_moves[12] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][6] = 1
        spazio[agent][7] = 0
        spazio[agent][11] = 1
        spazio[agent][14] = 0
        spazio[agent][15] = 0
        spazio[agent][16] = 0
        spazio[agent][17] = 0
        spazio[agent][18] = 0
        spazio[agent][19] = 0
        spazio[agent][20] = 0
