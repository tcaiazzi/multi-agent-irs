#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class BlockIp(azioneAsincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if (spazio['difensore'][14] >= T2 and spazio['difensore'][0] == 1 and
            spazio['difensore'][6] == 1 and spazio['difensore'][1] == 0 and spazio['difensore'][3] == 1 and
            spazio['difensore'][5] > 1 and spazio['difensore'][7] == 0 and Timer <=0) : 
            legal_moves[2] = 1
        else:
            legal_moves[2] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][1] = 1
        spazio[agent][14] = 0
