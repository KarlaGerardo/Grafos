from math import sqrt
import numpy as np
#from DFS_R import DFS_R
from nodo import Nodo
from arista import Arista
from random import randint
from random import random as rd
import matplotlib.pyplot as plt
from random import shuffle
#from BFS import BFS
#from DFS_I import DFS_I

#C:\Users\karla\OneDrive\CIC\B21\Diseño y Análisis\Proyecto 1
#dot -Tpng grafoN.gv -o wp.png

#Aris=int(input('Número de aristas: '))
nod=int(input('Número de nodos: '))
Aris=nod-1 #Esto debe cambiar a input
dirigido=int(input('Dirigido (1) No dirigido (0): '))
autociclado=int(input('Autociclado (1) No Autociclado (0): '))
columnas=int(input('Número de columnas del grafo Malla: '))
filas=int(input('Número de filas del grafo Malla: '))
probabilidad_Gilbert=int(input('Probabilidad para el grafo Gilbert (entre 0 y 100): '))
r=float(input('Distancia del radio para el modelo geográfico (0.0-1.0): '))
d=int(input('Grado de los vertices para el grafo Barabási-Albert: '))

#Variables utilizadas generales
grafo=[] #No sé para qué la estoy ocupando
m=nod-1 #Variables utilizadas para Gn,m de Erdon Renyi


