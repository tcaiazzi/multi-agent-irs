import threading
import subprocess
from matplotlib import pyplot as plt
import numpy as np
import json

def visualizza_reward_mosse():
    dati = ''
    with open("/home/matteo/Documenti/GitHub/tesiMagistrale/reward_mosse.txt", "r") as file:
        dati = file.read()
    dati_dict = json.loads(dati)
    print(dati_dict)

    # Grafico 1
    # il numero di mosse fatte nel tempo, per partita
    a = dati_dict['attaccante']
    x = []
    y = []
    for i in a :
        x.append(i[0])
    plt.figure()
    plt.ylabel('n mosse')
    plt.xlabel('t')
    plt.plot(np.arange(len(x)),x)

    # Grafico 2
    # reward rispetto al numero di mosse fatte dall'attaccante
    x = []
    y = []
    a.sort()
    for i in a :
        x.append(i[0])
        y.append(i[1])
    print(len(x))
    print(len(y))
    plt.figure()
    plt.title('PG campioni:'+str(len(x)))
    plt.ylabel('reward attaccante')
    plt.xlabel('numero mosse per partita')
    plt.plot(x,y)

    # Grafico 3
    # reward rispetto al numero di mosse fatte dal difensore
    x = []
    y = []
    b = dati_dict['difensore']
    b.sort()
    for i in b :
        x.append(i[0])
        y.append(i[1])
    print(len(x))
    print(len(y))
    plt.figure()
    plt.title('PG campioni:'+str(len(x)))
    plt.ylabel('reward difensore')
    plt.xlabel('numero mosse per partita')
    plt.plot(x,y)

    # Grafico 4
    # insieme di 2 e 3
    xA = []
    yA = []
    xB = []
    yB = []
    a.sort()
    b.sort()
    for i in range(len(a)) :
        xA.append(a[i][1])
        yA.append(a[i][0])
        xB.append(b[i][1])
        yB.append(b[i][0])
    print(len(xA))
    print(len(xB))
    plt.figure()
    plt.title('PG campioni:'+str(len(xA)))
    plt.ylabel('reward')
    plt.xlabel('numero mosse per partita')
    plt.plot(yA,xA)
    plt.plot(yB,xB)
    plt.legend(['attaccante','difensore'])

    plt.show()

def visualizza_curva_partita():
    dati = ''
    with open("/home/matteo/Documenti/GitHub/tesiMagistrale/curva_partita.txt", "r") as file:
        dati = file.read()
    dati_dict = json.loads(dati)

    a = dati_dict['attaccante']
    b = dati_dict['difensore']
    print(len(a))
    print(len(b))

    appA = []
    appB = []
    count = 0
    for i in range(len(a)):
        if a[i][0] != 1:
            appA.append(a[i][1])
            appB.append(b[i][1]) 
        else:
            plt.figure()
            plt.title('Alg PG Partita '+str(count)+' attaccante/difensore')
            plt.xlabel('ennesima mossa')
            plt.ylabel('reward totale')
            plt.plot(np.arange(len(appB)),appB)
            plt.plot(np.arange(len(appA)),appA)
            plt.legend(['difensore','attaccante'],title='legend')
            count +=1
            appA = []
            appB = []
            appA.append(a[i][1])
            appB.append(b[i][1])
    plt.show()


def programma1():
    try : 
        # Lancia RUN_RSP.py
        subprocess.run(["python3", '/home/matteo/Documenti/GitHub/tesiMagistrale/run_rsp.py'])

        # multithread ->
        #               lancia run_rsp->
        #                               che lancia rsp->
        #                                               che usa prePost
        #               alla fine lancia visualizza_reward_mosse

        visualizza_reward_mosse()
        #visualizza_curva_partita()

    except Exception as e :
        print(e)


t1 = threading.Thread(target=programma1)
#t2 = threading.Thread(target=programma2)

# Avviare i thread
t1.start()
#t2.start()

# Attendere che entrambi i thread terminino
#t1.join()
#t2.join()
