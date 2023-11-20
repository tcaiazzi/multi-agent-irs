#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class IncreaseLog(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][5] += 1
