import re
from random import shuffle
from arista import Arista

class DFS_R1:
    def __init__(self,nombreDelArchivo,nodoFuente):
        self.nombreDelArchivo=nombreDelArchivo
        self.nodoFuente=nodoFuente
        #print('Estoy haciendo'+self.nombreDelArchivo)
    
    def IdentificadorDeAristas(self):
        nodosConAristas=[]
        menuDeNodos=[]
        with open(self.nombreDelArchivo) as myfile:
            total_lines = sum(1 for line in myfile)
        c=0
        a=open(self.nombreDelArchivo)
        f=a.read()
        for i in range(total_lines):
            identificador=str(i)
            nodoIdentificado="id_"+identificador
            nodoIndentificadoD=nodoIdentificado+"--"
            nodoIndentificadoID="->"+nodoIdentificado+"["
            nodoIndentificadoInD="--"+nodoIdentificado+"["
            if nodoIdentificado in f:
                if nodoIndentificadoD in f:
                    if nodoIdentificado not in nodosConAristas:
                        nodosConAristas.append(nodoIdentificado)
                        #print(nodoIndentificadoD)
                        c=c+1 #Para saber cuántos nodos tienen aristas
                if nodoIndentificadoID in f:
                    if nodoIdentificado not in nodosConAristas:
                        nodosConAristas.append(nodoIdentificado)
                        #print(nodoIndentificadoID)
                        c=c+1
                if nodoIndentificadoInD in f:
                    if nodoIdentificado not in nodosConAristas:
                        nodosConAristas.append(nodoIdentificado)
                        #print(nodoIndentificadoInD)
                        c=c+1
                menuDeNodos.append(nodoIdentificado)
        a.close()
        if self.nodoFuente in nodosConAristas:
            siTiene=True
            return siTiene,c,menuDeNodos,nodosConAristas
        else:
            print("El nodo fuente no tiene arista, elija otro para el archivo")
            print(self.nombreDelArchivo)
            siTiene=False
            return siTiene,c
        
    def NodosConectados(self):
        a=open(self.nombreDelArchivo)
        nodoFuenteSeleccionado1=self.nodoFuente+"-"
        nodoFuenteSeleccionado3="-"+self.nodoFuente+"["
        nodoEncontrado=""
        nodosEncontrados=[]
        while(True):
            linea = a.readline()
            if nodoFuenteSeleccionado1 in linea: #Para cuando el nodo está del lado izquierdo
                linuo=linea
                for i in range(len(linuo)):#Para saber el inicio de la conexión
                    p=linuo[i]
                    for j in range(i+1,len(linuo)): #Para confirmar que sí es una conexión
                        p2=linuo[j]
                        if p=="-":
                            if p2=="-":
                                for inicio in range(j+1,len(linuo)):
                                    fin=linuo[inicio]
                                    if fin=="[":
                                        for n in range(j+1,inicio):
                                            nodoEncontrado=nodoEncontrado+str(linuo[n])
                                        nodosEncontrados.append(nodoEncontrado)
                                        nodoEncontrado=""
                            elif p2==">":
                                for inicio in range(j+1,len(linuo)):
                                    fin=linuo[inicio]
                                    if fin=="[":
                                        for n in range(j+1,inicio):
                                            nodoEncontrado=nodoEncontrado+str(linuo[n])
                                        nodosEncontrados.append(nodoEncontrado)
                                        nodoEncontrado=""        
            elif nodoFuenteSeleccionado3 in linea:  #Para cuando el nodo está del lado derecho pero no es dirigido
                linuo=linea
                for i in range(len(linuo)):
                    p=linuo[i]
                    for j in range(i+1,len(linuo)):
                        p2=linuo[j]
                        if p=="-":
                            if p2=="-":
                                for inicio in range(j+1,len(linuo)):
                                    fin=linuo[inicio]
                                    if fin=="[":
                                        for n in range(j-1):
                                            nodoEncontrado=nodoEncontrado+str(linuo[n])
                                        nodosEncontrados.append(nodoEncontrado)
                                        nodoEncontrado=""  
                            elif p2==">":
                                for inicio in range(j+1,len(linuo)):
                                    fin=linuo[inicio]
                                    if fin=="[":
                                        for n in range(j-1):
                                            nodoEncontrado=nodoEncontrado+str(linuo[n])
                                        nodosEncontrados.append(nodoEncontrado)
                                        nodoEncontrado=""       
            if not linea:
                break
        a.close()
        return nodosEncontrados

    def AleatorizarNodos(self,nodosConectados):
        shuffle(nodosConectados)
        #print(nodosConectados)
        return nodosConectados
    
    def nuevoNodoFuente(self,nodosConectados):
        #print(nodosConectados[0])
        return nodosConectados[0]



