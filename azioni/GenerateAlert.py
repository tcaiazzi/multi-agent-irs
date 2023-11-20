#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class GenerateAlert(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][3] = 1
