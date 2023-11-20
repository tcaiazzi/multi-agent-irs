#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Update(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][10] = 1
        spazio[agent][14] = 0
        spazio[agent][15] = 0
        spazio[agent][16] = 0
        spazio[agent][17] = 0
        spazio[agent][18] = 0
        spazio[agent][19] = 0
        spazio[agent][20] = 0