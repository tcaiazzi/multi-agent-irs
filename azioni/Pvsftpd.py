from azioneSincrona import azioneSincrona

class Pvsftpd(azioneSincrona):

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][15] < T1 and spazio[agent][14] > T2 and spazio[agent][6] == 1 and spazio[agent][10] == 0 and 
            # Timer 
            spazio[agent][21] >=0): 
            legal_moves[1] = 1
        else:
            legal_moves[1] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][15] = 1
