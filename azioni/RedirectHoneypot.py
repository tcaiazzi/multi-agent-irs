#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class RedirectHoneypot(azioneAsincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if (spazio['difensore'][4] == 0 and
            (spazio['difensore'][15] >= T1 or spazio['difensore'][16] >= T1 or spazio['difensore'][17] >= T1 or 
             spazio['difensore'][18] >= T1 or spazio['difensore'][19] >= T1 or spazio['difensore'][20] >= T1) 
            and spazio['difensore'][0] == 1 and  spazio['difensore'][7] == 0 and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[6] = 1
        else:
            legal_moves[6] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][14] = 0
        spazio[agent][4] = 1
