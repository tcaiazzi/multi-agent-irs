#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time
import random

class LimitFlowRate(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][2] = 1
		# prob 0.5
        p = random.random()
        if p < 0.5 :
            spazio[agent][14] = 0
