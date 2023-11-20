#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time
import random

class Reboot(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][8] = 1
        Timer = 1
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