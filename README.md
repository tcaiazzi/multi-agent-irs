# IRS: Intrusion Response System

INSTALLARE
requirements.txt

CONF.TXT NON UTILIZZATO

COMANDI:
 ./start ALGORITMO TrainingIteration
 ./start ALGORITMO -e CheckPoint > log.txt 

LEGENDA:
 - ALGORITMI: DQN, ApexDQN, Impala, PG, PPO
 - TrainingIteration: int



OUTPUT
/fileGrafici/reward_mosse.txt


./visualizzazione.py (UTILIZZATO PER TEST SUL PC PERSONALE PER RISCONTRO GRAFICO)
/fileGrafici/visualizzaAll.py (NON UTILIZZATO)


./evaluate/*
file per l'evaluation dei checkpoint