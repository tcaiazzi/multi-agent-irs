import json
import matplotlib.pyplot as plt
import numpy as np

dati_dict = ''
with open("/home/matteo/Documenti/GitHub/tesiMagistrale/fileGrafici/DQN_train_reward_mosse.txt", "r") as file:
        dati = file.read()
dati_dict = json.loads(dati)

attaccanteDQN = dati_dict['attaccante']
difensoreDQN = dati_dict['difensore']

yA = []
yB = []
for i in range(len(attaccanteDQN)) :
        yA.append(attaccanteDQN[i][1])
        yB.append(difensoreDQN[i][1])

plt.plot(np.arange(len(yA)),yA)
plt.plot(np.arange(len(yB)),yB)


dati_dict = ''
with open("/home/matteo/Documenti/GitHub/tesiMagistrale/fileGrafici/ApexDQN_train_reward_mosse.txt", "r") as file:
        dati = file.read()
dati_dict = json.loads(dati)

attaccanteApexDQN = dati_dict['attaccante']
difensoreApexDQN = dati_dict['difensore']

yA = []
yB = []
for i in range(len(attaccanteApexDQN)) :
        yA.append(attaccanteApexDQN[i][1])
        yB.append(difensoreApexDQN[i][1])

plt.plot(np.arange(len(yA)),yA)
plt.plot(np.arange(len(yB)),yB)


dati_dict = ''
with open("/home/matteo/Documenti/GitHub/tesiMagistrale/fileGrafici/Impala_train_reward_mosse.txt", "r") as file:
        dati = file.read()
dati_dict = json.loads(dati)

attaccanteImpala = dati_dict['attaccante']
difensoreImpala = dati_dict['difensore']

yA = []
yB = []
for i in range(len(attaccanteImpala)) :
        yA.append(attaccanteImpala[i][1])
        yB.append(difensoreImpala[i][1])

plt.plot(np.arange(len(yA)),yA)
plt.plot(np.arange(len(yB)),yB)


dati_dict = ''
with open("/home/matteo/Documenti/GitHub/tesiMagistrale/fileGrafici/PG_train_reward_mosse.txt", "r") as file:
        dati = file.read()
dati_dict = json.loads(dati)

attaccantePG = dati_dict['attaccante']
difensorePG = dati_dict['difensore']

yA = []
yB = []
for i in range(len(attaccantePG)) :
        yA.append(attaccantePG[i][1])
        yB.append(difensorePG[i][1])

plt.plot(np.arange(len(yA)),yA)
plt.plot(np.arange(len(yB)),yB)


dati_dict = ''
with open("/home/matteo/Documenti/GitHub/tesiMagistrale/fileGrafici/PPO_train_reward_mosse.txt", "r") as file:
        dati = file.read()
dati_dict = json.loads(dati)

attaccantePPO = dati_dict['attaccante']
difensorePPO = dati_dict['difensore']

yA = []
yB = []
for i in range(len(attaccantePPO)) :
        yA.append(attaccantePPO[i][1])
        yB.append(difensorePPO[i][1])


plt.plot(np.arange(len(yA)),yA)
plt.plot(np.arange(len(yB)),yB)
plt.legend(['attaccanteDQN','difensoreDQN','attaccanteApexDQN','difensoreApexDQN','attaccanteImpala','difensoreImpala','attaccantePG','difensorePG','attacantePPO','difensorePPO'])

plt.show()