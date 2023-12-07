
class agenteMossaAsincrona():

    def __init__(self, mossa,action,spazio,agent):
        self.mossa = mossa
        self.action = action
        self.spazio = spazio
        self.agent = agent
    
    # Se applica la postCondizione True e allora esce dalla coda
    # Se invece non l'applica torna false
    def stepSuccessivo(self,scalare,mosseAsincroneRunning,daRimuovere):
        print('STEPSUCCESSIVO tempo di attesa rimasto:',self.mossa.tempoAttesa)
        print('STEPSUCCESSIVO attesa-scalare:',self.mossa.tempoAttesa-scalare)
        val = False
        if (self.mossa.tempoAttesa-scalare) > 0:
            self.mossa.tempoAttesa -= scalare
        else:
            val = self.postCondizione()
            mosseAsincroneRunning.remove(daRimuovere)
        return val

    def postCondizione(self):
        print('AGENTEASINCRONO applico postcondizione')
        self.mossa.postCondizione(self.spazio,self.agent)
        return True