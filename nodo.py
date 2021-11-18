class Nodo:
    def __init__(self,ide,peso=1):
        self.ide=ide
        self.peso=peso
    
    def iden(self):
        return 'id_'+ self.ide
    
    def name(self):
        a=str(self.iden)
        return 'id_'+ self.ide + "[label="+'id_'+self.ide+"]"
    
    def nameW(self):
        a=str(self.iden)
        b=str(self.iden)
        return 'id_'+ self.ide + "[label="+a+"("+"b"+")"+"]"


#n=Nodo('1')
#print(n.iden())


