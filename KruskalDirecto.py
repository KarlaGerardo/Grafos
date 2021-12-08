import operator
import re
mNodos=[]
class NodosConectados:
    def __init__(self,nombreDelArchivo,nodo):
        self.nombreDelArchivo=nombreDelArchivo
        self.nodoFuente=nodo

    def MenuDeNodos(self):
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
        return nodosEncontrados

class NodosDeLaArista:
    def __init__(self):
        pass


class KruskalDirecto:
    def __init__(self,nombreDelArchivo):
        self.nombreDelArchivo=nombreDelArchivo
    
    def KrusalDirecto(self):
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
        T=[]
        #Para cada nodo en V calcular el componente conectado
        m=NodosConectados(self.nombreDelArchivo,'id_0')
        V=m.MenuDeNodos() #Lista de todos los nodos
        Sb=set() #Conjunto de nodos
        S=[]
        for i in range(len(V)):
            nodo=V[i]
            Sb.add(nodo)
            S.append(Sb)
            Sb=set()
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
            u={nodoEncontradoInicio}
            v={nodoEncontradoFin}
            for j in range(len(S)):
                if nodoEncontradoInicio in S[j]:
                    valor1=j
                if nodoEncontradoFin in S[j]:
                    valor2=j
            if valor1 != valor2:
                u=S[valor1]
                v=S[valor2]
                nuevoConjunto=u|v
                S.remove(u)
                S.remove(v)
                S.append(nuevoConjunto)
                T.append(arista)
        #Para abrir el archivo y generar el grafo.
        nombreArchivoAGenerarP1=self.nombreDelArchivo
        nombreArchivoAGenerarP1=re.sub("\.gv","",nombreArchivoAGenerarP1)
        nombreArchivoAGenerar=nombreArchivoAGenerarP1+"KruskalDirecto.gv"
        file = open(nombreArchivoAGenerar, "w")
        file.write('graph GR{\n')
        for g in range(len(V)):
            file.write(V[g]+";\n")
        for d in range(len(T)):
            file.write(T[d]+";\n")
        file.write("}")
        file.close()

"""p=KruskalDirecto('grafoMalla.gv')
p.KrusalDirecto()"""
