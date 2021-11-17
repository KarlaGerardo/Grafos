#from nodo import Nodo 

class Arista:
    def __init__(self,nodo1,nodo2,peso=1):
        self.nodo1=nodo1 #Nodo Fuente
        self.nodo2=nodo2 #Nodo Objetivo
        self.peso=peso
    
    def concatenar(self):
        a=str(self.peso)
        return self.nodo1 + '--' + self.nodo2 + "[label="+a+"]"#+"weight="+a+"]"
    
    def concatenarD(self):
        a=str(self.peso)
        return self.nodo1 + '->' + self.nodo2 + "[label="+a+"]"#+"weight="+a+"]"
    
    def name(self):
        a=str(self.nodo1)
        b=str(self.nodo2)
        return self.nodo1 + '--' + self.nodo2 + "[label="+a+"--"+b+"]"
        
    def nodo1Arista(self):
        return self.nodo1
    
    def nodo2Arista(self):
        return self.nodo2
    
    def nameD(self):
        c=str(self.nodo1)
        d=str(self.nodo2)
        return self.nodo1 + '->' + self.nodo2 + "[label="+c+"->"+d+"]"

"""p=Nodo("h1")
hi=p.iden()
p2=Nodo("h2")
hi2=p2.iden()
prueba1=Arista(hi,hi2,True)
f=prueba1.concatenarD()
print(f)"""