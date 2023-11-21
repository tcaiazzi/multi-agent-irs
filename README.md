# IRS: Intrusion Response System
NOTA: Multithread non ancora utilizzato/sfruttato

python3 ./training/run_rspXXX.py 
(lui usa algoritmiTraining per l'implementazione dei modelli e visualizzazione per vedere i grafici di training )
	invoca rsp.py che si avvale di prePost per il training
	
	|run_rspDQN--->
	|run_rspApexDQN--->
	|run_rspImpala--->
	|run_rspPG--->
	|run_rspPPO--->
		|algoritmiTraining--->
		|rsp--->
			|prePost
		|visualizzzazione--->


python3 ./evaluate/evaluationXXX.py 
(lui usa algoritmi di training per ricaricare il checkpoint treinato)
	invoca visualizzazione per vedere come si comporta il modello
	
	|evaluationModel--->
		|algoritmiTraining--->
		|visualizzazione--->

	
NOTA: salvare a mano i differenti file da confrontare dei diversi algoritmi
lanciare fileGrafici/visualizzazioneAll.py 
	per vedere tutti i dati a confronto
