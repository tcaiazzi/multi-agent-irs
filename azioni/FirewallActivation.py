from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class FirewallActivation(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if ((spazio['difensore'][14] >= T1 or spazio['difensore'][15] >= T1 or spazio['difensore'][16] >= T1 or 
            spazio['difensore'][17] >= T1 or spazio['difensore'][18] >= T1 or spazio['difensore'][19] >= T1 or 
            spazio['difensore'][20] >= T1 and Timer <=0) 
            and spazio['difensore'][0] == 0 and spazio['difensore'][6] == 1 and spazio['difensore'][7] == 0 and spazio['difensore'][5] > 0):
            legal_moves[1] = 1
        else:
            legal_moves[1] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][0] = 1
