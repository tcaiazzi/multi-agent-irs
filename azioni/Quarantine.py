#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Quarantine(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][12] = 1
        spazio[agent][7] = 1
