from azioneSincrona import azioneSincrona

class Prmi(azioneSincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio):
        spazio['difensore'][20] = 1