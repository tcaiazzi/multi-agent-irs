#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class BlockIp(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][1] = 1
        spazio[agent][14] = 0
