from Agente import Agente
from azioni.GenerateAlert import GenerateAlert 
from azioni.FirewallActivation import FirewallActivation
from azioni.BlockIp import BlockIp 
from azioni.UnBlockIp import UnBlockIp
from azioni.LimitFlowRate import LimitFlowRate
from azioni.UnLimitFlowRate import UnLimitFlowRate
from azioni.RedirectHoneypot import RedirectHoneypot
from azioni.UnRedirectHoneypot import UnRedirectHoneypot
from azioni.IncreaseLog import IncreaseLog
from azioni.DecreaseLog import DecreaseLog
from azioni.Quarantine import Quarantine
from azioni.UnQuarantine import UnQuarantine
from azioni.ManualResolution import ManualResolution
from azioni.Reboot import Reboot
from azioni.ShutDown import ShutDown
from azioni.Start import Start
from azioni.Backup import Backup
from azioni.Update import Update

import random


class Difensore(Agente):
    def __init__(self):
        super().__init__()
        self.GenerateAlertAzione = GenerateAlert()
        self.FirewallActivationAzione = FirewallActivation()
        self.BlockIpAzione = BlockIp()
        self.UnBlockIpAzione = UnBlockIp()
        self.LimitFlowRateAzione = LimitFlowRate()
        self.UnLimitFlowRateAzione = UnLimitFlowRate()
        self.RedirectHoneypotAzione = RedirectHoneypot()
        self.UnRedirectHoneypotAzione = UnRedirectHoneypot()
        self.IncreaseLogAzione = IncreaseLog()
        self.DecreaseLogAzione = DecreaseLog()
        self.QuarantineAzione = Quarantine()
        self.UnQuarantineAzione = UnQuarantine()
        self.ManualResolutionAzione = ManualResolution()
        self.RebootAzione = Reboot()
        self.ShutDownAzione = ShutDown()
        self.StartAzione = Start()
        self.BackupAzione = Backup()
        self.UpdateAzione = Update()

    # Il difensore invece può eseguire una mossa solo nel caso incui il Timer è <=0 ed ogni mossa vale 1
    def preCondizioni(self,spazio,legal_moves,Timer):
        # Generate alert
        self.GenerateAlertAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if ((spazio['difensore'][14] >= self.T1 or spazio['difensore'][15] >= self.T1 or spazio['difensore'][16] >= self.T1 or
            spazio['difensore'][17] >= self.T1 or spazio['difensore'][18] >= self.T1 or spazio['difensore'][19] >= self.T1 or 
            spazio['difensore'][20] >= self.T1) and spazio['difensore'][3] == 0 and spazio['difensore'][6] == 1 and Timer <=0):
            legal_moves[0] = 1
        else:
            legal_moves[0] = 0 """
        # FirewallActivation
        self.FirewallActivationAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        # preso dal paper
        """ if ((spazio['difensore'][14] >= self.T1 or spazio['difensore'][15] >= self.T1 or spazio['difensore'][16] >= self.T1 or 
            spazio['difensore'][17] >= self.T1 or spazio['difensore'][18] >= self.T1 or spazio['difensore'][19] >= self.T1 or 
            spazio['difensore'][20] >= self.T1 and Timer <=0) 
            and spazio['difensore'][0] == 0 and spazio['difensore'][6] == 1 and spazio['difensore'][7] == 0 and spazio['difensore'][5] > 0):
            legal_moves[1] = 1
        else:
            legal_moves[1] = 0 """
        # BlockSourceIp
        # preso dal paper
        self.BlockIpAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][14] >= self.T2 and spazio['difensore'][0] == 1 and
            spazio['difensore'][6] == 1 and spazio['difensore'][1] == 0 and spazio['difensore'][3] == 1 and
            spazio['difensore'][5] > 1 and spazio['difensore'][7] == 0 and Timer <=0) : 
            legal_moves[2] = 1
        else:
            legal_moves[2] = 0 """
        # UnblockSourceIp
        self.UnBlockIpAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][14] < self.T2 and spazio['difensore'][0] == 1  and
            spazio['difensore'][6] == 1 and spazio['difensore'][1] == 1  and
            spazio['difensore'][5] > 1 and Timer <=0) :
            legal_moves[3] = 1
        else:
            legal_moves[3] = 0 """
        # FlowRateLimit
        # preso dal paper
        self.LimitFlowRateAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][14] >= self.T1 and spazio['difensore'][0] ==1 and spazio['difensore'][3] == 1 and
            spazio['difensore'][6] == 1 and spazio['difensore'][2] == 0 and spazio['difensore'][5] > 0 and
            spazio['difensore'][1] == 0 and spazio['difensore'][7] == 0 and Timer <=0) :
            legal_moves[4] = 1
        else:
            legal_moves[4] = 0 """
        # UnlimitFlowRate
        self.UnLimitFlowRateAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][14] < self.T1 and spazio['difensore'][0] ==1 and
            spazio['difensore'][6] == 1 and spazio['difensore'][2] == 1 and spazio['difensore'][5] > 0 and Timer <=0):
            legal_moves[5] = 1
        else:
            legal_moves[5] = 0 """
        # RedirectToHoneypot
        self.RedirectHoneypotAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][4] == 0 and
            (spazio['difensore'][15] >= self.T1 or spazio['difensore'][16] >= self.T1 or spazio['difensore'][17] >= self.T1 or 
             spazio['difensore'][18] >= self.T1 or spazio['difensore'][19] >= self.T1 or spazio['difensore'][20] >= self.T1) 
            and spazio['difensore'][0] == 1 and  spazio['difensore'][7] == 0 and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[6] = 1
        else:
            legal_moves[6] = 0 """
        # UnHoneypot
        self.UnRedirectHoneypotAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][4] == 1 and 
            (spazio['difensore'][15] < self.T1 or spazio['difensore'][16] < self.T1 or spazio['difensore'][17] < self.T1 or 
             spazio['difensore'][18] < self.T1 or spazio['difensore'][19] < self.T1 or spazio['difensore'][20] < self.T1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 0 and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[7] = 1
        else:
            legal_moves[7] = 0 """
        # IncreaseLog
        self.IncreaseLogAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][5] < 5 and 
            (spazio['difensore'][14] >= self.T1 or spazio['difensore'][15] >= self.T1 or spazio['difensore'][16] >= self.T1 or 
             spazio['difensore'][17] >= self.T1 or spazio['difensore'][18] >= self.T1 or spazio['difensore'][19] >= self.T1 or 
             spazio['difensore'][20] >= self.T1) and spazio['difensore'][6] == 1 and Timer <=0) : 
            legal_moves[8] = 1
        else:
            legal_moves[8] = 0 """
        # DecreaseLog
        self.DecreaseLogAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][5] > 0 and 
            (spazio['difensore'][14] < self.T2 or spazio['difensore'][15] < self.T2 or spazio['difensore'][16] < self.T2 or 
             spazio['difensore'][17] < self.T2 or spazio['difensore'][18] < self.T2 or spazio['difensore'][19] < self.T2 or 
             spazio['difensore'][20] < self.T2) and spazio['difensore'][6] == 1 and Timer <=0) : 
            legal_moves[9] = 1
        else:
            legal_moves[9] = 0 """
        # QuarantineHost
        self.QuarantineAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][7] == 0 and 
            (spazio['difensore'][14] > self.T2 or spazio['difensore'][15] > self.T2 or spazio['difensore'][16] > self.T2 or 
             spazio['difensore'][17] > self.T2 or spazio['difensore'][18] > self.T2 or spazio['difensore'][19] > self.T2 or 
             spazio['difensore'][20] > self.T2 ) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][3] == 1 and spazio['difensore'][5] >= 3 
            and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[10] = 1
        else:
            legal_moves[10] = 0  """   
        # UnQuarantineHost
        self.UnQuarantineAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][7] == 1 and 
            (spazio['difensore'][14] < self.T2 or spazio['difensore'][15] < self.T2 or spazio['difensore'][16] < self.T2 or 
             spazio['difensore'][17] < self.T2 or spazio['difensore'][18] < self.T2 or spazio['difensore'][19] < self.T2 or 
             spazio['difensore'][20] < self.T2) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][5] > 3 and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[11] = 1
        else:
            legal_moves[11] = 0 """
        # ManualResolution 
        self.ManualResolutionAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][11] == 0 and 
            (spazio['difensore'][15] == 1 or spazio['difensore'][16] == 1 or spazio['difensore'][17] == 1 or 
             spazio['difensore'][18] == 1 or spazio['difensore'][19] == 1 or spazio['difensore'][20] == 1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 1 and spazio['difensore'][8] == 1 
            and spazio['difensore'][10] == 1 and spazio['difensore'][3] == 1 and spazio['difensore'][9] == 1 
            and spazio['difensore'][6] == 1 and Timer <=0) :
            legal_moves[12] = 1
        else:
            legal_moves[12] = 0 """
        # SystemReboot
        self.RebootAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][11] == 0 and spazio['difensore'][6] == 1 and 
            (spazio['difensore'][14] == 1 or spazio['difensore'][15] == 1 or spazio['difensore'][16] == 1 or spazio['difensore'][17] == 1 or 
             spazio['difensore'][18] == 1 or spazio['difensore'][19] == 1 or spazio['difensore'][20] == 1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 1 
            and spazio['difensore'][3] == 1 and Timer <=0) :
            legal_moves[13] = 1
        else:
            legal_moves[13] = 0 """
        # SystemShutdown
        self.ShutDownAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][11] == 0 and spazio['difensore'][6] == 1 and 
            (spazio['difensore'][14] == 1 or spazio['difensore'][15] == 1 or spazio['difensore'][16] == 1 or spazio['difensore'][17] == 1 or 
             spazio['difensore'][18] == 1 or spazio['difensore'][19] == 1 or spazio['difensore'][20] == 1) 
            and spazio['difensore'][0] == 1 and spazio['difensore'][7] == 1 
            and spazio['difensore'][3] == 1 and Timer <=0) :
            legal_moves[14] = 1
        else:
            legal_moves[14] = 0 """
        # SystemStart
        self.StartAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if spazio['difensore'][6] == 0 :
            legal_moves[15] = 1
        else:
            legal_moves[15] = 0 """
        # BackupHost
        self.BackupAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][6] == 1 and spazio['difensore'][9] == 0 and spazio['difensore'][7] == 0 and
            spazio['difensore'][3] == 1 and spazio['difensore'][5] > 1 and Timer <=0 and
            (spazio['difensore'][15] > self.T1 or spazio['difensore'][16] > self.T1 or spazio['difensore'][17] > self.T1 or 
             spazio['difensore'][18] > self.T1 or spazio['difensore'][19] > self.T1 or spazio['difensore'][20] > self.T1)):
            legal_moves[16] = 1
        else:
            legal_moves[16] = 0 """
        # SoftwareUpdate
        # detto dal prof: deve aver fatto backup
        self.UpdateAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,Timer)
        """ if (spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0 and spazio['difensore'][9] == 1 and Timer <=0 and 
            (spazio['difensore'][15] > self.T1 or spazio['difensore'][16] > self.T1 or spazio['difensore'][17] > self.T1 or 
             spazio['difensore'][18] > self.T1 or spazio['difensore'][19] > self.T1 or spazio['difensore'][20] > self.T1)) :
            legal_moves[17] = 1
        else:
            legal_moves[17] = 0 """
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




    def postCondizioni(self,action,spazio,agent,Timer):

        # GenerateAlert
        if action == 0 :
            #spazio[agent][3] = 1
            self.GenerateAlertAzione.postCondizione(spazio,agent)
            Timer += 1
        # FirewallActivation
        elif action == 1 :
            #spazio[agent][0] = 1
            self.FirewallActivationAzione.postCondizione(spazio,agent)
            Timer += 1
        # BlockSourceIp
        elif action == 2 :
            """ spazio[agent][1] = 1
            spazio[agent][14] = 0  """
            self.BlockIpAzione.postCondizione(spazio,agent)
            Timer += 1
        # UnblockSourceIp
        elif action == 3 :
            #spazio[agent][1] = 0
            self.UnBlockIpAzione.postCondizione(spazio,agent)
            Timer += 1
        # FlowRateLimit
        elif action == 4 :
            #spazio[agent][2] = 1
            self.LimitFlowRateAzione.postCondizione(spazio,agent)
            Timer += 1
            # prob 0.5
            """ p = random.random()
            if p < 0.5 :
                spazio[agent][14] = 0  """
        # UnlimitFlowRate
        elif action == 5 :
            self.UnLimitFlowRateAzione.postCondizione(spazio,agent)
            #spazio[agent][2] = 0
            Timer += 1
        # RedirectToHoneypot
        elif action == 6 :
            """ spazio[agent][14] = 0
            spazio[agent][4] = 1  """
            self.RedirectHoneypotAzione.postCondizione(spazio,agent)
            Timer += 1
            # Pxxx da scalare con prob 0.5
            # Pxx da scalare con prob
            # PROVA PER VEDERE SE CONVERGE
            """ p = random.random()
            if p < 0.5 :
                spazio[agent][14] = 0
                for j in range(15,21,1):
                    if spazio[agent][j] > self.T2 :
                        spazio[agent][j] = p """
        # UnHoneypot
        elif action == 7 :
            #spazio[agent][4] = 0
            self.UnRedirectHoneypotAzione.postCondizione(spazio,agent)
            Timer += 1
        # IncreaseLog
        elif action == 8 :
            #spazio[agent][5] += 1
            self.IncreaseLogAzione.postCondizione(spazio,agent)
            Timer += 1
        # DecreaseLog
        elif action == 9 :
            #spazio[agent][5] -= 1
            self.DecreaseLogAzione.postCondizione(spazio,agent)
            Timer += 1
        # QuarantineHost
        elif action == 10 :
            """ spazio[agent][12] = 1
            spazio[agent][7] = 1 """
            self.QuarantineAzione.postCondizione(spazio,agent)
            Timer += 1
            # Pxx da scalare con prob
            # PROVA PER VEDERE SE CONVERGE
            """ p = random.random()
            if p < 0.5 :
                spazio[agent][14] = 0
                for j in range(15,21,1):
                    if spazio[agent][j] > self.T2 :
                        spazio[agent][j] = p  """
        # UnQuarantineHost
        elif action == 11 :
            #spazio[agent][7] = 0
            self.UnQuarantineAzione.postCondizione(spazio,agent)
            Timer += 1
        # ManualResolution
        elif action == 12 :
            """ spazio[agent][6] = 1
            spazio[agent][7] = 0
            spazio[agent][11] = 1
            spazio[agent][14] = 0
            spazio[agent][15] = 0
            spazio[agent][16] = 0
            spazio[agent][17] = 0
            spazio[agent][18] = 0
            spazio[agent][19] = 0
            spazio[agent][20] = 0  """
            self.ManualResolutionAzione.postCondizione(spazio,agent)
            Timer += 1
        # SystemReboot
        elif action == 13 :
            #spazio[agent][8] = 1
            Timer += 1
            self.RebootAzione.postCondizione(spazio,agent)
            """ p = random.random()
            if p < 0.3 :
                # Scalare gli attacchi con una prob
                spazio[agent][14] = 0
                spazio[agent][15] = 0
                spazio[agent][16] = 0
                spazio[agent][17] = 0
                spazio[agent][18] = 0
                spazio[agent][19] = 0
                spazio[agent][20] = 0  """

        # SystemShutdown
        elif action == 14 :
            """ spazio[agent][13] = 1
            spazio[agent][6] = 0  """
            self.ShutDownAzione.postCondizione(spazio,agent)
            Timer += 1
            # Tutti gli attacchi a 0 con una prob
            """ p = random.random()
            if p < 0.3 :
                # Scalare gli attacchi con una prob
                spazio[agent][14] = 0
                spazio[agent][15] = 0
                spazio[agent][16] = 0
                spazio[agent][17] = 0
                spazio[agent][18] = 0
                spazio[agent][19] = 0
                spazio[agent][20] = 0 """
        # SystemStart
        elif action == 15 :
            """ spazio[agent][6] = 1
            spazio[agent][8] = 1 """
            self.StartAzione.postCondizione(spazio,agent)
            Timer += 1
        # BackupHost
        elif action == 16 :
            #spazio[agent][9] = 1
            self.BackupAzione.postCondizione(spazio,agent)
            Timer += 1
        # SoftwareUpdate
        elif action == 17 :
            """ spazio[agent][10] = 1
            spazio[agent][14] = 0
            spazio[agent][15] = 0
            spazio[agent][16] = 0
            spazio[agent][17] = 0
            spazio[agent][18] = 0
            spazio[agent][19] = 0
            spazio[agent][20] = 0  """
            self.UpdateAzione.postCondizione(spazio,agent)
            Timer += 1
            
        return Timer