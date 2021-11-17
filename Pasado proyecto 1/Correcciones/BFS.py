from arista import Arista
import re
vectorDeNodosYaExplorados=[]
aristasNodosBFS=[]
mNodos=[]
capas=[]
class BFS:
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
                #print(nodoIdentificado) #Esto te imprime el menú de nodos que tiene el archivo
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
        a.close()
        return nodosEncontrados
    
    def ModeloBFS(self):
        capas=[]
        #n1=input('Ingrese el nodo fuente: ')
        n1vector=[]
        n1vector.append(self.nodoFuente)
        capas.append(n1vector)
        vectorDeNodosYaExplorados.append(self.nodoFuente)
        p=BFS(self.archivo,self.nodoFuente)
        ar=p.LineasTotales()
        contador=p.MenuDeNodos(ar)
        nodosConectados=p.NodosConectados()
        capas.append(nodosConectados)
        nodosConectadosS=[]
        for i in range(len(n1vector)):
            nN=n1vector[i]
            vectorDeNodosYaExplorados.append(nN)
            p=BFS(self.archivo,nN)
            a=p.NodosConectados()
            for j in range(len(a)):
                if a[j] not in nodosConectadosS:
                    if a[j] not in vectorDeNodosYaExplorados:
                        nodosConectadosS.append(a[j])
                        vectorUnidoBFS=Arista(nN,a[j]) #Una vez que confirmas que no ha sido explorado se hace la arista
                        aristasNodosBFS.append(vectorUnidoBFS.concatenar())#Se agrega la arista
        capas.append(nodosConectadosS)
        while len(vectorDeNodosYaExplorados)<(contador+1):
            nodosConectados=nodosConectadosS.copy()
            nodosConectadosS=[]
            for i in range(len(nodosConectados)):
                nN=nodosConectados[i]
                vectorDeNodosYaExplorados.append(nN)
                p=BFS(self.archivo,nN)
                a=p.NodosConectados()
                for j in range(len(a)):
                    if a[j] not in nodosConectadosS:
                        if a[j] not in vectorDeNodosYaExplorados:
                            nodosConectadosS.append(a[j])
                            vectorUnidoBFS=Arista(nN,a[j]) #Una vez que confirmas que no ha sido explorado se hace la arista
                            aristasNodosBFS.append(vectorUnidoBFS.concatenar())#Se agrega la arista
            capas.append(nodosConectadosS)
        vectorDeNodosYaExplorados.pop(0)
        #Para abrir el archivo y generar el grafo.
        nombreArchivoAGenerarP1=self.archivo
        nombreArchivoAGenerarP1=re.sub("\.gv","",nombreArchivoAGenerarP1)
        nombreArchivoAGenerar=nombreArchivoAGenerarP1+"BFS.gv"
        file = open(nombreArchivoAGenerar, "w")
        file.write('graph GR{\n')
        for g in range(len(vectorDeNodosYaExplorados)):
            file.write(vectorDeNodosYaExplorados[g]+";\n")
        for d in range(len(aristasNodosBFS)):
            file.write(aristasNodosBFS[d]+";\n")
        file.write("}")
        file.close()
        


   
