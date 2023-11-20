#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Backup(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][9] = 1