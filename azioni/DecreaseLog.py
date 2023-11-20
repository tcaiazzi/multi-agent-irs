#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class DecreaseLog(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][5] -= 1
