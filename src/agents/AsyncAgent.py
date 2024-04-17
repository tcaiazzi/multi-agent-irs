class AsyncAgent:

    def __init__(self, mossa,action,spazio,agent):
        self.T1 = 0.33
        self.T2 = 0.66

        self.mossa = mossa
        self.action = action
        self.spazio = spazio
        self.agent = agent
    
    # Se applica la postCondizione se è finito il tempo di attesa della mossa
    # ovvero è passato il tempo necessario all'esecuzione
    # torna true se ho eseguito la mossa così la rimuovo altrimenti false
    def stepSuccessivo(self,scalare,action,mAttS):
        """ print('MOSSA:',self.mossa)
        print('Tempo Attesa:',self.mossa.tempoAttesa)
        print('Tempo Attuazione:',self.mossa.tempoAttuazione) """
        val = False
        if (self.mossa.waiting_time - scalare) > 0:
            self.mossa.waiting_time = round((self.mossa.waiting_time - scalare), 2)
        else:
            val = True
            self.mossa.waiting_time = 0
            self.mossa.verify_postconditions(self.spazio, self.agent, action, mAttS)

        return val