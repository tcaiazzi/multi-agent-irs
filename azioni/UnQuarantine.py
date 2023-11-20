#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class UnQuarantine(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][7] = 0
