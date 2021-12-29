import random
import pygame
import math
import re


X=1000
Y=600


screen=pygame.display.set_mode([X,Y])
screen.fill((255,236,204))

nombreDelArchivo="grafoGilbert.gv"
def MenuDeNodos(nombreDelArchivo):
    mNodos=[]
    with open(nombreDelArchivo) as myfile:
        LineasTotales = sum(1 for line in myfile)
    c=0
    a=open(nombreDelArchivo)
    f=a.read()
    for i in range(LineasTotales):
        identificador=str(i)
        nodoIdentificado="id_"+identificador
        if nodoIdentificado in f:
            mNodos.append(nodoIdentificado) #Nodos identificados
            c=c+1 #Número de nodos encontrados
    a.close()
    return c

nodos=MenuDeNodos(nombreDelArchivo)
print(nodos)
d=600/nodos #Distancia entre los vertices

def IdentificadorDeAristas(nombreDelArchivo,XY,justNodos):
    #Identificar las aristas y nodos de la arista
    concatenador2=""
    aristasGrafo=[]
    a=open(nombreDelArchivo)
    pos1=0
    pos2=0
    while(True):
        linea = a.readline()
        nodo1=''
        nodo2=''
        if "-" in linea: 
            subcadena2="[" #Para encontrar las aristas
            indice2=linea.find(subcadena2)
            #Identifica la arista
            for j in range(indice2):
                concatenador2=concatenador2+linea[j]
            #Identifica los nodos de la arista
            for i in range(len(concatenador2)):
                if concatenador2[i]=="-":
                    if concatenador2[i+1]=="-":
                        for k in range(0,i):
                            nodo1=nodo1+concatenador2[k]
                        for j in range(i+2,len(concatenador2)):
                            nodo2=nodo2+concatenador2[j]
            nodo1=re.sub('id_','',nodo1)
            nodo2=re.sub('id_','',nodo2)
            if nodo1 in justNodos:
                pos1=justNodos.index(nodo1)
            if nodo2 in justNodos:
                pos2=justNodos.index(nodo2)
            X1pos=XY[pos1]
            X2pos=XY[pos2]
            aristasGrafo.append([nodo1,nodo2,X1pos[1],X2pos[1]]) #Arista con los nodos y su posición
            concatenador2=""
        if not linea:
            break
    a.close()
    return aristasGrafo

def NodosConectados(nombreDelArchivo,nodoFuente):
    a=open(nombreDelArchivo)
    nodoFuenteSeleccionado1=nodoFuente+"-"
    nodoFuenteSeleccionado2=">"+nodoFuente+"["
    nodoFuenteSeleccionado3="-"+nodoFuente+"["
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

def DistanciasAleatorias(nodos):
    XY=[]
    justNodos=[]
    for i in range(nodos):
        x=random.randint(100,500)
        y=random.randint(100,300)
        XY.append((i,(x,y)))
        justNodos.append(str(i))
    return XY,justNodos #El nodo y la posición aleatoria que tiene

