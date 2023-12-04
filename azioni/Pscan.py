from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona


class Pscan(azioneAsincrona):
    
    def preCondizione(self,spazio,legal_moves,T1,T2,agent,mosseAsincroneRunning):
        if (spazio[agent][14] < T1 and spazio[agent][6] == 1 and spazio[agent][10] == 0 and 
            # Timer 
            spazio[agent][21] >=0
            and 0 not in mosseAsincroneRunning):
            legal_moves[0] = 1
        else:
            legal_moves[0] = 0

    def postCondizione(self,spazio,agent,mosseAsincroneRunning,action):
        self.attendi(0.001)
        spazio[agent][14] = 1
        mosseAsincroneRunning.remove(action)
