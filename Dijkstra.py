import operator
import math
from arista import Arista
import re

class Dijkstra:
    def __init__(self,nombreDelArchivo,nodoFuente):
        self.nombreDelArchivo=nombreDelArchivo
        self.nodoFuente=nodoFuente
    
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
            nodoIndentificadoD=nodoIdentificado+"-"
            nodoIndentificadoID="->"+nodoIdentificado+"["
            nodoIndentificadoInD="--"+nodoIdentificado+"["
            if nodoIdentificado in f:
                if nodoIndentificadoD in f:
                    if nodoIdentificado not in nodosConAristas:
                        nodosConAristas.append(nodoIdentificado)
                        c=c+1 #Para saber cuántos nodos tienen aristas
                if nodoIndentificadoID in f:
                    if nodoIdentificado not in nodosConAristas:
                        nodosConAristas.append(nodoIdentificado)
                        c=c+1
                if nodoIndentificadoInD in f:
                    if nodoIdentificado not in nodosConAristas:
                        nodosConAristas.append(nodoIdentificado)
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
            return siTiene,c,menuDeNodos
    

    def NodosConectados(self):
        a=open(self.nombreDelArchivo)
        nodoFuenteSeleccionado1=self.nodoFuente+"-"
        nodoFuenteSeleccionado3="-"+self.nodoFuente+"["
        nodoEncontrado=""
        nodosEncontrados=[]
        r=""
        pesos=[]
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
                for i in range(len(linea)):
                    if linea[i]=="=":
                        for j in range(i,len(linea)-4):
                            r=r+linea[j+1]
                        pesos.append(r)
                        r=""           
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
                for i in range(len(linea)):
                    if linea[i]=="=":
                        for j in range(i,len(linea)-4):
                            r=r+linea[j+1]
                        pesos.append(r)
                        r="" 

            if not linea:
                break
        a.close()
        ss={} #Aquí se ordenan los nodos por pesos 
        for i in range(len(nodosEncontrados)): #Los volvemos diccionarios
            ss[nodosEncontrados[i]]=float(pesos[i])
        sortedDict = sorted(ss.items(), key=operator.itemgetter(1)) #Se ordenan por pesos
        vectorDePesosOrdenado=[]
        vectorDeNodosOrdenadosPorPeso=[]
        for o in range(len(sortedDict)):
            separador=sortedDict[o]
            vectorDeNodosOrdenadosPorPeso.append(separador[0])
            vectorDePesosOrdenado.append(separador[1])
        return vectorDeNodosOrdenadosPorPeso,vectorDePesosOrdenado
    
    def Dijkstra(self):
        p=Dijkstra(self.nombreDelArchivo,self.nodoFuente)
        h=p.IdentificadorDeAristas()
        h2=h[2] #Lista de todos los nodos
        S=[] #Se inicia el conjunto S en cero
        q={} #Cola de prioridades
        for i in range(len(h2)):  #Para cada nodo que pertenece al grafo se agrega a "q" con prioridad infinita
            q[h2[i]]=math.inf
        q.update({self.nodoFuente : 0}) #Se actualiza el nodo fuente a prioridad 0
        aristasu={}
        aristaConPesoDelNodo={}
        while len(q)>0:
            listaDeNodos=list(q)
            u=listaDeNodos[0]
            S.append(u) #Se agrega "u" al conjunto S
            p=Dijkstra(self.nombreDelArchivo,u)
            aristasDD=p.NodosConectados() #Se calculan los nodos conectados de "u"
            aristasD=aristasDD[0]
            pesosAristas=aristasDD[1]
            du=q.get(u) #Se obtiene el valor de "du"
            q.pop(u) #Se borra el nodo "u" de la cola de prioridades
            for j in range(len(aristasD)): #Para cada arista que saliente de "u"
                if aristasD[j] not in S: #Si el nodo no está en el conjunto S
                    dv=q.get(aristasD[j]) #Obtienes su peso
                    if dv>(du+pesosAristas[j]): #Si ese peso es menor que la suma del peso del nodo "u" + el peso de la arista "le"
                        q.update({aristasD[j]:(du+pesosAristas[j])}) #Se actualiza el peso del nodo "v"
                        if aristasD[j] not in aristasu:
                            aristasu[aristasD[j]]=u
                            aristaConPesoDelNodo[aristasD[j]]=(du+pesosAristas[j])
                        else:
                            aristasu.update({aristasD[j]:u})
                            aristaConPesoDelNodo.update({aristasD[j]:(du+pesosAristas[j])})
            qq= sorted(q.items(), key=operator.itemgetter(1)) #Se ordenan por pesos
            q={}
            for k in range(len(qq)):
                dicDeNuevo=qq[k]
                q[dicDeNuevo[0]]=dicDeNuevo[1]
        #Renombrar nodos
        aristaConPesoDelNodoLista=sorted(aristaConPesoDelNodo.items(), key=operator.itemgetter(1))
        for d in range(len(aristaConPesoDelNodoLista)):
            nombreNuevo=aristaConPesoDelNodoLista[d]
            if nombreNuevo[0] in h2:
                h2.remove(nombreNuevo[0])
                h2.append(nombreNuevo[0]+"("+str(nombreNuevo[1])+")")
        #Crear aristas
        p=Dijkstra(self.nombreDelArchivo,self.nodoFuente)
        hj=p.IdentificadorDeAristas()
        h22=hj[2] #Lista de todos los nodos
        aristasTotalesDijkstra=[]
        aristasuLista=sorted(aristasu.items(), key=operator.itemgetter(1))
        for l in range(len(aristasuLista)):
            aristaCreada=aristasuLista[l]
            nodo1=aristaCreada[1]
            nodo2=aristaCreada[0]
            if nodo2 in h22:
                for ll in range(len(aristaConPesoDelNodoLista)):
                    nn=aristaConPesoDelNodoLista[ll]
                    if nodo2==nn[0]:
                        nodo2=nodo2+"("+str(nn[1])+")"
            if nodo1 in h22:
                for ll in range(len(aristaConPesoDelNodoLista)):
                    nn=aristaConPesoDelNodoLista[ll]
                    if nodo1==nn[0]:
                        nodo1=nodo1+"("+str(nn[1])+")"
            aristaDijkstra=Arista(nodo1,nodo2)
            aristasTotalesDijkstra.append(aristaDijkstra.concatenarD())
        #Para abrir el archivo y generar el grafo.
        nombreArchivoAGenerarP1=self.nombreDelArchivo
        nombreArchivoAGenerarP1=re.sub("\.gv","",nombreArchivoAGenerarP1)
        nombreArchivoAGenerar=nombreArchivoAGenerarP1+"Dijkstra.gv"
        file = open(nombreArchivoAGenerar, "w")
        file.write('graph GR{\n')
        for g in range(len(h2)):
            file.write(h2[g]+";\n")
        for d in range(len(aristasTotalesDijkstra)):
            file.write(aristasTotalesDijkstra[d]+";\n")
        file.write("}")
        file.close()


#p=Dijkstra('grafoGeografico.gv','id_0')
#gg=p.Dijkstra()