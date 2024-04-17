# qui ho implementato la stessa idea delle mosse sincrone

class AsyncMove:

    def __init__(self, execution_time: float = 1.0, waiting_time: float = 1.0):
        self.execution_time = execution_time
        self.waiting_time = waiting_time

    def verify_preconditions(self, spazio, legal_moves, pos, agent, mAttS, mosseEseguite, running):

        # mossa asincrona non in esecuzione...
        if not (running):
            if agent == 'attacker':
                # mossa asincrona mai eseguita...
                if (pos not in mosseEseguite):
                    # for i in range(mAttS,len(legal_moves)):
                    # classica pre condizione di abilitazione...
                    for j in range(pos + 1):
                        # print(f'pos {pos} j {j}')
                        if spazio['defender'][j] == 0:
                            # print(f'LEGAL PRIMA {legal_moves}')
                            legal_moves[pos] = 1
                            # print(f'LEGAL DOPO {legal_moves}')
                            break
                        else:
                            legal_moves[pos] = 0
                # mossa asinc giaà eseguita...
                else:
                    legal_moves[pos] = 0
            else:
                # mossa asincrona mai eseguita...
                if (pos not in mosseEseguite):
                    # for i in range(mAttS,len(legal_moves)):
                    # classica pre condizione di abilitazione...
                    for j in range(pos + 1):
                        # print(f'pos {pos} j {j}')
                        if spazio['defender'][j] == 1:
                            # print(f'LEGAL PRIMA {legal_moves}')
                            legal_moves[pos] = 1
                            # print(f'LEGAL DOPO {legal_moves}')
                            break
                        else:
                            legal_moves[pos] = 0
                # mossa asinc giaà eseguita...
                else:
                    legal_moves[pos] = 0

        # mossa asincrona in esecuzione
        else:
            legal_moves[pos] = 0

    def verify_postconditions(self, spazio, agent, action, mAttS):
        # soglia = round(random.random(),2)

        if agent == 'attacker':
            # prob = round(random.random(),2)
            # if prob <= soglia :
            for i in range((action + 1)):
                spazio['defender'][i] = 1
        else:
            # prob = round(random.random(),2)
            # if prob <= soglia :
            for i in range((action + 1)):
                spazio['defender'][i] = 0

    def reset(self):
        self.waiting_time = self.execution_time
