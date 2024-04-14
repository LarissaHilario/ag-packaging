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


    def visualizarRepisa3D(repisa, repisa_index, escala=1.0):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')

        if repisa_index < len(repisa):
            repisa_obj = repisa[repisa_index]

            # Dimensiones de la repisa establecidas en 1x3x1
            repisa_size_x = 100  # Representa 1 metro
            repisa_size_y = 300  # Representa 3 metros
            repisa_size_z = 100  # Representa 1 metro

            # Dibujar la repisa como borde
            ax.bar3d(0, 0, 0, repisa_size_x * escala, repisa_size_y * escala, repisa_size_z * escala, color='black',alpha=0.3, linewidth=1, edgecolor='blue')

            # Iterar sobre los paquetes y agregar barras 3D para cada uno
            for rep in repisa:
                for paquete in rep.paquetes:
                    # Ajustar las coordenadas para centrar los paquetes dentro de la repisa
                    paquete_x = paquete.x + repisa_size_x / 2 - paquete.longitud / 2
                    paquete_y = paquete.y + repisa_size_y / 2 - paquete.anchura / 2
                    paquete_z = paquete.z + repisa_size_z / 2 - paquete.altura / 2

                    ax.bar3d(paquete_x, paquete_y, paquete_z,
                            paquete.longitud, paquete.anchura, paquete.altura,
                            color=paquete.color, alpha=0.4, linewidth=0.5, edgecolor='black')

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('Visualización de la repisa con paquetes')
            plt.show()
        else:
            print("El índice de la repisa está fuera de los límites.")




    for _ in range(iteraciones):
        csv = ReadData(ruta_archivo).readCsv()
        poblacion = [createIndividuo(csv) for _ in range(poblacionSize)]
        poblacion = cruza(poblacion, csv, probCruza)
        poblacion = mutacion(poblacion, probMuta, csv)
        poblacion = seleccionarMejoresIndividuos(poblacion, csv, poblacionMaxima)

    poblacion.sort(key=lambda individuo: evaluarIndividuo(individuo, csv))
    visualizarRepisa3D(poblacion[0][0], 0)
    paquetes = contarPaquetes(poblacion[0])
    print(paquetes - len(csv), "paquetes")
    paquetes = contarPaquetes(poblacion[len(poblacion[0])])
