from Agente import Agente

class agenteMossaAsincrona():

    def __init__(self, mossa,action,spazio,agent):
        self.T1 = 0.33
        self.T2 = 0.66

        self.mossa = mossa
        self.action = action
        self.spazio = spazio
        self.agent = agent
    
    # Se applica la postCondizione True e allora esce dalla coda
    # Se invece non l'applica torna false
    def stepSuccessivo(self,scalare):
        print('SCALARE:',scalare)
        val = False
        if (self.mossa.tempoAttesa-scalare) > 0:
            self.mossa.tempoAttesa -= scalare

        else:
            val = True
            self.mossa.tempoAttesa = 0
            val = self.mossa.postCondizione(self.spazio,self.agent,self.T1,self.T2)
    
        round(self.mossa.tempoAttesa,1)
        return val