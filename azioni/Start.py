#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Start(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][6] = 1
        spazio[agent][8] = 1