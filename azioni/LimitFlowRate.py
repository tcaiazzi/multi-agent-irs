from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time
import random

class LimitFlowRate(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if (spazio['difensore'][14] >= T1 and spazio['difensore'][0] ==1 and spazio['difensore'][3] == 1 and
            spazio['difensore'][6] == 1 and spazio['difensore'][2] == 0 and spazio['difensore'][5] > 0 and
            spazio['difensore'][1] == 0 and spazio['difensore'][7] == 0 and Timer <=0) :
            legal_moves[4] = 1
        else:
            legal_moves[4] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][2] = 1
		# prob 0.5
        p = random.random()
        if p < 0.5 :
            spazio[agent][14] = 0
