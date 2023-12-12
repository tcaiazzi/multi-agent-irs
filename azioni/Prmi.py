from azioneAsincrona import azioneAsincrona

class Prmi(azioneAsincrona):
    def __init__(self):
        self.tempoAttuazione = 0.8
        self.tempoAttesa = 0.8

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][20] < T1 and spazio[agent][14] > T2 and spazio[agent][6] == 1 and spazio[agent][10] == 0 and 
            # Timer or noop difensore
            (spazio[agent][21] >=0 or spazio[agent][22] == 2)):
            legal_moves[6] = 1
        else:
            legal_moves[6] = 0

    def postCondizione(self,spazio,agent):
        spazio[agent][20] = 1