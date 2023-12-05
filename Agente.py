
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