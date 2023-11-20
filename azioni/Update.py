#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Update(azioneAsincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if (spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and spazio['difensore'][9] == 1 and Timer <=0 and 
            (spazio['difensore'][15] > T1 or spazio['difensore'][16] > T1 or spazio['difensore'][17] > T1 or 
             spazio['difensore'][18] > T1 or spazio['difensore'][19] > T1 or spazio['difensore'][20] > T1)) :
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