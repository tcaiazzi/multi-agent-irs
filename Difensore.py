from Agente import Agente


class Difensore(Agente):
    def __init__(self):
        super().__init__()

    # Il difensore invece può eseguire una mossa solo nel caso incui il Timer è <=0 ed ogni mossa vale 1
    def preCondizioni(self,spazio,legal_moves,Timer):
        # Generate alert
        if ((spazio['difensore'][14] >= self.T1 or spazio['difensore'][15] >= self.T1 or spazio['difensore'][16] >= self.T1 or
            spazio['difensore'][17] >= self.T1 or spazio['difensore'][18] >= self.T1 or spazio['difensore'][19] >= self.T1 or 
            spazio['difensore'][20] >= self.T1) and spazio['difensore'][3] == 0 and spazio['difensore'][6] == 1 and Timer <=0):
            legal_moves[0] = 1
        else:
            legal_moves[0] = 0
        # FirewallActivation
        # preso dal paper
        if ((spazio['difensore'][14] >= self.T1 or spazio['difensore'][15] >= self.T1 or spazio['difensore'][16] >= self.T1 or 
            spazio['difensore'][17] >= self.T1 or spazio['difensore'][18] >= self.T1 or spazio['difensore'][19] >= self.T1 or 
            spazio['difensore'][20] >= self.T1 and Timer <=0) 
            and spazio['difensore'][0] == 0 and spazio['difensore'][6] == 1 and spazio['difensore'][7] == 0 and spazio['difensore'][5] > 0):
            legal_moves[1] = 1
        else:
            legal_moves[1] = 0
        # BlockSourceIp
        # preso dal paper
        if (spazio['difensore'][14] >= self.T2 and spazio['difensore'][0] == 1 and
            spazio['difensore'][6] == 1 and spazio['difensore'][1] == 0 and spazio['difensore'][3] == 1 and
            spazio['difensore'][5] > 1 and spazio['difensore'][7] == 0 and Timer <=0) : 
            legal_moves[2] = 1
        else:
            legal_moves[2] = 0
        # UnblockSourceIp
        if (spazio['difensore'][14] < self.T2 and spazio['difensore'][0] == 1  and
            spazio['difensore'][6] == 1 and spazio['difensore'][1] == 1  and
            spazio['difensore'][5] > 1 and Timer <=0) :
            legal_moves[3] = 1
        else:
            legal_moves[3] = 0
        # FlowRateLimit
        # preso dal paper
        if (spazio['difensore'][14] >= self.T1 and spazio['difensore'][0] ==1 and spazio['difensore'][3] == 1 and
            spazio['difensore'][6] == 1 and spazio['difensore'][2] == 0 and spazio['difensore'][5] > 0 and
            spazio['difensore'][1] == 0 and spazio['difensore'][7] == 0 and Timer <=0) :
            legal_moves[4] = 1
        else:
            legal_moves[4] = 0
        # UnlimitFlowRate
        if (spazio['difensore'][14] < self.T1 and spazio['difensore'][0] ==1 and
            spazio['difensore'][6] == 1 and spazio['difensore'][2] == 1 and spazio['difensore'][5] > 0 and Timer <=0):
            legal_moves[5] = 1
        else:
            legal_moves[5] = 0
        # RedirectToHoneypot
        if (spazio['difensore'][4] == 0 and
            (spazio['difensore'][15] >= self.T1 or spazio['difensore'][16] >= self.T1 or spazio['difensore'][17] >= self.T1 or 
             spazio['difensore'][18] >= self.T1 or spazio['difensore'][19] >= self.T1 or spazio['difensore'][20] >= self.T1) 
            and spazio['difensore'][0] == 1 and  spazio['difensore'][7] == 0 and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[6] = 1
        else:
            legal_moves[6] = 0
        # UnHoneypot
        if (spazio['difensore'][4] == 1 and 
            (spazio['difensore'][15] < self.T1 or spazio['difensore'][16] < self.T1 or spazio['difensore'][17] < self.T1 or 
             spazio['difensore'][18] < self.T1 or spazio['difensore'][19] < self.T1 or spazio['difensore'][20] < self.T1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 0 and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[7] = 1
        else:
            legal_moves[7] = 0
        # IncreaseLog
        if (spazio['difensore'][5] < 5 and 
            (spazio['difensore'][14] >= self.T1 or spazio['difensore'][15] >= self.T1 or spazio['difensore'][16] >= self.T1 or 
             spazio['difensore'][17] >= self.T1 or spazio['difensore'][18] >= self.T1 or spazio['difensore'][19] >= self.T1 or 
             spazio['difensore'][20] >= self.T1) and spazio['difensore'][6] == 1 and Timer <=0) : 
            legal_moves[8] = 1
        else:
            legal_moves[8] = 0
        # DecreaseLog
        if (spazio['difensore'][5] > 0 and 
            (spazio['difensore'][14] < self.T2 or spazio['difensore'][15] < self.T2 or spazio['difensore'][16] < self.T2 or 
             spazio['difensore'][17] < self.T2 or spazio['difensore'][18] < self.T2 or spazio['difensore'][19] < self.T2 or 
             spazio['difensore'][20] < self.T2) and spazio['difensore'][6] == 1 and Timer <=0) : 
            legal_moves[9] = 1
        else:
            legal_moves[9] = 0
        # QuarantineHost
        if (spazio['difensore'][7] == 0 and 
            (spazio['difensore'][14] > self.T2 or spazio['difensore'][15] > self.T2 or spazio['difensore'][16] > self.T2 or 
             spazio['difensore'][17] > self.T2 or spazio['difensore'][18] > self.T2 or spazio['difensore'][19] > self.T2 or 
             spazio['difensore'][20] > self.T2 ) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][3] == 1 and spazio['difensore'][5] >= 3 
            and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[10] = 1
        else:
            legal_moves[10] = 0    
        # UnQuarantineHost    
        if (spazio['difensore'][7] == 1 and 
            (spazio['difensore'][14] < self.T2 or spazio['difensore'][15] < self.T2 or spazio['difensore'][16] < self.T2 or 
             spazio['difensore'][17] < self.T2 or spazio['difensore'][18] < self.T2 or spazio['difensore'][19] < self.T2 or 
             spazio['difensore'][20] < self.T2) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][5] > 3 and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[11] = 1
        else:
            legal_moves[11] = 0
        # ManualResolution 
        if (spazio['difensore'][11] == 0 and 
            (spazio['difensore'][15] == 1 or spazio['difensore'][16] == 1 or spazio['difensore'][17] == 1 or 
             spazio['difensore'][18] == 1 or spazio['difensore'][19] == 1 or spazio['difensore'][20] == 1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 1 and spazio['difensore'][8] == 1 
            and spazio['difensore'][10] == 1 and spazio['difensore'][3] == 1 and spazio['difensore'][9] == 1 
            and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[12] = 1
        else:
            legal_moves[12] = 0
        # SystemReboot
        if (spazio['difensore'][11] == 0 and spazio['difensore'][6] == 1 and 
            (spazio['difensore'][14] == 1 or spazio['difensore'][15] == 1 or spazio['difensore'][16] == 1 or spazio['difensore'][17] == 1 or 
             spazio['difensore'][18] == 1 or spazio['difensore'][19] == 1 or spazio['difensore'][20] == 1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 1 
            and spazio['difensore'][3] == 1 and Timer <=0) :
            legal_moves[13] = 1
        else:
            legal_moves[13] = 0
        # SystemShutdown
        if (spazio['difensore'][11] == 0 and spazio['difensore'][6] == 1 and 
            (spazio['difensore'][14] == 1 or spazio['difensore'][15] == 1 or spazio['difensore'][16] == 1 or spazio['difensore'][17] == 1 or 
             spazio['difensore'][18] == 1 or spazio['difensore'][19] == 1 or spazio['difensore'][20] == 1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 1 
            and spazio['difensore'][3] == 1 and Timer <=0) :
            legal_moves[14] = 1
        else:
            legal_moves[14] = 0
        # SystemStart
        if spazio['difensore'][6] == 0 :
            legal_moves[15] = 1
        else:
            legal_moves[15] = 0
        # BackupHost
        if (spazio['difensore'][6] == 1 and spazio['difensore'][9] == 0 and spazio['difensore'][7] == 0 and
            spazio['difensore'][3] == 1 and spazio['difensore'][5] > 1 and Timer <=0 and
            (spazio['difensore'][15] > self.T1 or spazio['difensore'][16] > self.T1 or spazio['difensore'][17] > self.T1 or 
             spazio['difensore'][18] > self.T1 or spazio['difensore'][19] > self.T1 or spazio['difensore'][20] > self.T1)):
            legal_moves[16] = 1
        else:
            legal_moves[16] = 0
        # SoftwareUpdate
        # detto dal prof: deve aver fatto backup
        if (spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and spazio['difensore'][9] == 1 and Timer <=0 and 
            (spazio['difensore'][15] > self.T1 or spazio['difensore'][16] > self.T1 or spazio['difensore'][17] > self.T1 or 
             spazio['difensore'][18] > self.T1 or spazio['difensore'][19] > self.T1 or spazio['difensore'][20] > self.T1)) :
            legal_moves[17] = 1
        else:
            legal_moves[17] = 0
        # noOp (altrimenti se nulla è selezionbile sceglie a caso)
        # se nessuna mossa è selezionabile allora noop
        """ noOp = True
        for z in range(18):
            if (legal_moves[z] == 1):
                noOp = False
        if noOp: """
        # Ora abbiamo deciso di renderla ammissibile ad ogni stato così che possa terminare anche 
        # quando non ho piu mosse che mi portano sullo stato target (finale)
        legal_moves[18] = 1