def SPRING():
    clock=pygame.time.Clock()
    Dis=DistanciasAleatorias(nodos)
    aristasCalculadas=list(IdentificadorDeAristas(nombreDelArchivo,Dis[0],Dis[1])) # Aristas del grafo con distancias aleatorias
    contador=0
    #Variables del algoritmo
    c1=1 #Constante
    c2=100#Constante distancia minima de los nodos
    c3=1 #Constante
    c4=0.1
    M=100
    while contador<100:
        for i in range(len(aristasCalculadas)):
            w=aristasCalculadas[i]
            w1=w[2]
            w2=w[3]
            ax=w1[0]
            ay=w1[1]
            bx=w2[0]
            by=w2[1]
            no1=w[0]
            pygame.draw.circle(screen, (0,0,0),  w1, 5)
            pygame.draw.circle(screen, (0,0,0), w2, 5)
            pygame.draw.line(screen, (8,82,222),w1,w2,2)
            nodocompleto1='id_'+no1
            no2=w[1]
            nodocompleto2='id_'+no2
            nodosConectados1=NodosConectados(nombreDelArchivo,nodocompleto1)
            nodosConectados2=NodosConectados(nombreDelArchivo,nodocompleto2)
            nodosConectadosEncontrados=[]
            nodosConectadosEncontradosB=[]
            for ll in range(len(nodosConectados1)):
                nn=re.sub('id_','',nodosConectados1[ll])
                nodosConectadosEncontrados.append(nn)
            for pp in range(len(nodosConectados2)):
                nn=re.sub('id_','',nodosConectados2[pp])
                nodosConectadosEncontradosB.append(nn)
            if no1 in nodosConectadosEncontradosB:
                nodosConectadosEncontradosB.remove(no1)
            if no2 in nodosConectadosEncontrados:
                nodosConectadosEncontrados.remove(no2)

            #calculate the force acting on each vertex;
            d=math.sqrt((bx-ax)**2+(by-ay)**2)
            #print(d,no1,no2)
            #if d>=c2:
            fa=c1*math.log(d/c2)
            fr=c3/math.sqrt(d)
        
            #Dirección del vector
            pendiente1=(by-ay)/(bx-ax)
            #Sabes que la pendiente será positiva porque by>ay
            if pendiente1<0:
                angulo1=math.atan(pendiente1)+180 #Para el nodo 1
            else: 
                angulo1=math.atan(pendiente1)
            #if ay<by:
            
            #Componentes del vector fa
            AX=c4*fa*math.cos(angulo1)
            AY=c4*fa*math.sin(angulo1)
            AX2=c4*fr*math.cos(angulo1)
            AY2=c4*fr*math.sin(angulo1)
            #Componentes del vector fa nodo2 
            """BX=c4*fa*math.cos(angulo1)
            BY=c4*fa*math.sin(angulo1)
            BX2=c4*fr*math.cos(angulo1)
            BY2=c4*fr*math.sin(angulo1)"""


            #¿Qué nodo está más a la derecha?
            if ax<bx: #Quiere decir que el nodo 1 está más a la izquierda en coordenadas
                nuevaCoordenadaEnX=ax+AX-AX2
                nuevaCoordenadaEnY=ay+AY-AY2
                nuevaCoordenadaEnXB=bx-AX+AX2
                nuevaCoordenadaEnYB=by-AY+AY2
            else:
                nuevaCoordenadaEnX=ax-AX+AX2
                nuevaCoordenadaEnY=ay-AY+AY2
                nuevaCoordenadaEnXB=bx+AX-AX2
                nuevaCoordenadaEnYB=by+AY-AY2

            #Actualización de las aristas 
            for nuevaExploracion in range(len(aristasCalculadas)):
                if no1 in aristasCalculadas[nuevaExploracion]:
                    if (aristasCalculadas[nuevaExploracion].index(no1))==0:
                        aristasCalculadas[nuevaExploracion][2]=(nuevaCoordenadaEnX,nuevaCoordenadaEnY)
                    if (aristasCalculadas[nuevaExploracion].index(no1))==1:
                        aristasCalculadas[nuevaExploracion][3]=(nuevaCoordenadaEnX,nuevaCoordenadaEnY)
                if no2 in aristasCalculadas[nuevaExploracion]:
                    if (aristasCalculadas[nuevaExploracion].index(no2))==0:
                        aristasCalculadas[nuevaExploracion][2]=(nuevaCoordenadaEnXB,nuevaCoordenadaEnYB)
                    if (aristasCalculadas[nuevaExploracion].index(no2))==1:
                        aristasCalculadas[nuevaExploracion][3]=(nuevaCoordenadaEnXB,nuevaCoordenadaEnYB)
            wK=aristasCalculadas[i]
            w1K=wK[2]
            w2K=wK[3]
            pygame.draw.circle(screen, (0,0,0),  w1K, 5)
            pygame.draw.circle(screen, (0,0,0), w2K, 5)
            pygame.draw.line(screen, (8,82,222),w1K,w2K,2)
        contador=contador+1
        clock.tick(100)
        pygame.display.flip()
        screen.fill((255,236,204))
        if contador==100: pygame.quit()
SPRING()
