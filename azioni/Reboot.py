from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time
import random

class Reboot(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][11] == 0 and spazio[agent][6] == 1 and 
            (spazio[agent][14] == 1 or spazio[agent][15] == 1 or spazio[agent][16] == 1 or spazio[agent][17] == 1 or 
             spazio[agent][18] == 1 or spazio[agent][19] == 1 or spazio[agent][20] == 1) 
            and spazio[agent][0] == 1 and spazio[agent][7] == 1 
            and spazio[agent][3] == 1 and 
            # Timer 
            spazio[agent][21] <=0) :
            legal_moves[13] = 1
        else:
            legal_moves[13] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][8] = 1
        Timer = 1
        p = random.random()
        if p < 0.3 :
            # Scalare gli attacchi con una prob
            spazio[agent][14] = 0
            spazio[agent][15] = 0
            spazio[agent][16] = 0
            spazio[agent][17] = 0
            spazio[agent][18] = 0
            spazio[agent][19] = 0
            spazio[agent][20] = 0