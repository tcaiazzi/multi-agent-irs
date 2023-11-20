#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class RedirectHoneypot(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][14] = 0
        spazio[agent][4] = 1
