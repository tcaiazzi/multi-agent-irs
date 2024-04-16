from agents.Agent import Agent

class Attacker(Agent):

    def __init__(self):
        super().__init__()

    # Se l'attaccante trova il Timer <=0 non puo eseguire e per ora facciamo che ogni azione vale 1
    def preCondizioni(self, spazio, legal_moves, mosse, agent, timer):
        mAttS = mosse[agent]['sync']
        mAttA = mosse[agent]['async']

        return super().preCondizioni(spazio, legal_moves, mAttS, mAttA, agent, timer)

    def postCondizioni(self, action, spazio, agent, mosse, timer):
        mAttS = mosse['attacker']['sync']
        mAttA = mosse['attacker']['async']
        mAttT = mAttS + mAttA

        return super().postCondizioni(action, spazio, agent, mosse, timer, mAttS)

    def reward(self, azione, n_azioni):
        return (azione - (n_azioni - 2)) / (n_azioni - 2)

    def reset(self):
        super().reset()
        self.asincronaAzione.reset()
        # self.sincronaAzione.reset()
