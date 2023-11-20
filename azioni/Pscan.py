from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona


class Pscan(azioneAsincrona):
    
    def preCondizione(self,spazio,legal_moves,T1,T2,Timer,mosseAsincroneRunning):
        if (spazio['difensore'][14] < T1 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0
            and 0 not in mosseAsincroneRunning):
            legal_moves[0] = 1
        else:
            legal_moves[0] = 0

    def postCondizione(self,spazio,agent,mosseAsincroneRunning,action):
        #self.attendi(0)
        spazio[agent][14] = 1
        mosseAsincroneRunning.remove(action)
        print('Mosse Asincrone in Running dopo ATtesa e applicazione della mossa:',mosseAsincroneRunning)
        print('PSCAN TERMINATO ORA')