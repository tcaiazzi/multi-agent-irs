from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona


class noOp(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,Timer,agent):
        if agent == 'Difensore':
            legal_moves[18] = 1
        else:
            legal_moves[7] = 1

    def postCondizione(self,spazio,agent):
        pass