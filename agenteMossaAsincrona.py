from Agente import Agente

class agenteMossaAsincrona(Agente):

    def __init__(self, mossa,action,spazio,agent):
        super().__init__()
        self.mossa = mossa
        self.action = action
        self.spazio = spazio
        self.agent = agent
    
    # Se applica la postCondizione True e allora esce dalla coda
    # Se invece non l'applica torna false
    def stepSuccessivo(self,scalare,mosseAsincroneRunning,daRimuovere):
        print('Scalare:',scalare)
        val = False
        if (self.mossa.tempoAttesa-scalare) > 0:
            self.mossa.tempoAttesa -= scalare
            val = self.mossa.postCondizione(self.spazio,self.agent,self.T1,self.T2)

        else:
            self.mossa.tempoAttesa = 0
            val = self.mossa.postCondizione(self.spazio,self.agent,self.T1,self.T2)
            mosseAsincroneRunning.remove(daRimuovere)
    
        round(self.mossa.tempoAttesa,1)
        return val