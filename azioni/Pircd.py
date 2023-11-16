from azioneSincrona import azioneSincrona

class Pircd(azioneSincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio):
        spazio['difensore'][18] = 1