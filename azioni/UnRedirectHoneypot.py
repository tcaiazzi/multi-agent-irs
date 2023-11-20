#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class UnRedirectHoneypot(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][4] = 0
