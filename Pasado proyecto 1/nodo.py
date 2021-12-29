class Nodo:
    def __init__(self,ide):
        self.ide=ide
    
    def iden(self):
        return 'id_'+ self.ide
    
    def name(self):
        a=str(self.iden)
        return 'id_'+ self.ide #+ "[label="+'id_'+self.ide+"]"


#n=Nodo('1')
#print(n.iden())


