#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Pscan():
    
    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if spazio['difensore'][14] < T1 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0:
            legal_moves[0] = 1
        else:
            legal_moves[0] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][14] = 1
        print('PSCAN TERMINATO ORA:',spazio)