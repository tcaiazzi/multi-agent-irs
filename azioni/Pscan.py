#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Pscan(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio):
        time.sleep(2)
        spazio['difensore'][14] = 1
        print('PSCAN TERMINATO ORA:',spazio)