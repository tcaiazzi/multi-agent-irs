import json
import os
import sys

import numpy as np
from matplotlib import pyplot as plt


def visualizza_reward_mosse():
    dati = ''
    #with open(pathCompleto, "r") as file:
    with open("fileGrafici/reward_mosse.txt", "r") as file:
        dati = file.read()
    dati_dict = json.loads(dati)
    
    #print(dati_dict)

    a = dati_dict['attacker']
    b = dati_dict['defender']



    # insieme di 2 e 3
    app = dati_dict['attacker']
    bpp = dati_dict['defender']
    """ print('APP:',app)
    print('BPP:',bpp) """

    yA = []
    yB = []

    # reward per ogni partita
    """ for i in range(len(app)) :
        yA.append(app[i][1])
        yB.append(bpp[i][1])
    #print('YA:',yA)
    #print('YB:',yB)
    plt.figure()
    plt.title('ADDESTRAMENTO/EVALUATE')
    plt.ylabel('reward')
    plt.xlabel('t')
    #plt.xlabel('numero mosse per partita')
    plt.plot(np.arange(len(yA)),yA)
    plt.plot(np.arange(len(yB)),yB)
    
    plt.legend(['attacker','defender']) """


    # reward per epoca
    app = dati_dict['attacker']
    bpp = dati_dict['defender']
    """ print('APP:',app)
    print('BPP:',bpp) """

    yA = []
    yB = []
    tempoAtt = []
    tempoDiff = []
    
    aPPEND = 0
    bPPEND = 0
    count = 0
    sommaTempoAtt = 0
    sommaTempoDiff = 0

    for i in range(len(app)):
        aPPEND+=app[i][1]
        bPPEND+=bpp[i][1]
        count +=1

        sommaTempoAtt = app[i][2]
        sommaTempoDiff = bpp[i][2]

        if count == 10:
            count = 0
            #print(i)
            #print(c/10)
            yA.append(aPPEND/10)
            yB.append(bPPEND/10)
            aPPEND = 0
            bPPEND = 0
            tempoAtt.append(sommaTempoAtt)
            tempoDiff.append(sommaTempoDiff)

    """ print('YA:',yA)
    print('YB:',yB) """
    plt.figure()
    plt.title('reward per epoca')
    plt.ylabel('reward')
    plt.xlabel('epoche')
    plt.plot(np.arange(len(yA)),yA)
    plt.plot(np.arange(len(yB)),yB)
    ra = [0 for i in range(len(yA))]
    rb = [-0.1 for i in range(len(yA))]
    plt.plot(np.arange(len(yA)),ra)
    plt.plot(np.arange(len(yA)),rb)
    plt.legend(['attacker','defender','reward ottimo attaccante','reward ottimo difensore'])

    """  plt.figure()
    plt.plot(tempoAtt,yA)
    plt.plot(tempoDiff,yB)
    xl=600
    ra = [0 for i in range(xl)]
    rb = [-0.1 for i in range(xl)]
    plt.plot(np.arange(xl),ra)
    plt.plot(np.arange(xl),rb)
    plt.xlabel('secondi')
    plt.ylabel('reward')
    plt.ylim(-3.5,0)
    plt.xlim(0,600)
    plt.legend(['reward-tempo Attaccante','reward-tempo Difensore']) """

# Crea il grafico
    fig, ax = plt.subplots()

    # Plotta i dati
    ax.plot(tempoAtt,yB)
    ax.plot(tempoDiff,yB)
    ax.set_xlabel('secondi')
   
    ax2 = ax.twiny()
    ax2.plot(tempoAtt,yB)
    ax2.set_xticks([0,tempoAtt[int(len(tempoAtt)/4)],tempoAtt[int(len(tempoAtt)/2)],tempoAtt[int(3*(len(tempoAtt))/4)],tempoAtt[-1]],[0,int(len(yB)/4),int(len(yB)/2),int(3*(len(yB)/4)),len(yB)])
    
    ax2.plot(tempoDiff,yB)
    ax2.set_xticks([0,tempoDiff[int(len(tempoDiff)/4)],tempoDiff[int(len(tempoDiff)/2)],tempoDiff[int(3*(len(tempoDiff))/4)],tempoDiff[-1]],[0,int(len(yB)/4),int(len(yB)/2),int(3*(len(yB)/4)),len(yB)])
    ax2.set_xlabel('epoche')
    
    plt.legend()
    plt.savefig(os.path.join("fileGrafici", "plot1.pdf"), format='pdf')



    # il numero di mosse fatte nel tempo, per partita
    """ y = []
    for i in a :
        y.append(i[0])
    plt.figure()
    plt.title('MOSSE ATT+DIF fatte per ogni partita')
    plt.ylabel('n mosse')
    plt.xlabel('partite')
    plt.plot(np.arange(len(y)),y) """




    # reward rispetto al numero di mosse fatte dall'attaccante
    """ x = []
    y = []
    a.sort()
    for i in a :
        x.append(i[0])
        y.append(i[1])
    #print(len(x))
    #print(len(y))
    plt.figure()
    plt.title('REWARD attaccante rispetto il N.MOSSE')
    plt.ylabel('reward attaccante')
    plt.xlabel('numero mosse per partita')
    plt.plot(x,y) """
    

    # Grafico 3
    # reward rispetto al numero di mosse fatte dal difensore
    """ x = []
    y = []
    b.sort()
    for i in b :
        x.append(i[0])
        y.append(i[1])
    #print(len(x))
    #print(len(y)) 
    plt.figure()
    plt.title('')
    plt.title('REWARD difensore rispetto il N.MOSSE')
    plt.xlabel('numero mosse per partita')
    plt.plot(x,y) """

    # plt.savefig(os.path.join("fileGrafici", "plot2.pdf"), format='pdf')

if __name__ == '__main__':
    visualizza_reward_mosse()

