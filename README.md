# tesiMagistrale

lanciare python3 run_rsp.py (lui usa algoritmiTraining per l'implementazione dei modelli e visualizzazione per vedere i grafici di training )
	invoca rsp.py che si avvale di prePost per il training
	
	|run_rsp--->
		|algoritmiTraining--->
		|rsp--->
			|prePost
		|visualizzzazione--->


lanciare python3 evaluationModel.py (lui usa algoritmi di training per ricaricare il checkpoint treinato)
	invoca visualizzazione per vedere come si comporta il modello
	
	|evaluationModel--->
		|algoritmiTraining--->
		|visualizzazione--->

	
NOTA: salvare a mano i differenti file da confrontare dei diversi algoritmi
lanciare fileGrafici/visualizzazioneAll.py 
	per vedere tutti i dati a confronto
