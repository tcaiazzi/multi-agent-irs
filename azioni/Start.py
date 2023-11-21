from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Start(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if spazio[agent][6] == 0 :
            legal_moves[15] = 1
        else:
            legal_moves[15] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][6] = 1
        spazio[agent][8] = 1