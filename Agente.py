
class Agente():
    def __init__(self):
        self.T1 = 0.33
        self.T2 = 0.66
        self.mosseAsincroneRunning = []

        self.wt = 0.16
        self.wc = 0.34
        self.wi = 0.50
        self.tMax = 100
        self.cMax = 100

    def reward(self,azione):
        calcolo = -(-self.wt*(azione[0]/self.tMax)-self.wc*(azione[1]/self.cMax)-self.wi*azione[2])
        #calcolo = REWARD_MAP[agent][action][0]+REWARD_MAP[agent][action][1]+REWARD_MAP[agent][action][2]
        print('Reward:',calcolo)
        return calcolo
    
    def reset(self):
        self.mosseAsincroneRunning = []

    def aggiornaMosseAsincrone(self,tot,agente,action):
        # Questo mi servirebbe a far scattare il tempo delle mosse asincrone
        # calcolo anche il delta della mossa del difensore + dell'attaccante
        for x,i in self.mosseAsincroneRunning:
            x.stepSuccessivo(tot,self.mosseAsincroneRunning,(x,i))

        #La metto qui perche altrimenti anche quelle appena create mi subiscono il delta del difensore
        # del turno prima
        if agente != 0:
            self.mosseAsincroneRunning.append((agente,action))