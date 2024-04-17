from agents.AsyncAgent import AsyncAgent
from actions.AsyncMove import AsyncMove
from actions.SyncMove import SyncMove


class Agent:

    def __init__(self):

        self.sincronaAzione = SyncMove()
        self.asincronaAzione = AsyncMove(1.0, 1.0)

        self.mosseAsincroneRunning = []
        # Per le mosse asincrone, per il calcolo del tempo del difensore
        #self.lastTimer = 0
        self.mosseEseguite = []

        self.wt = 1
        self.wc = 0
        self.wi = 0
        self.tMax = 1
        self.cMax = 1


    def lenMosseAsincroneRunning(self):
        return len(self.mosseAsincroneRunning)


    def lenMosseEseguite(self):
        return len(self.mosseEseguite)


    def preCondizioni(self,spazio,legal_moves,mAgentSinc,mAgentAsinc,agent,timer):
        mAgentTot = (mAgentSinc+mAgentAsinc)

        # controllo chi dei due agenti è e se il timer è a suo famore
        if (spazio['defender'][timer] <=0 and agent == 'defender'):
            # Per tutte le mosse sincrone
            self.sincronaAzione.preCondizione(spazio,legal_moves,mAgentSinc,agent,self.mosseEseguite)

            # Per tutte le mosse asincrone
            for mossa in range(mAgentSinc,mAgentTot,1):
                # controllo se la mosse asincrona è in running
                running = 0
                if any(tupla[1] == mossa for tupla in self.mosseAsincroneRunning):
                    running = 1
                self.asincronaAzione.verify_preconditions(spazio, legal_moves, mossa, agent, mAgentSinc, self.mosseEseguite, running)
            


        # controllo chi dei due agenti è e se il timer è a suo famore
        if (spazio['defender'][timer] >=0 and agent == 'attacker'):
            # Per tutte le mosse sincrone
            self.sincronaAzione.preCondizione(spazio,legal_moves,mAgentSinc,agent,self.mosseEseguite)

            # Per tutte le mosse asincrone
            for mossa in range(mAgentSinc,mAgentTot):
                #print(f'PRECONDIZIONI MOSSE ASINCRONE:{mossa}')
                # mossa asincrona non in running
                running = 0
                if any(tupla[1] == mossa for tupla in self.mosseAsincroneRunning):
                    running = 1
                self.asincronaAzione.verify_preconditions(spazio, legal_moves, mossa, agent, mAgentSinc, self.mosseEseguite, running)

        # Fare check mossa wait
        # vale solo quando ci sono mosse asinc in running e non ha più mosse sinc
        sincDisp = False
        asincDisp = False
        for i in range(mAgentSinc):
            if legal_moves[i] == 1:
                sincDisp = True   

        for i in range(mAgentSinc,mAgentTot):
            if legal_moves[i] == 1:
                asincDisp = True

        # se non ci sono 
        if (len(self.mosseAsincroneRunning) != 0 and not(sincDisp) and not(asincDisp)) :
            legal_moves[timer] = 1
        else:
            legal_moves[timer] = 0

        # controllo che nessuna mossa sia eseguibile NOOP
        noopPosition = timer + 1
        check = [ not(legal_moves[i]) for i in range(len(legal_moves)-1)]
        #print(f'CHECK NOOP:{check}')
        if all(check):
            # abilito la noop
            legal_moves[noopPosition] = 1
        else:
            legal_moves[noopPosition] = 0
        

    def postCondizioni(self,action,spazio,agent,mosse,timer,mAgentSinc):

        #-----------------------------------------------------
        # tempo appicazione della mossa sincrona
        t = 0
        # nuovo agente asincrono
        agente = 0

        # tempo mossa difensore turno precedente
        #delta = abs(spazio[agent][timer]-self.lastTimer)
        #delta = lastTimer
        #print('LASTTIMER:',lastTimer)
        # azzero i nop
        #spazio[agent][22] = 0
        #-----------------------------------------------------

        # tnop usato perche nop non scala il tempo se l'agente ha ancora mosse asincrone e/o sincrone da fare
        # lo scala solo nel momento in cui il nop viene selezionato perche son finite le mosse
        # e devo scalare il tempo alle mosse asincrone affinche finiscano
        # ma non mi altera ai il timer
        tnop = 0 
        # se l'azione è sincrona fa...
        if action < mAgentSinc :
            self.sincronaAzione.postCondizione(spazio,agent,action)
            self.mosseEseguite.append(action)
            t = 0.5
        # se l'azione è asincrona fa...
        else:
            if action < timer:
                agente = AsyncAgent(AsyncMove(),action,spazio,agent)
                agente.mossa.waiting_time = agente.mossa.execution_time
            else:
                # se invece la mossa è noop...
                # ed è i suo turno MA QUESTO IF FUNZIONA SOLO SE HANNO LO STESSO NUMERO DI AZIONI SINCRONE
                # PERCHE IL TIMER ALLA FINE SARà SEMPRE 0
                """ if agent == 'attacker':
                    if spazio['defender'][timer] >= 0:
                        # se ci sono mosse asincrone noop me le deve far terminare
                        t = 0.5
                        # verifico che tutte le mosse sincrone (SCALA TEMPO) siano state usate
                        for i in range(mAgentSinc):
                            # se almeno 1 non usata t = 0
                            if i not in self.mosseEseguite:
                                t = 0
                                tnop = 1
                                break
                else:
                    if spazio['defender'][timer] <= 0:
                        # se ci sono mosse asincrone noop me le deve far terminare
                        t = 0.5
                        # verifico che tutte le mosse sincrone (SCALA TEMPO) siano state usate
                        for i in range(mAgentSinc):
                            # se almeno 1 non usata t = 0
                            if i not in self.mosseEseguite:
                                t = 0
                                tnop = 1
                                break """
                # wait
                if action == timer:
                    t = 0.5
                elif action == timer+1:
                    t = 0

        # se tnop è 1 vuol dire che è stata scelta nop e nop scala 0.5 alle mosse asincrone
        # per forza ha finito le mosse
        # ma non deve alterarmi il timer in alcun modo
        # if tnop == 0:
        if agent == 'attacker':
            spazio['defender'][timer] -= round(t,2)
        else:
            spazio['defender'][timer] += round(t,2)
        #----------------------------------------------------------------------------
        self.aggiornaMosseAsincrone(round(t,2),agente,action,mAgentSinc)
        # perche lamossa noop col numero combacia alla posizione del timer

        #lastTimer = round(spazio['defender'][timer],2)
        #----------------------------------------------------------------------------
        return t


    def reward(self,azione,n_azioni):
        pass
    

    def reset(self):
        self.mosseAsincroneRunning = []
        self.mosseEseguite = []


    def aggiornaMosseAsincrone(self,tot,agente,action,mAgentSinc):
        # Questo mi servirebbe a far scattare il tempo delle mosse asincrone
        # calcolo anche il delta della mossa del difensore + dell'attaccante
        print('Mosse Asincrone in Running PRIMA della mossa:',self.mosseAsincroneRunning)    
        print('tot:',tot)
        
        # lA LISTA RIMOZIONI la utilizzo per rimuovere tutte quelle azioni asincrone che vengono eseguite
        # non le elimino direttmente perche togliendo elementi dalla lista mentre la eseguo smonto 
        # l'ordine degli elementi rispetto l'indice
        listaRimozioni = []
        for i in self.mosseAsincroneRunning:
            print(i)
            print('Tempo Attesa:', i[0].mossa.waiting_time)
            print('Tempo Attuazione:', i[0].mossa.execution_time)
            # richiama il metodo dell'agente asincrono per aggiornare il tempo sulla mossa ed eventualmente applicarla
            val = i[0].stepSuccessivo(tot,i[1],mAgentSinc)
            if val :
                listaRimozioni.append(i)

        # rimuovo azoni asincrone eseguite
        for i in listaRimozioni:
            i[0].mossa.waiting_time = i[0].mossa.execution_time
            self.mosseAsincroneRunning.remove(i)
            self.mosseEseguite.append(i[1])
        listaRimozioni = []


        #La metto qui perche altrimenti anche quelle appena create mi subiscono il delta del difensore
        # del turno prima
        if agente != 0:
            self.mosseAsincroneRunning.append((agente,action))

        print('Mosse Asincrone in Running DOPO la mossa:',self.mosseAsincroneRunning)
        for i in self.mosseAsincroneRunning:
            print('Tempo Attesa:', i[0].mossa.waiting_time)
            print('Tempo Attuazione:', i[0].mossa.execution_time)