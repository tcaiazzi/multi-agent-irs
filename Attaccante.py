from Agente import Agente

from azioni.Pscan import Pscan
from azioni.Pvsftpd import Pvsftpd
from azioni.Psmbd import Psmbd
from azioni.Pphpcgi import Pphpcgi
from azioni.Pircd import Pircd
from azioni.Pdistccd import Pdistccd
from azioni.Prmi import Prmi


class Attaccante(Agente):
    def __init__(self):
        super().__init__()
        self.PscanAzione = Pscan()
        self.PvsftpdAzione = Pvsftpd()
        self.PsmbdAzione = Psmbd()
        self.PphpcgiAzione = Pphpcgi()
        self.PircdAzione = Pircd()
        self.PdistccdAzione = Pdistccd()
        self.PrmiAzione = Prmi()
    
    def preCondizioni(self,spazio,legal_moves):
        if spazio['difensore'][14] < self.T1 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0:
            legal_moves[0] = 1
        else:
            legal_moves[0] = 0
        # Pvsftpd
        if spazio['difensore'][15] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0: 
            legal_moves[1] = 1
        else:
            legal_moves[1] = 0
        # Psmbd
        if spazio['difensore'][16] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0:
            legal_moves[2] = 1
        else:
            legal_moves[2] = 0
        # Pphpcgi
        if spazio['difensore'][17] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0:
            legal_moves[3] = 1
        else:
            legal_moves[3] = 0
        # Pircd
        if spazio['difensore'][18] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0:
            legal_moves[4] = 1
        else:
            legal_moves[4] = 0
        # Pdistccd
        if spazio['difensore'][19] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0:
            legal_moves[5] = 1
        else:
            legal_moves[5] = 0
        # Prmi
        if spazio['difensore'][20] < self.T1 and spazio['difensore'][14] > self.T2 and spazio['difensore'][6] == 1 and spazio['difensore'][10] == 0:
            legal_moves[6] = 1
        else:
            legal_moves[6] = 0
        legal_moves[7] = 1

        # Non ci sono mosse per l'attaccante
        for i in range(8,19,1):
            legal_moves[i] = 0