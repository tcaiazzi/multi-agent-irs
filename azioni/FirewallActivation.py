#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class FirewallActivation(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][0] = 1
