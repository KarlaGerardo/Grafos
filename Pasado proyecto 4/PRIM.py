import sys # Library for INT_MAX
import operator
import re
class PRIM():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                    for row in range(vertices)]
 
    def printMST(self, parent):
        aristasPRIM=[]
        pesosPRIM=0
        for i in range(1, self.V):
            pesosPRIM+=self.graph[i][ parent[i] ]
            aristaEncontrada="id_"+str(parent[i])+"--"+"id_"+str(i)
            aristasPRIM.append( aristaEncontrada)
        
        return aristasPRIM,pesosPRIM
 
    def minKey(self, key, mstSet):
        min_index=0
        min = sys.maxsize
        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v
        return min_index
 
    def primMST(self):
        key = [sys.maxsize] * self.V
        parent = [None] * self.V # Vector para construir el árbol
        key[0] = 0
        mstSet = [False] * self.V
        parent[0] = -1 #Primer nodo raiz
        for cout in range(self.V):
            u = self.minKey(key, mstSet)
            mstSet[u] = True
            for v in range(self.V):
                if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
                        key[v] = self.graph[u][v]
                        parent[v] = u
        self.printMST(parent)
        return self.printMST(parent)
 

class NodosConectados:
    def __init__(self,nombreDelArchivo):
        self.nombreDelArchivo=nombreDelArchivo

    def MenuDeNodos(self):
        mNodos=[]
        with open(self.nombreDelArchivo) as myfile:
            LineasTotales = sum(1 for line in myfile)
        c=0
        a=open(self.nombreDelArchivo)
        f=a.read()
        for i in range(LineasTotales):
            identificador=str(i)
            nodoIdentificado="id_"+identificador
            if nodoIdentificado in f:
                mNodos.append(nodoIdentificado) #Nodos identificados
                c=c+1 #Número de nodos encontrados
        a.close()
        return mNodos
    
    def IdentificarAristas(self):
        nodosDelArchivo=self.MenuDeNodos()
        g=PRIM(len(nodosDelArchivo))
        #Identificar las aristas
        concatenador=""
        concatenador2=""
        aristasPesosJuntos={}
        a=open(self.nombreDelArchivo)
        while(True):
            linea = a.readline()
            sizeLine=len(linea)
            if "=" in linea: 
                subcadena="="
                indice=linea.find(subcadena)
                for i in range(indice+1,sizeLine-3):
                    concatenador=concatenador+linea[i]
                valorDeLaArista=int(concatenador) #Para obtener el valor de la arista
                concatenador=""
                subcadena2="[" #Para recordar qué arista es la que se calculó
                indice2=linea.find(subcadena2)
                for j in range(indice2):
                    concatenador2=concatenador2+linea[j]
                aristasPesosJuntos[concatenador2]=valorDeLaArista
                concatenador2=""
            if not linea:
                break
        a.close()
        #Paso 0:Matriz de indicencia
        matrizE=[0]*len(nodosDelArchivo)
        for i in range(len(nodosDelArchivo)):
            matrizE[i]=[0]*len(nodosDelArchivo)

        #Paso 1: Ordenar las aristas asendentemente por su costo
        aristasPesosJuntosOrdenados=sorted(aristasPesosJuntos.items(),key=operator.itemgetter(1))
        for k in range(len(aristasPesosJuntosOrdenados)):
            aristasT=aristasPesosJuntosOrdenados[k]
            arista=aristasT[0]
            nodoEncontradoFin="" #Para encontrar qué nodos son los que tiene la arista
            nodoEncontradoInicio=""
            for j in range(len(arista)):
                for i in range(j+1,len(arista)):
                    if arista[j]=="-":
                        if arista[i]=="-":
                            for fin in range(i+1,len(arista)):
                                nodoEncontradoFin=nodoEncontradoFin+arista[fin]
                            for inicio in range(j):
                                nodoEncontradoInicio=nodoEncontradoInicio+arista[inicio]
            peso=aristasT[1]
            u=nodoEncontradoInicio
            u=int(re.sub("id_","",u))
            v=nodoEncontradoFin
            v=int(re.sub("id_","",v))
            matrizE[u][v]=peso
            matrizE[v][u]=peso
        g.graph=matrizE
        arbol=g.primMST()
        aristasObtenidasDeLArbol=arbol[0]
        #Para abrir el archivo y generar el grafo.
        nombreArchivoAGenerarP1=self.nombreDelArchivo
        nombreArchivoAGenerarP1=re.sub("\.gv","",nombreArchivoAGenerarP1)
        nombreArchivoAGenerar=nombreArchivoAGenerarP1+"PRIM.gv"
        file = open(nombreArchivoAGenerar, "w")
        file.write('graph GR{\n')
        for g in range(len(nodosDelArchivo)):
            file.write(nodosDelArchivo[g]+";\n")
        for d in range(len(aristasObtenidasDeLArbol)):
            file.write(aristasObtenidasDeLArbol[d]+";\n")
        file.write("}")
        file.close()
        print("El peso del MTS calculado con PRIM es de: ",arbol[1], "para el grafo ",nombreArchivoAGenerarP1)

"""p=NodosConectados('grafoMalla.gv')
p.IdentificarAristas()"""