from azioneSincrona import azioneSincrona

class Pdistccd(azioneSincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio):
        spazio['difensore'][19] = 1