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
from azioni.noOp import noOp

from threading import Thread

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
        self.noOp = noOp()

    # Il difensore invece può eseguire una mossa solo nel caso incui il Timer è <=0 ed ogni mossa vale 1
    def preCondizioni(self,spazio,legal_moves):
        # Generate alert
        self.GenerateAlertAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # FirewallActivation
        # preso dal paper
        self.FirewallActivationAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # BlockSourceIp
        # preso dal paper
        self.BlockIpAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # UnblockSourceIp
        self.UnBlockIpAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # FlowRateLimit
        # preso dal paper
        self.LimitFlowRateAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # UnlimitFlowRate
        self.UnLimitFlowRateAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # RedirectToHoneypot
        self.RedirectHoneypotAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # UnHoneypot
        self.UnRedirectHoneypotAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # IncreaseLog
        self.IncreaseLogAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # DecreaseLog
        self.DecreaseLogAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # QuarantineHost
        self.QuarantineAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
          
        # UnQuarantineHost
        self.UnQuarantineAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # ManualResolution 
        self.ManualResolutionAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # SystemReboot
        self.RebootAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # SystemShutdown
        self.ShutDownAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # SystemStart
        self.StartAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # BackupHost
        self.BackupAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,self.mosseAsincroneRunning)
        
        # SoftwareUpdate
        # detto dal prof: deve aver fatto backup
        self.UpdateAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # noOp (altrimenti se nulla è selezionbile sceglie a caso)
        # Ora abbiamo deciso di renderla ammissibile ad ogni stato così che possa terminare anche 
        # quando non ho piu mosse che mi portano sullo stato target (finale)
        self.noOp.preCondizione(spazio,legal_moves,self.T1,self.T2,self.__class__.__name__)
        #legal_moves[18] = 1




    def postCondizioni(self,action,spazio,agent):
        print('Mosse Asincrone in Running prima della mossa:',self.mosseAsincroneRunning)

        # GenerateAlert
        if action == 0 :
            self.GenerateAlertAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # FirewallActivation
        elif action == 1 :
            self.FirewallActivationAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # BlockSourceIp
        elif action == 2 :
            self.BlockIpAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # UnblockSourceIp
        elif action == 3 :
            self.UnBlockIpAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # FlowRateLimit
        elif action == 4 :
            self.LimitFlowRateAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # UnlimitFlowRate
        elif action == 5 :
            self.UnLimitFlowRateAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # RedirectToHoneypot
        elif action == 6 :
            self.RedirectHoneypotAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # UnHoneypot
        elif action == 7 :
            self.UnRedirectHoneypotAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # IncreaseLog
        elif action == 8 :
            self.IncreaseLogAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # DecreaseLog
        elif action == 9 :
            self.DecreaseLogAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # QuarantineHost
        elif action == 10 :
            self.QuarantineAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # UnQuarantineHost
        elif action == 11 :
            self.UnQuarantineAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # ManualResolution
        elif action == 12 :
            self.ManualResolutionAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # SystemReboot
        elif action == 13 :
            # Timer
            spazio[agent][21] += 1
            self.RebootAzione.postCondizione(spazio,agent)
        
        # SystemShutdown
        elif action == 14 :
            self.ShutDownAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # SystemStart
        elif action == 15 :
            self.StartAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
        
        # BackupHost
        elif action == 16 :
            self.mosseAsincroneRunning.append(action)
            Thread(target=self.BackupAzione.postCondizione,args=(spazio,agent,self.mosseAsincroneRunning,action)).start()
            print('AVVIO BACKUP')
            # Timer
            spazio[agent][21] += 1

        # SoftwareUpdate
        elif action == 17 :
            self.UpdateAzione.postCondizione(spazio,agent)
            # Timer
            spazio[agent][21] += 1
