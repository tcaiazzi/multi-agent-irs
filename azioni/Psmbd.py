from azioneSincrona import azioneSincrona

class Psmbd(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if spazio['difensore'][16] < T1 and spazio['difensore'][14] > T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0:
            legal_moves[2] = 1
        else:
            legal_moves[2] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][16] = 1
