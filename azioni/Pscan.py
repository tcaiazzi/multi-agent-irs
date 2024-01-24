from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona


class Pscan(azioneSincrona):
    def __init__(self):
        self.reward = (1,1,1)
    
    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][14] < T1 and spazio[agent][6] == 1 and 
            spazio[agent][10] == 0 and spazio[agent][11] == 0 and 
            # Timer or noop difensore
            (spazio[agent][21] >=0 or spazio[agent][22] == 2)):
            legal_moves[0] = 1
        else:
            legal_moves[0] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][14] = 1
