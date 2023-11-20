#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time
import random

class ShutDown(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][13] = 1
        spazio[agent][6] = 0
        # Tutti gli attacchi a 0 con una prob
        p = random.random()
        if p < 0.3 :
            # Scalare gli attacchi con una prob
            spazio[agent][14] = 0
            spazio[agent][15] = 0
            spazio[agent][16] = 0
            spazio[agent][17] = 0
            spazio[agent][18] = 0
            spazio[agent][19] = 0
            spazio[agent][20] = 0