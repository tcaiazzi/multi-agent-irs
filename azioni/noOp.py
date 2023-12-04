from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import numpy as np


class noOp(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        # li notto tutti così che nel caso nessuna piu sia la mossa selezionabile (tutti 0)
        # con all avendo messo tutti una mi torna true
        l = np.copy(legal_moves)
        for i in range(len(l)) :
                l[i] = not(l[i])

        if all(l):
            if agent == 'Difensore':
                legal_moves[18] = 1
            else:
                legal_moves[7] = 1
        else: 
            if agent == 'Difensore':
                legal_moves[18] = 0
            else:
                legal_moves[7] = 0

    def postCondizione(self,spazio,agent):
        pass