
class agenteMossaAsincrona():

    def __init__(self,tempo, mossa,action,spazio,agent):
        self.tempoAttesa = tempo
        self.mossa = mossa
        self.action = action
        self.spazio = spazio
        self.agent = agent
    
    # Se applica la postCondizione True e allora esce dalla coda
    # Se invece non l'applica torna false
    def stepSuccessivo(self,scalare,mosseAsincroneRunning,daRimuovere):
        print('STEPSUCCESSIVO tempo di attesa rimasto:',self.tempoAttesa)
        print('STEPSUCCESSIVO attesa-scalare:',self.tempoAttesa-scalare)
        val = False
        if (self.tempoAttesa-scalare) > 0:
            self.tempoAttesa -= scalare
        else:
            val = self.postCondizione()
            mosseAsincroneRunning.remove(daRimuovere)
        return val

    def postCondizione(self):
        print('AGENTEASINCRONO applico postcondizione')
        self.mossa.postCondizione(self.spazio,self.agent)
        return True