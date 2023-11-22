from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class Backup(azioneAsincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,mosseAsincroneRunning):
        if (spazio['difensore'][6] == 1 and spazio['difensore'][9] == 0 and spazio['difensore'][7] == 0 and
            spazio['difensore'][3] == 1 and spazio['difensore'][5] > 1 and spazio['difensore'][0] == 1 and 
            #Timer
            spazio['difensore'][21] <=0 and
            (spazio['difensore'][15] > T1 or spazio['difensore'][16] > T1 or spazio['difensore'][17] > T1 or 
             spazio['difensore'][18] > T1 or spazio['difensore'][19] > T1 or spazio['difensore'][20] > T1)
             and 16 not in mosseAsincroneRunning):
            legal_moves[16] = 1
        else:
            legal_moves[16] = 0

    def postCondizione(self,spazio,agent,mosseAsincroneRunning,action):
        self.attendi(0.01)
        spazio[agent][9] = 1
        mosseAsincroneRunning.remove(action)
        print('Mosse Asincrone in Running dopo ATtesa e applicazione della mossa:',mosseAsincroneRunning)
        print('BACKUP TERMINATO ORA')