class DFS_R:
    def __init__(self,nombreDelArchivo,nodoFuente):
        self.nombreDelArchivo=nombreDelArchivo
        self.nodoFuente=nodoFuente
        #print('Estoy haciendo'+self.nombreDelArchivo)

    def ModeloDFSR(self):
        vectorDeNodosYaExplorados=[]
        aristasNodosDFS=[]
        contadorDeVueltas=0
        p=DFS_R1(self.nombreDelArchivo,self.nodoFuente)    
        ar=p.IdentificadorDeAristas()
        contador=ar[1]
        nN=self.nodoFuente
        while True:
            p=DFS_R1(self.nombreDelArchivo,nN)#Se utiliza de nuevo la clase DFS
            vectorDeNodosYaExplorados.append(nN) #Agregas el valor a los nodos ya explorados
            nodosConectados=p.NodosConectados() #Revisas qué nodos tiene conectados
            nCSh=p.AleatorizarNodos(nodosConectados) #Los aleatorizas
            nnN=p.nuevoNodoFuente(nCSh) #El primer valor del vector aleatorizado se toma como segundo nodo destino
            while nnN in vectorDeNodosYaExplorados:
                nCSh.remove(nnN)
                if len(nCSh)==0: 
                    break
                else:
                    nCSh=p.AleatorizarNodos(nCSh) #Los aleatorizas
                    nnN=p.nuevoNodoFuente(nCSh) #El primer valor del vector aleatorizado se toma como segundo nodo destino
            if len(nCSh)==0:  #Ramas secundarias
                vectorDeNodosYaExploradosR=vectorDeNodosYaExplorados.copy()
                nN=vectorDeNodosYaExploradosR[-2]
                while contador>len(vectorDeNodosYaExplorados):
                    while len(vectorDeNodosYaExploradosR)>1:
                        p=DFS_R1(self.nombreDelArchivo,nN)#Se utiliza de nuevo la clase DFS
                        nodosConectados=p.NodosConectados() #Revisas qué nodos tiene conectados
                        nCSh=p.AleatorizarNodos(nodosConectados) #Los aleatorizas
                        nnN=p.nuevoNodoFuente(nCSh) #El primer valor del vector aleatorizado se toma como segundo nodo destino
                        while nnN in vectorDeNodosYaExplorados:
                            nCSh.remove(nnN)
                            if len(nCSh)==0:
                                vectorDeNodosYaExploradosR.pop()
                                break
                            nnN=nCSh[0]
                        if nnN not in vectorDeNodosYaExplorados:
                            vectorDeNodosYaExplorados.append(nnN)
                            vectorDeNodosYaExploradosR=vectorDeNodosYaExplorados.copy()
                            vectorUnidoDFS=Arista(nN,nnN) #Una vez que confirmas que no ha sido explorado se hace la arista
                            aristasNodosDFS.append(vectorUnidoDFS.concatenar())#Se agrega la arista
                            nN=vectorDeNodosYaExplorados[-1]
                        else:
                            nN=vectorDeNodosYaExploradosR[-1]
                    vectorDeNodosYaExploradosR=vectorDeNodosYaExplorados.copy()
                    contadorDeVueltas=contadorDeVueltas+1
                    if contadorDeVueltas>=contador:
                        break
                break
            
            vectorUnidoDFS=Arista(nN,nnN) #Una vez que confirmas que no ha sido explorado se hace la arista
            aristasNodosDFS.append(vectorUnidoDFS.concatenar())#Se agrega la arista
            nN=nnN #El valor del nodo destino ahora se vuelve el nodo fuente

        #Para abrir el archivo y generar el grafo.
        b=ar[2]
        nombreArchivoAGenerarP1=self.nombreDelArchivo
        nombreArchivoAGenerarP1=re.sub("\.gv","",nombreArchivoAGenerarP1)
        nombreArchivoAGenerar=nombreArchivoAGenerarP1+"DFSR.gv"
        file = open(nombreArchivoAGenerar, "w")
        file.write('graph GR{\n')
        for g in range(len(b)):
            file.write(b[g]+";\n")
        for d in range(len(aristasNodosDFS)):
            file.write(aristasNodosDFS[d]+";\n")
        file.write("}")
        file.close()

p=DFS_R('grafoMalla.gv',"id_1")
p.ModeloDFSR()

m=DFS_R('grafoErdosRenyi.gv','id_1')
m.ModeloDFSR()

n=DFS_R('grafoGilbert.gv',"id_1")
n.ModeloDFSR()

o=DFS_R('grafoGeografico.gv',"id_1")
o.ModeloDFSR()

q=DFS_R('grafoBarabasiAlbert.gv',"id_1")
q.ModeloDFSR()

r=DFS_R('grafoDorogovtsevMendes.gv',"id_1")
r.ModeloDFSR()