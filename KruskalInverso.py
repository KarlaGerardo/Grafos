import operator
import re

from PRIM import PRIM
class KruskalInverso:
    def __init__(self, v):
        self.v = v
        self.adj = [0] * v
        self.edges = []
        for i in range(v):
            self.adj[i] = []
  
    def addEdge(self, u: int, v: int, w: int):
        self.adj[u].append(v) 
        self.adj[v].append(u)
        self.edges.append((w, (u, v)))
  
    def dfs(self, v: int, visited: list):
        visited[v] = True
        for i in self.adj[v]:
            if not visited[i]:
                self.dfs(i, visited)

    def connected(self):
        visited = [False] * self.v
        self.dfs(0, visited)
        for i in range(1, self.v):
            if not visited[i]:
                return False
        return True
    def reverseDeleteMST(self):
        aristasKI=[]
        self.edges.sort(key = lambda a: a[0])
        mst_wt = 0
        for i in range(len(self.edges) - 1, -1, -1):
            u = self.edges[i][1][0]
            v = self.edges[i][1][1]
            self.adj[u].remove(v)
            self.adj[v].remove(u)
            if self.connected() == False:
                self.adj[u].append(v)
                self.adj[v].append(u)
                aristaObtenida="id_"+str(u)+"--""id_"+str(v)
                aristasKI.append(aristaObtenida)
                mst_wt += self.edges[i][0]
        return aristasKI,mst_wt


class KruskalInversoS:
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
    
    def IdentificarAristasKI(self):
        nodosDelArchivo=self.MenuDeNodos()
        g=KruskalInverso(len(nodosDelArchivo))
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
        #Algoritmo de Kruskal
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
            g.addEdge(u, v, peso)
        aristasYPesoMTS=g.reverseDeleteMST()
        aristasObtenidasDeLArbol=aristasYPesoMTS[0]
        #Para abrir el archivo y generar el grafo.
        nombreArchivoAGenerarP1=self.nombreDelArchivo
        nombreArchivoAGenerarP1=re.sub("\.gv","",nombreArchivoAGenerarP1)
        nombreArchivoAGenerar=nombreArchivoAGenerarP1+"KruskalInverso.gv"
        file = open(nombreArchivoAGenerar, "w")
        file.write('graph GR{\n')
        for g in range(len(nodosDelArchivo)):
            file.write(nodosDelArchivo[g]+";\n")
        for d in range(len(aristasObtenidasDeLArbol)):
            file.write(aristasObtenidasDeLArbol[d]+";\n")
        file.write("}")
        file.close()
        print("----------------------------------------")
        print("El peso del MTS calculado con Kruskal Inverso es de: ",aristasYPesoMTS[1], "para el grafo ",nombreArchivoAGenerarP1)
        

"""p=NodosConectados('grafoMalla.gv')
p.IdentificarAristas()"""