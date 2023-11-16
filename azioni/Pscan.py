from azioneSincrona import azioneSincrona

class Pscan(azioneSincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio):
        spazio['difensore'][14] = 1
