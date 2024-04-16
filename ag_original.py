import numpy as np
import math as m
import matplotlib.pyplot as plt
import pandas as pd
from paquete import Paquete
from contenedor import Repisa
import random

espacios = 3000000
repisa_size_x = 300  
repisa_size_y = 100  
repisa_size_z = 100 



def algoritmo_gen(poblacionSize, poblacionMaxima, probCruza, probMuta, estanterias, repisas, iteraciones, ruta_archivo):
    class ReadData:
        def __init__(self, archivo):
            self.archivo = archivo

        def readCsv(self):
            df = pd.read_csv(self.archivo)
            paquetes = []
            for index, row in df.iterrows():
                id = row["ID"]
                tamaño = row["Tamaño"]
                peso = row["Peso"]
                volumen = row["Volumen"]
                longitud = row["Longitud"]
                anchura = row["Anchura"]
                altura = row["Altura"]
                paquete = Paquete(
                    id, tamaño, peso, volumen, longitud, anchura, altura
                )
                paquetes.append(paquete)
            print("Datos leídos desde el archivo CSV:")
            return paquetes


    def cruza(poblacion, csv, probCruza):
        newPoblacion = []
        poblacion.sort(
            key=lambda individuo: evaluarIndividuo(individuo, csv), reverse=True
        )
        for estanteria in poblacion:
            if random.uniform(0, 1) < probCruza:
                padre2 = random.sample(poblacion, 1)
                padre1 = estanteria
                puntoCruza = random.randint(0, len(padre1))
                hijo = padre1[:puntoCruza] + padre2[0][puntoCruza:]
                newPoblacion.append(padre1)
                newPoblacion.append(hijo)
                hijo = eliminarPaquetesRepetidos(hijo, csv)

            else:
                newPoblacion.append(estanteria)
        newPoblacion = poblacion + newPoblacion
        return newPoblacion


    def mutacion(poblacion, probMutacion, csv):
        for individuo in poblacion:
            if random.random() < probMutacion:
                repisa1 = random.randint(0, len(individuo) - 1)
                repisa2 = random.randint(0, len(individuo) - 1)
                paquete1 = random.randint(0, len(individuo[repisa1]) - 1)
                paquete2 = random.randint(0, len(individuo[repisa2]) - 1)
                individuo[repisa1][paquete1], individuo[repisa2][paquete2] = individuo[repisa2][paquete2], individuo[repisa1][paquete1]
                individuo = eliminarPaquetesRepetidos(individuo, csv)
        return poblacion


    def evaluarIndividuo(individuo, csv):
        espacioTotal = estanterias * repisas * espacios
        volumenTotal = sum(paquete.volumen for paquete in csv)
        volumenOcupado = sum(
            sum(paquete.volumen for paquete in repisa.paquetes) for estanteria in individuo for repisa in estanteria
        )
        espacioDisponible = espacioTotal - volumenOcupado
        puntaje = espacioDisponible / volumenTotal
        paquetesDentro = contarPaquetes(individuo)
        paquetesFuera = len(csv) - paquetesDentro
        puntaje += 0.3 * paquetesFuera

        return puntaje



    def seleccionarMejoresIndividuos(poblacion, csv, numMejores):
        evaluaciones = [
            (individuo, evaluarIndividuo(individuo, csv)) for individuo in poblacion
        ]
        evaluaciones.sort(key=lambda x: x[1], reverse=True)
        mejoresIndividuos = [evaluacion[0] for evaluacion in evaluaciones[:numMejores]]
        return mejoresIndividuos


    def contarPaquetes(estanterias):
        paquetesVistos = set()
        for estanteria in estanterias:
            for repisa in estanteria:
                for paquete in repisa.paquetes:
                    if paquete.id not in paquetesVistos:
                        paquetesVistos.add(paquete.id)

        return len(paquetesVistos)



    def eliminarPaquetesRepetidos(hijo, csv):
        hijoLimpio = []

        for estanteria in hijo:
            paquetesVistos = set()
            paquetesRepetidos = set()
            cleanEstanteria = []
            for repisa in estanteria:
                volumenEstante = espacios
                cleanRepisa = []
                for paquete in repisa.paquetes:
                    if (
                        paquete.id not in paquetesVistos
                        and volumenEstante >= paquete.volumen
                    ):
                        volumenEstante -= paquete.volumen
                        paquetesVistos.add(paquete.id)
                        cleanRepisa.append(paquete)
                    else:
                        for paquete in csv:
                            if (
                                paquete.id not in paquetesVistos
                                and volumenEstante >= paquete.volumen
                            ):
                                cleanRepisa.append(paquete)
                                volumenEstante -= paquete.volumen
                                paquetesVistos.add(paquete.id)
                        continue
                cleanEstanteria.append(cleanRepisa)
            hijoLimpio.append(cleanEstanteria)
        return hijoLimpio


    def createIndividuo(csv):
        individuo = []
        paquetesSinGuardar = []
        paquetesColocados = set()
        for _ in range(estanterias):
            estanteria = []
            for _ in range(repisas):
                c = 0
                repisa = Repisa(0, 0, 0)
                espacioRepisa = espacios
                paquetes_repisa = []
                while espacioRepisa >= 0:
                    indice = random.randint(0, len(csv) - 1)
                    paquete = csv[indice]
                    volumenPaquete = paquete.volumen
                    if (
                        paquete.id not in paquetesColocados
                        and espacioRepisa >= volumenPaquete
                    ):
                        paquetes_repisa.append(paquete)
                        paquetesColocados.add(paquete.id)
                        espacioRepisa -= paquete.volumen
                    elif paquete.id in paquetesColocados and c != len(csv):
                        c += 1
                        continue
                    else:
                        for paquete in csv:
                            if (
                                paquete.id not in paquetesColocados
                                and espacioRepisa >= paquete.volumen
                            ):
                                paquetes_repisa.append(paquete)
                                espacioRepisa -= paquete.volumen
                                paquetesColocados.add(paquete.id)
                        break

                repisa.paquetes = paquetes_repisa
                estanteria.append(repisa)
            individuo.append(estanteria)
        paquetesGuardados = set(
            paquete.id
            for estanteria in individuo
            for repisa in estanteria
            for paquete in repisa.paquetes
        )
        for estanteria in individuo:
            for repisa in estanteria:
                distribuir_paquetes(repisa_size_x, repisa_size_y, repisa_size_z, repisa.paquetes)
        for paquete in csv:
            if paquete.id not in paquetesGuardados:
                paquetesSinGuardar.append(paquete)
        return individuo

                        
    def generar_posicion_aleatoria(estanteria_size_x, estanteria_size_y, estanteria_size_z, paquete_longitud, paquete_anchura, paquete_altura):
        x = random.randint(0, estanteria_size_x - paquete_longitud)
        y = random.randint(0, estanteria_size_y - paquete_anchura)
        z = random.randint(0, estanteria_size_z - paquete_altura)
        return x, y, z

    def verificar_colision(posicion, paquete_longitud, paquete_anchura, paquete_altura, paquetes):
        for p in paquetes:
            if (posicion[0] < p.x + p.longitud and
                posicion[0] + paquete_longitud > p.x and
                posicion[1] < p.y + p.anchura and
                posicion[1] + paquete_anchura > p.y and
                posicion[2] < p.z + p.altura and
                posicion[2] + paquete_altura > p.z):
                return True  # Hay colisión
        return False  # No hay colisión

    def distribuir_paquetes(repisa_size_x, repisa_size_y, repisa_size_z, paquetes):
       
        paquetes.sort(key=lambda p: p.volumen, reverse=True)
        current_x = current_y = current_z = 0

        for paquete in paquetes:
          
            if current_x + paquete.longitud <= repisa_size_x and \
            current_y + paquete.anchura <= repisa_size_y and \
            current_z + paquete.altura <= repisa_size_z:
               
                paquete.x, paquete.y, paquete.z = current_x, current_y, current_z

                current_x += paquete.longitud

            else:
                # Si el paquete no cabe en la posición actual, moverse al siguiente nivel (eje y)
                current_y += paquete.anchura
                current_x = 0  
                current_z = 0  

                # Verificar si se ha alcanzado el final de la repisa en el eje y
                if current_y + paquete.anchura > repisa_size_y:
                   
                    current_z += paquete.altura
                    current_y = 0 
                   
                    if current_z + paquete.altura > repisa_size_z:
                        print("La repisa está llena. No se pueden colocar más paquetes.")
                        break




    def visualizarPoblacion(population):
        
        best_individual = max(population, key=lambda individuo: evaluarIndividuo(individuo, csv))
        
        print("Visualización de todas las estanterías del mejor individuo:")
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        for j, estanteria in enumerate(best_individual):
            for k, repisa in enumerate(estanteria):
                print(f"Estantería {j+1}, Repisa {k+1}:")
                visualizarRepisa3D(repisa, repisa_size_x, repisa_size_y, repisa_size_z)
                print("-----------------------")
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Visualización de todas las estanterías del mejor individuo')
        plt.show()


    def visualizarRepisa3D(repisa, repisa_size_x, repisa_size_y, repisa_size_z, escala=1.0):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d') 
        ax.bar3d(0, 0, 0, repisa_size_x * escala, repisa_size_y * escala, repisa_size_z * escala, color='black', alpha=0.1, linewidth=1, edgecolor='blue')

        for paquete in repisa.paquetes:
            ax.bar3d(paquete.x, paquete.y, paquete.z,
                    paquete.longitud, paquete.anchura, paquete.altura,
                    color=paquete.color, alpha=0.4, linewidth=0.5, edgecolor='black')
        plt.savefig('grafica.png')
        

    for _ in range(iteraciones):
        csv = ReadData(ruta_archivo).readCsv()
        poblacion = [createIndividuo(csv) for _ in range(poblacionSize)]
        poblacion = cruza(poblacion, csv, probCruza)
        poblacion = mutacion(poblacion, probMuta, csv)
        poblacion = seleccionarMejoresIndividuos(poblacion, csv, poblacionMaxima)
    

    poblacion.sort(key=lambda individuo: evaluarIndividuo(individuo, csv))
    visualizarPoblacion(poblacion)
    paquetes = contarPaquetes(poblacion[0])
    print(paquetes - len(csv), "paquetes")
    paquetes = contarPaquetes(poblacion[len(poblacion[0])])
