from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class DecreaseLog(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][5] > 0 and 
            (spazio[agent][14] < T2 or spazio[agent][15] < T2 or spazio[agent][16] < T2 or 
             spazio[agent][17] < T2 or spazio[agent][18] < T2 or spazio[agent][19] < T2 or 
             spazio[agent][20] < T2) and spazio[agent][6] == 1 and 
             # Timer 
             spazio[agent][21] <= 0 
             #and 9 not in mosseAsincroneRunning
             ) : 
            #mosseAsincroneRunning.append(9)
            legal_moves[9] = 1
        else:
            legal_moves[9] = 0

    def postCondizione(self,spazio,agent):
        #time.sleep(0.0001)
        #print("RIMOZIONE DECRELOG:",mosseAsincroneRunning)
        #print(action)
        #mosseAsincroneRunning.remove(action)
        #print("RIMOsso DECRELOG:",mosseAsincroneRunning)
        spazio[agent][5] -= 1
