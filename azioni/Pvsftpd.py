from azioneSincrona import azioneSincrona

class Pvsftpd(azioneSincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio):
        spazio['difensore'][15] = 1
