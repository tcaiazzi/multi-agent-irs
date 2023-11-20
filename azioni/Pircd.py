from azioneSincrona import azioneSincrona

class Pircd(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,Timer):
        if spazio['difensore'][18] < T1 and spazio['difensore'][14] > T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and Timer >=0:
            legal_moves[4] = 1
        else:
            legal_moves[4] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][18] = 1