from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class IncreaseLog(azioneAsincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,agent,mosseAsincroneRunning):
        if (spazio[agent][5] < 5 and 
            (spazio[agent][14] >= T1 or spazio[agent][15] >= T1 or spazio[agent][16] >= T1 or 
             spazio[agent][17] >= T1 or spazio[agent][18] >= T1 or spazio[agent][19] >= T1 or 
             spazio[agent][20] >= T1) and spazio[agent][6] == 1 and 
             # Timer 
             spazio[agent][21] <=0 and 8 not in mosseAsincroneRunning) : 
            
            legal_moves[8] = 1
        else:
            legal_moves[8] = 0

    def postCondizione(self,spazio,agent,mosseAsincroneRunning,action):
        self.attendi(0.0001)
        mosseAsincroneRunning.remove(action)
        spazio[agent][5] += 1
