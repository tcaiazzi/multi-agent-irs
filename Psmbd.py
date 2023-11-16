from azioneSincrona import azioneSincrona

class Psmbd(azioneSincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio):
        spazio['difensore'][16] = 1
