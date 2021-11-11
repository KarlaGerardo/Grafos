import re
from random import shuffle
from arista import Arista
vectorDeNodosYaExplorados=[]
aristasNodosDFS=[]
mNodos=[]

class DFS_R:
    def __init__(self,archivo,nodoFuente):
        self.archivo=archivo
        self.nodoFuente=nodoFuente

    def LineasTotales(self):
        with open(self.archivo) as myfile:
            total_lines = sum(1 for line in myfile)
        return total_lines
    
    def MenuDeNodos(self,LineasTotales):
        c=0
        a=open(self.archivo)
        f=a.read()
        for i in range(LineasTotales):
            identificador=str(i)
            nodoIdentificado="id_"+identificador
            if nodoIdentificado in f:
                mNodos.append(nodoIdentificado)
                c=c+1
        a.close()
        return c
    
    def NodosConectados(self):
        a=open(self.archivo)
        nodoFuenteSeleccionado1=self.nodoFuente+"-"
        nodoFuenteSeleccionado2=">"+self.nodoFuente+"["
        nodoFuenteSeleccionado3="-"+self.nodoFuente+"["
        nodoEncontrado=""
        nodosEncontrados=[]
        while(True):
            linea = a.readline()
            if nodoFuenteSeleccionado1 in linea: #Para cuando el nodo está del lado izquierdo
                #print(linea)
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

            elif nodoFuenteSeleccionado2 in linea: #Para cuando el nodo está del lado derecho pero es dirigido
                #print(linea)
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
                                        for n in range(j-2):
                                            nodoEncontrado=nodoEncontrado+str(linuo[n])
                                        nodosEncontrados.append(nodoEncontrado)
                                        nodoEncontrado=""

            elif nodoFuenteSeleccionado3 in linea:  #Para cuando el nodo está del lado derecho pero no es dirigido
                #print(linea)
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
            if not linea:
                break
        #print(nodosEncontrados)
        a.close()
        return nodosEncontrados

    def AleatorizarNodos(self,nodosConectados):
        shuffle(nodosConectados)
        #print(nodosConectados)
        return nodosConectados
    
    def nuevoNodoFuente(self,nodosConectados):
        #print(nodosConectados[0])
        return nodosConectados[0]
    
    def ModeloDFSR(self):
        p=DFS_R(self.archivo,self.nodoFuente)    
        ar=p.LineasTotales()
        contador=p.MenuDeNodos(ar)
        nN=self.nodoFuente
        while True:
            p=DFS_R(self.archivo,nN)#Se utiliza de nuevo la clase DFS
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
                        p=DFS_R(self.archivo,nN)#Se utiliza de nuevo la clase DFS
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
                break
            vectorUnidoDFS=Arista(nN,nnN) #Una vez que confirmas que no ha sido explorado se hace la arista
            aristasNodosDFS.append(vectorUnidoDFS.concatenar())#Se agrega la arista
            nN=nnN #El valor del nodo destino ahora se vuelve el nodo fuente

        #Para abrir el archivo y generar el grafo.
        nombreArchivoAGenerarP1=self.archivo
        nombreArchivoAGenerarP1=re.sub("\.gv","",nombreArchivoAGenerarP1)
        nombreArchivoAGenerar=nombreArchivoAGenerarP1+"DFSR.gv"
        file = open(nombreArchivoAGenerar, "w")
        file.write('graph GR{\n')
        for g in range(len(vectorDeNodosYaExplorados)):
            file.write(vectorDeNodosYaExplorados[g]+";\n")
        for d in range(len(aristasNodosDFS)):
            file.write(aristasNodosDFS[d]+";\n")
        file.write("}")
        file.close()

#m=DFS_R('grafoMalla.gv','id_1')    
#m.ModeloDFSR()