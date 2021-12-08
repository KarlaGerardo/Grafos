from arista import Arista
import re



class BFS:
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
                            elif p2==">":
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
                            elif p2==">":
                                for inicio in range(j+1,len(linuo)):
                                    fin=linuo[inicio]
                                    if fin=="[":
                                        for n in range(j-1):
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
    
    def ModeloBFS(self):
        vectorDeNodosYaExplorados=[]
        aristasNodosBFS=[]
        subVector=[]
        nodoAEstudiar=self.nodoFuente #El nodo fuente
        p=BFS(self.nombreDelArchivo,nodoAEstudiar) #Llamas la función para el nodo fuente
        A=p.IdentificadorDeAristas()
        if A[0]==True:
            contador=A[1]
            a=[nodoAEstudiar] #Buscas los nodos conectados del nodo fuente
            contadorDeVueltas=0
            while True:
                for i in range (len(a)): #Una vez que tienes la segunda capa determinas su tamaño para iterarla
                    nodoAEstudiar=a[i] #Cada elemento de la segunda capa toma el lugar del nodo fuente para buscar sus nodos conectados
                    p=BFS(self.nombreDelArchivo,nodoAEstudiar) #Llamas a la función para el primer elemento de la segunda capa
                    subNodos=p.NodosConectados()#Buscas sus nodos conectados y los guardas en una variable para despúes crear la tercera capa
                    for j in range(len(subNodos)): 
                        if subNodos[j] not in subVector:
                            if subNodos[j] not in vectorDeNodosYaExplorados:
                                subVector.append(subNodos[j])
                                if a[i] not in vectorDeNodosYaExplorados:
                                    vectorDeNodosYaExplorados.append(a[i]) #Del lado derecho hay esta cantidad de nodos
                                vectorUnidoBFS=Arista(a[i],subNodos[j]) #Una vez que confirmas que no ha sido explorado se hace la arista
                                aristasNodosBFS.append(vectorUnidoBFS.concatenar())#Se agrega la arista
                        for h in range(len(subVector)):
                            if subVector[h] not in vectorDeNodosYaExplorados:
                                vectorDeNodosYaExplorados.append(subVector[h])
                contadorDeVueltas=contadorDeVueltas+1
                a=subVector #Buscas los nodos conectados del nodo fuente
                if len(a)==contador-1:
                    break
                if contadorDeVueltas>=contador:
                    break

            #Para abrir el archivo y generar el grafo.
            b=A[2]
            nombreArchivoAGenerarP1=self.nombreDelArchivo
            nombreArchivoAGenerarP1=re.sub("\.gv","",nombreArchivoAGenerarP1)
            nombreArchivoAGenerar=nombreArchivoAGenerarP1+"BFS.gv"
            file = open(nombreArchivoAGenerar, "w")
            file.write('graph GR{\n')
            for g in range(len(b)):
                file.write(b[g]+";\n")
            for d in range(len(aristasNodosBFS)):
                file.write(aristasNodosBFS[d]+";\n")
            file.write("}")
            file.close()

#f=BFS('grafoErdosRenyi.gv','id_1')
#p=BFS('grafoMalla.gv',"id_1")
#p.ModeloBFS()

#m=BFS('grafoErdosRenyi.gv','id_1')
#m.ModeloBFS()

#n=BFS('grafoGilbert.gv',"id_1")
#n.ModeloBFS()

#o=BFS('grafoGeografico.gv',"id_1")
#o.ModeloBFS()

#q=BFS('grafoBarabasiAlbert.gv',"id_1")
#q.ModeloBFS()

#r=BFS('grafoDorogovtsevMendes.gv',"id_1")
#r.ModeloBFS()
    