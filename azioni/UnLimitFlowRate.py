#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class UnLimitFlowRate(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][2] = 0
