import numpy as np
import math as m
import matplotlib.pyplot as plt
import pandas as pd
from paquete import Paquete
from contenedor import Repisa
import random

espacios = 3000000



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
                repisa = Repisa(0, 0, 0)  # Crear una instancia de Repisa
                espacioRepisa = espacios // repisas  # Espacio disponible para cada repisa
                paquetes_repisa = []
                for paquete in csv:
                    if paquete.id not in paquetesColocados and espacioRepisa >= paquete.volumen:
                        paquetes_repisa.append(paquete)
                        paquetesColocados.add(paquete.id)
                        espacioRepisa -= paquete.volumen
                repisa.paquetes = paquetes_repisa
                estanteria.append(repisa)
            individuo.append(estanteria)
        return individuo


    def visualizarPoblacion(population):
        for _, individuo in enumerate(population):
            print(f"Individuo {_ + 1}:")
            visualizarIndividuos(individuo[0])
            print("-----------------------")
   
    def generar_posicion_aleatoria(estanteria_size_x, estanteria_size_y, estanteria_size_z, paquete_longitud, paquete_anchura, paquete_altura):
        # Genera posiciones aleatorias dentro de los límites de la estantería
        x = random.randint(0, estanteria_size_x - paquete_longitud)
        y = random.randint(0, estanteria_size_y - paquete_anchura)
        z = random.randint(0, estanteria_size_z - paquete_altura)
        return x, y, z

    def verificar_colision(posicion, paquete_longitud, paquete_anchura, paquete_altura, paquetes):
        # Verifica si hay colisión entre el nuevo paquete y los paquetes existentes
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
        for paquete in paquetes:
            # Genera posiciones aleatorias dentro de los límites de la repisa
            x = random.uniform(0, repisa_size_x - paquete.longitud)
            y = random.uniform(0, repisa_size_y - paquete.anchura)
            z = random.uniform(0, repisa_size_z - paquete.altura)

            # Ajusta las coordenadas si se encuentran fuera de los límites de la repisa
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if z < 0:
                z = 0
            if x + paquete.longitud > repisa_size_x:
                x = repisa_size_x - paquete.longitud
            if y + paquete.anchura > repisa_size_y:
                y = repisa_size_y - paquete.anchura
            if z + paquete.altura > repisa_size_z:
                z = repisa_size_z - paquete.altura

            # Actualiza la posición del paquete
            paquete.x, paquete.y, paquete.z = x, y, z

    def visualizarRepisa3D(repisa, repisa_index, repisa_size_x, repisa_size_y, repisa_size_z, escala=1.0):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')

        if repisa_index < len(repisa):
            repisa_obj = repisa[repisa_index]

            ax.bar3d(0, 0, 0, repisa_size_x * escala, repisa_size_y * escala, repisa_size_z * escala, color='black', alpha=0.1, linewidth=1, edgecolor='blue')

            # Distribuye los paquetes dentro de la repisa
            distribuir_paquetes(repisa_size_x * escala, repisa_size_y * escala, repisa_size_z * escala, repisa_obj.paquetes)

            for rep in repisa:
                for paquete in rep.paquetes:
                    # Asegúrate de que las coordenadas del paquete estén dentro de los límites de la repisa
                    paquete_x = max(0, min(paquete.x, repisa_size_x - paquete.longitud))
                    paquete_y = max(0, min(paquete.y, repisa_size_y - paquete.anchura))
                    paquete_z = max(0, min(paquete.z, repisa_size_z - paquete.altura))

                    ax.bar3d(paquete_x, paquete_y, paquete_z,
                            paquete.longitud, paquete.anchura, paquete.altura,
                            color=paquete.color, alpha=0.4, linewidth=0.5, edgecolor='black')

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('Visualización de la repisa con paquetes')
            plt.show()
            plt.savefig('grafica.png')
        else:
            print("El índice de la repisa está fuera de los límites.")





    for _ in range(iteraciones):
        csv = ReadData(ruta_archivo).readCsv()
        poblacion = [createIndividuo(csv) for _ in range(poblacionSize)]
        poblacion = cruza(poblacion, csv, probCruza)
        poblacion = mutacion(poblacion, probMuta, csv)
        poblacion = seleccionarMejoresIndividuos(poblacion, csv, poblacionMaxima)
    
    repisa_size_x = 300  # Tamaño de la repisa en el eje x
    repisa_size_y = 100  # Tamaño de la repisa en el eje y
    repisa_size_z = 100  # Tamaño de la repisa en el eje z

    poblacion.sort(key=lambda individuo: evaluarIndividuo(individuo, csv))

    visualizarRepisa3D(poblacion[0][0], 0, repisa_size_x, repisa_size_y, repisa_size_z)
    paquetes = contarPaquetes(poblacion[0])
    print(paquetes - len(csv), "paquetes")
    paquetes = contarPaquetes(poblacion[len(poblacion[0])])