class grafo:
    """
    A continuación se presenta el modelo Gm,n de malla-----------------------------------------------------------
    donde m es el número de columnas y n el número de filas
    Dentro de cada función de grafo ya se genera automáticamente BFS, DFS_I y DFS_R, los cuales generan
    un archivo con el mismo nombre del grafo generado pero con sus terminaciones correspondientes. 
    Estos mismos son analizados con el nodo fuente id_1
    """
    def grafoMalla(self,columnas,filas,dirigido=0):
        vectorNodos=[]
        
        #Para abrir el archivo y generar el grafo.
        if dirigido==1:
            file = open("grafoMalla.gv", "w")
            file.write('digraph GR{\n')
        if dirigido==0:
            file = open("grafoMalla.gv", "w")
            file.write('graph GR{\n')

        #Número de nodos
        nod=columnas*filas

        #Generar los nodos:
        for i in range(nod):
            j=str(i)
            n=Nodo(j)
            vectorNodos.append(n.iden())
            file.write(n.iden()+";\n")
        
        vP=np.array(vectorNodos).reshape(filas,columnas) #Matríz de nodos
        aristasNodosMalla=[]

        #Conexión hacia la derecha
        for i in range(filas):
            for j in range(columnas):
                primerV=vP[i,j]
                if j<(columnas-1):
                    segundoV=vP[i,j+1]
                    if dirigido==1:
                        vectorUnidoMalla=Arista(primerV,segundoV)
                        aristasNodosMalla.append(vectorUnidoMalla.concatenarD())
                        file.write(vectorUnidoMalla.concatenarD()+";\n") 
                    elif dirigido==0:
                        vectorUnidoMalla=Arista(primerV,segundoV)
                        aristasNodosMalla.append(vectorUnidoMalla.concatenar())
                        file.write(vectorUnidoMalla.concatenar()+";\n") 
        
        #Conexión hacía abajo
        for k in range(filas):
            for l in range(columnas):
                primerV=vP[k,l]
                if k<(filas-1):
                    segundoV=vP[k+1,l]
                    if dirigido==1:
                        vectorUnidoMalla=Arista(primerV,segundoV)
                        aristasNodosMalla.append(vectorUnidoMalla.concatenarD())
                        file.write(vectorUnidoMalla.concatenarD()+";\n") 
                    elif dirigido==0:
                        vectorUnidoMalla=Arista(primerV,segundoV)
                        aristasNodosMalla.append(vectorUnidoMalla.concatenar())
                        file.write(vectorUnidoMalla.concatenar()+";\n")

        file.write("}")
        file.close()
        """p=BFS('grafoMalla.gv',"id_1")
        p.ModeloBFS()

        m=DFS_I('grafoMalla.gv','id_1')    
        m.ModeloDFS_I()

        mm=DFS_R('grafoMalla.gv','id_1')    
        mm.ModeloDFSR()"""
        
    """
    A continuación se presenta el modelo Gn,m de Erdon Renyi------------------------------------------------------
    """
    def grafoErdosRenyi(self,nod,m, dirigido=0, autociclado=0):
        aristasNodos=[]
        vectorNodos=[]
        #Para abrir el archivo y generar el grafo.
        if dirigido==1:
            file = open("grafoErdosRenyi.gv", "w")
            file.write('digraph GR{\n')
        if dirigido==0:
            file = open("grafoErdosRenyi.gv", "w")
            file.write('graph GR{\n')


        for i in range(nod):
            j=str(i)
            n=Nodo(j)
            vectorNodos.append(n.iden())
            file.write(n.iden()+";\n")
        t=0
        while t!=m:
            #Grafo Erdos Renyi, Crear n nodos y elige uniformemente al azar m distintos pares de distintos vértices.
            c=randint(0,nod-1) #Nodo fuente
            primerV=vectorNodos[c]
            #print(primerV)
            c1=randint(0,nod-1) #Nodo objetivo
            segundoV=vectorNodos[c1]
            #print(segundoV)


            #Para evitar autociclos
            if (primerV!=segundoV):
                #Para cuando no es dirigido
                if dirigido==0:
                    vectorUnido=Arista(primerV,segundoV) #Aquí entra la clase arista
                    comprobar=vectorUnido.concatenar()
                    if comprobar not in aristasNodos:
                        vectorCUnido=Arista(segundoV,primerV)
                        comprobar2=vectorCUnido.concatenar()
                        if comprobar2 not in aristasNodos:
                            aristasNodos.append(vectorUnido.concatenar())
                            #print(aristasNodos)
                            file.write(vectorUnido.concatenar()+";\n")
                            t=t+1
                #Para cuando es dirigido
                elif dirigido==1:
                    vectorUnido=Arista(primerV,segundoV)
                    comprobar=vectorUnido.concatenarD()
                    if comprobar not in aristasNodos:
                        aristasNodos.append(vectorUnido.concatenarD())
                        file.write(vectorUnido.concatenarD()+";\n")
                        t=t+1
            elif autociclado==1:
                if dirigido==0:
                    vectorUnido=Arista(primerV,segundoV) #Aquí entra la clase arista
                    comprobar=vectorUnido.concatenar()
                    if comprobar not in aristasNodos:
                        vectorCUnido=Arista(segundoV,primerV)
                        comprobar2=vectorUnido.concatenar()
                        if comprobar2 not in aristasNodos:
                            aristasNodos.append(vectorUnido.concatenar())
                            file.write(vectorUnido.concatenar()+";\n")
                            t=t+1
                #Para cuando es dirigido
                elif dirigido==1:
                    vectorUnido=Arista(primerV,segundoV)
                    comprobar=vectorUnido.concatenarD()
                    if comprobar not in aristasNodos:
                        aristasNodos.append(vectorUnido.concatenarD())
                        file.write(vectorUnido.concatenarD()+";\n")
                        t=t+1

        file.write("}")
        file.close()
        
        """p=BFS('grafoErdosRenyi.gv',"id_1")
        p.ModeloBFS()

        m=DFS_I('grafoErdosRenyi.gv','id_1')    
        m.ModeloDFS_I()

        mm=DFS_R('grafoErdosRenyi.gv','id_1')    
        mm.ModeloDFSR()"""
    """
    A continuación se presenta el modelo Gn,p de Gilbert-----------------------------------------------------------
    """
    def grafoGilbert(self,nod, probabilidad_Gilbert, dirigido=0, autociclado=0):
        
        vectorNodos=[]
        #Para abrir el archivo y generar el grafo.
        if dirigido==1:
            file = open("grafoGilbert.gv", "w")
            file.write('digraph GR{\n')
        if dirigido==0:
            file = open("grafoGilbert.gv", "w")
            file.write('graph GR{\n')

        #Generar los nodos:
        for i in range(nod):
            j=str(i)
            n=Nodo(j)
            vectorNodos.append(n.iden())
            file.write(n.iden()+";\n")
        
        #Variables y vectores
        aristasNodosGilbert=[]  #Vector para aristas nodos de Gilbert

        #Algoritmo
        if dirigido==0:
            for u in range(nod): #Aquí había un menos 1
                primerV=vectorNodos[u]
                for s in range(nod):#Aquí había un menos 1
                    segundoV=vectorNodos[s]
                    if autociclado==0:
                        if (primerV!=segundoV): #Para evitar autociclos
                            probabilidad_Random=randint(0,100)
                            if probabilidad_Gilbert>=probabilidad_Random:
                                vectorUnidoGilbert=Arista(primerV,segundoV)
                                comprobar1G=vectorUnidoGilbert.concatenar()
                                comprobar2G=Arista(segundoV,primerV)
                                comprobar2G1=comprobar2G.concatenar()
                                if comprobar1G  not in aristasNodosGilbert:
                                        if comprobar2G1 not in aristasNodosGilbert:
                                            aristasNodosGilbert.append(vectorUnidoGilbert.concatenar())
                                            file.write(vectorUnidoGilbert.concatenar()+";\n")
                    elif autociclado==1:
                        probabilidad_Random=randint(0,100)
                        if probabilidad_Gilbert>=probabilidad_Random:
                            vectorUnidoGilbert=Arista(primerV,segundoV)
                            comprobar1G=vectorUnidoGilbert.concatenar()
                            comprobar2G=Arista(segundoV,primerV)
                            comprobar2G1=comprobar2G.concatenar()
                            if comprobar1G not in aristasNodosGilbert:
                                if comprobar2G1 not in aristasNodosGilbert:
                                    aristasNodosGilbert.append(vectorUnidoGilbert.concatenar())
                                    file.write(vectorUnidoGilbert.concatenar()+";\n")
        elif dirigido==1:
            for u in range(nod): #Aquí había otro menos uno
                primerV=vectorNodos[u]
                for s in range(nod): #Aquí había un menos 1
                    segundoV=vectorNodos[s]
                    if autociclado==0:
                        if (primerV!=segundoV):
                            comprobar1G=Arista(primerV,segundoV)
                            if comprobar1G not in aristasNodosGilbert:
                                probabilidad_Random=randint(0,100)
                                if probabilidad_Gilbert>=probabilidad_Random:
                                    vectorUnidoGilbert=Arista(primerV,segundoV)
                                    aristasNodosGilbert.append(vectorUnidoGilbert.concatenarD())
                                    file.write(vectorUnidoGilbert.concatenarD()+";\n")
                    elif autociclado==1:
                        comprobar1G=Arista(primerV,segundoV)
                        if comprobar1G not in aristasNodosGilbert:
                            probabilidad_Random=randint(0,100)
                            if probabilidad_Gilbert>=probabilidad_Random:
                                vectorUnidoGilbert=Arista(primerV,segundoV)
                                aristasNodosGilbert.append(vectorUnidoGilbert.concatenarD())
                                file.write(vectorUnidoGilbert.concatenarD()+";\n")

        file.write("}")
        file.close()

        """p=BFS('grafoGilbert.gv',"id_1")
        p.ModeloBFS()

        m=DFS_I('grafoGilbert.gv','id_1')    
        m.ModeloDFS_I()

        mm=DFS_R('grafoGilbert.gv','id_1')    
        mm.ModeloDFSR()"""
    """
    A continuación se presenta el modelo Gn,r geográfico simple-----------------------------------------------------
    """
    def grafoGeografico(self,nodos, r, dirigido=0, autociclado=0):
        
        vectorNodos=[]
        #Para abrir el archivo y generar el grafo.
        if dirigido==1:
            file = open("grafoGeografico.gv", "w")
            file.write('digraph GR{\n')
        if dirigido==0:
            file = open("grafoGeografico.gv", "w")
            file.write('graph GR{\n')


        #Generar los nodos:
        for i in range(nodos):
            j=str(i)
            n=Nodo(j)
            vectorNodos.append(n.iden())
            file.write(n.name()+";\n")

        cordenadasX=[] #Vector para guardar las cordenadas X de los nodos
        cordenadasY=[] #Vector para guardar las cordenadas Y de los nodos

        #Generar las cordenadas de los nodos:
        for i in range(nodos):
            cordenadasX.append(rd())
            cordenadasY.append(rd())

        #Seleccionar un nodo al azar
        aristasNodosGeografico=[]  #Vector para aristas nodos Geografico

        for j in range(nodos):
            nodoSeleccionado=vectorNodos[j]
            nodocordenadaX=cordenadasX[j]
            nodoCordenadaY=cordenadasY[j]
            if autociclado==0:
                for i in range(j,nodos-1):
                    nodoMedido=vectorNodos[i+1]
                    nodocordenadaX2=cordenadasX[i+1]
                    nodoCordenadaY2=cordenadasY[i+1]
                    distancia=sqrt((nodocordenadaX2-nodocordenadaX)**2+(nodoCordenadaY2-nodoCordenadaY)**2)
                    if distancia<=r:
                        if dirigido==1:
                            vectorUnidoGeografico=Arista(nodoSeleccionado,nodoMedido,distancia)
                            aristasNodosGeografico.append(vectorUnidoGeografico.concatenarD())
                            file.write(vectorUnidoGeografico.concatenarD()+";\n")
                        if dirigido==0:
                            vectorUnidoGeografico=Arista(nodoSeleccionado,nodoMedido,distancia)
                            aristasNodosGeografico.append(vectorUnidoGeografico.concatenar())
                            file.write(vectorUnidoGeografico.concatenar()+";\n")
            elif autociclado==1:
                for i in range(j,nodos-1):
                    nodoMedido=vectorNodos[i]
                    nodocordenadaX2=cordenadasX[i]
                    nodoCordenadaY2=cordenadasY[i]
                    distancia=sqrt((nodocordenadaX2-nodocordenadaX)**2+(nodoCordenadaY2-nodoCordenadaY)**2)
                    if distancia<=r:
                        if dirigido==1:
                            vectorUnidoGeografico=Arista(nodoSeleccionado,nodoMedido,distancia)
                            aristasNodosGeografico.append(vectorUnidoGeografico.concatenarD())
                            file.write(vectorUnidoGeografico.concatenarD()+";\n")
                        if dirigido==0:
                            vectorUnidoGeografico=Arista(nodoSeleccionado,nodoMedido,distancia)
                            aristasNodosGeografico.append(vectorUnidoGeografico.concatenar())
                            file.write(vectorUnidoGeografico.concatenar()+";\n")
        fig = plt.figure()
        plt.plot(cordenadasX,cordenadasY,'m.')
        fig.savefig('EspacioGeografico.png')

        file.write("}")
        file.close()

        """p=BFS('grafoGeografico.gv',"id_1")
        p.ModeloBFS()

        m=DFS_I('grafoGeografico.gv','id_1')    
        m.ModeloDFS_I()

        mm=DFS_R('grafoGeografico.gv','id_1')    
        mm.ModeloDFSR()"""
    """
    A continuación se presental el modelo Gn,d Barabási-Albert------------------------------------------------------
    Colocar n nodos uno por uno, asignando a cada uno d aristas a vértices------------------------------------------
    distintos de tal manera que la probabilidad de que el vértice nuevo se conecte a un vértice--------------------- 
    existente v es proporcional-------------------------------------------------------------------------------------
    a la cantidad de aristas que v tiene actualmente - los primeros d vértices se conecta todos a todos.------------
    """
    def grafoBarabasiAlbert(self,nod, d, dirigido=0,autociclado=0):
        aristasNodos=[]
        vectorNodos=[]
        #Para abrir el archivo y generar el grafo.
        if dirigido==1:
            file = open("grafoBarabasiAlbert.gv", "w")
            file.write('digraph GR{\n')
        if dirigido==0:
            file = open("grafoBarabasiAlbert.gv", "w")
            file.write('graph GR{\n')

        #Generar los nodos:
        for i in range(nod):
            j=str(i)
            n=Nodo(j)
            vectorNodos.append(n.iden())
            file.write(n.name()+";\n")
            
        #Para confirmar que el grado de "d" es máximo el número de nodos menos 1
        if d<=(nod-1):
            d=d
        else:
            d=nod-1 #Este sería el valor máximo de grado que puede tener el nodo
        
        #Aleatorizar los nodos
        l1=vectorNodos[:]
        contadorConexiones=0
        pro=1

        for i in range(nod):
            shuffle(l1)
            for j in range(nod):
                pro=(d-contadorConexiones)/d
                proTirada=rd()
                primerV=vectorNodos[i]
                if pro>=proTirada:
                    segundoV=l1[j]
                    if autociclado==0:
                        if segundoV!=primerV:
                            if dirigido==0:
                                vectorUnidoBarabasiAlbert=Arista(primerV,segundoV)
                                vectorUnidoBarabasiAlbert2=Arista(segundoV,primerV)
                                a=vectorUnidoBarabasiAlbert.concatenar()
                                b=vectorUnidoBarabasiAlbert2.concatenar()
                                if a not in aristasNodos:
                                    if b not in aristasNodos:
                                        aristasNodos.append(vectorUnidoBarabasiAlbert.concatenar())
                                        file.write(vectorUnidoBarabasiAlbert.name()+";\n")
                            elif dirigido==1:
                                vectorUnidoBarabasiAlbert=Arista(primerV,segundoV)
                                vectorUnidoBarabasiAlbert2=Arista(segundoV,primerV)
                                a=vectorUnidoBarabasiAlbert.concatenarD()
                                b=vectorUnidoBarabasiAlbert2.concatenarD()
                                if a not in aristasNodos:
                                    if b not in aristasNodos:
                                        aristasNodos.append(vectorUnidoBarabasiAlbert.concatenarD())
                                        file.write(vectorUnidoBarabasiAlbert.nameD()+";\n")
                        contadorConexiones=contadorConexiones+1
                    elif autociclado==1:
                        if dirigido==0:
                            vectorUnidoBarabasiAlbert=Arista(primerV,segundoV)
                            vectorUnidoBarabasiAlbert2=Arista(segundoV,primerV)
                            a=vectorUnidoBarabasiAlbert.concatenar()
                            b=vectorUnidoBarabasiAlbert2.concatenar()
                            if a not in aristasNodos:
                                if b not in aristasNodos:
                                    aristasNodos.append(vectorUnidoBarabasiAlbert.concatenar())
                                    file.write(vectorUnidoBarabasiAlbert.name()+";\n")
                        elif dirigido==1:
                            vectorUnidoBarabasiAlbert=Arista(primerV,segundoV)
                            vectorUnidoBarabasiAlbert2=Arista(segundoV,primerV)
                            a=vectorUnidoBarabasiAlbert.concatenarD()
                            b=vectorUnidoBarabasiAlbert2.concatenarD()
                            if a not in aristasNodos:
                                if b not in aristasNodos:
                                    aristasNodos.append(vectorUnidoBarabasiAlbert.concatenarD())
                                    file.write(vectorUnidoBarabasiAlbert.nameD()+";\n")
                        contadorConexiones=contadorConexiones+1
            contadorConexiones=0
        
        #Cerrar archivo
        file.write("}")
        file.close()

        """p=BFS('grafoBarabasiAlbert.gv',"id_1")
        p.ModeloBFS()

        m=DFS_I('grafoBarabasiAlbert.gv','id_1')    
        m.ModeloDFS_I()

        mm=DFS_R('grafoBarabasiAlbert.gv','id_1')    
        mm.ModeloDFSR()"""
    """
    A continuación se muestra el modelo Gn Dorogovtsev-Mendes-------------------------------------------------------
    Crear 3 nodos y 3 aristas formando un triángulo-----------------------------------------------------------------
    Después, para cada nodo adicional, se selecciona una arista al azar y-------------------------------------------
    se crean aristas entre el nodo nuevo y los extremos de la arista seleccionada.----------------------------------
    """
    def grafoDorogovtsevMendes(self,nod, dirigido=0):
        aristasNodos=[]
        vectorNodos=[]
        nodo1aris=[]
        nodo2aris=[]
        if nod<3:
            nod3=3 #Con esto se asegura que sea mayor a tres 
        else:
            nod3=nod
        #Para abrir el archivo y generar el grafo.
        if dirigido==1:
            file = open("grafoDorogovtsevMendes.gv", "w")
            file.write('digraph GR{\n')
        if dirigido==0:
            file = open("grafoDorogovtsevMendes.gv", "w")
            file.write('graph GR{\n')
        
        #Generar los nodos:
        for i in range(nod3):
            j=str(i)
            n=Nodo(j)
            vectorNodos.append(n.iden())
            file.write(n.name()+";\n")

        #Conectar los primeros tres nodos:
        n=2
        for j in range(n):
            primerV=vectorNodos[j]
            for k in range(j+1,n+1):
                segundoV=vectorNodos[k]
                if dirigido==1:
                    vectorUnidoDorogovtsevMendes=Arista(primerV,segundoV)
                    aristasNodos.append(vectorUnidoDorogovtsevMendes.concatenarD())
                    nodo1aris.append(vectorUnidoDorogovtsevMendes.nodo1Arista())
                    nodo2aris.append(vectorUnidoDorogovtsevMendes.nodo2Arista())
                    file.write(vectorUnidoDorogovtsevMendes.nameD()+";\n")
                elif dirigido==0:
                    vectorUnidoDorogovtsevMendes=Arista(primerV,segundoV)
                    aristasNodos.append(vectorUnidoDorogovtsevMendes.concatenar())
                    nodo1aris.append(vectorUnidoDorogovtsevMendes.nodo1Arista())
                    nodo2aris.append(vectorUnidoDorogovtsevMendes.nodo2Arista())
                    file.write(vectorUnidoDorogovtsevMendes.name()+";\n")
        tam=3 #Siempre será el tamaño inicial del vector aristas
        #Escoger arista en 3D
        for l in range(3,nod3): 
            c=randint(0,tam-1)
            primerV=nodo1aris[c]
            segundoV=vectorNodos[l]
            vectorUnidoDorogovtsevMendes=Arista(primerV,segundoV)
            if dirigido==1:
                aristasNodos.append(vectorUnidoDorogovtsevMendes.concatenarD())
                nodo1aris.append(vectorUnidoDorogovtsevMendes.nodo1Arista())
                nodo2aris.append(vectorUnidoDorogovtsevMendes.nodo2Arista())
                file.write(vectorUnidoDorogovtsevMendes.nameD()+";\n")
            elif dirigido==0:
                aristasNodos.append(vectorUnidoDorogovtsevMendes.concatenar())
                nodo1aris.append(vectorUnidoDorogovtsevMendes.nodo1Arista())
                nodo2aris.append(vectorUnidoDorogovtsevMendes.nodo2Arista())
                file.write(vectorUnidoDorogovtsevMendes.name()+";\n")
            primer2V=nodo2aris[c]
            vectorUnidoDorogovtsevMendes2=Arista(primer2V,segundoV)
            if dirigido==1:
                aristasNodos.append(vectorUnidoDorogovtsevMendes2.concatenarD())
                nodo1aris.append(vectorUnidoDorogovtsevMendes2.nodo1Arista())
                nodo2aris.append(vectorUnidoDorogovtsevMendes2.nodo2Arista())
                file.write(vectorUnidoDorogovtsevMendes2.nameD()+";\n")
            elif dirigido==0:
                aristasNodos.append(vectorUnidoDorogovtsevMendes2.concatenar())
                nodo1aris.append(vectorUnidoDorogovtsevMendes2.nodo1Arista())
                nodo2aris.append(vectorUnidoDorogovtsevMendes2.nodo2Arista())
                file.write(vectorUnidoDorogovtsevMendes2.name()+";\n")
            tam=tam+1  
        file.write("}")
        file.close()

        """p=BFS('grafoDorogovtsevMendes.gv',"id_1")
        p.ModeloBFS()

        m=DFS_I('grafoDorogovtsevMendes.gv','id_1')    
        m.ModeloDFS_I()

        mm=DFS_R('grafoDorogovtsevMendes.gv','id_1')    
        mm.ModeloDFSR()"""
        
f=grafo()
f.grafoMalla(columnas,filas,dirigido)
f.grafoErdosRenyi(nod,m,dirigido,autociclado)
f.grafoGilbert(nod,probabilidad_Gilbert,dirigido,autociclado)
f.grafoGeografico(nod,r,dirigido,autociclado)
f.grafoBarabasiAlbert(nod,d,dirigido,autociclado)
f.grafoDorogovtsevMendes(nod,dirigido)
