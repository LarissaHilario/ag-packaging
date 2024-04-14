import numpy as np
import math as m
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from contenedor import Repisa
from paquete import Paquete
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
        paquetesVistos = set()  # Definir paquetesVistos aquí

        for estanteria in hijo:
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
                cleanEstanteria.append(cleanRepisa)  # Añadir la repisa limpia a la estantería limpia
            hijoLimpio.append(cleanEstanteria)  # Añadir la estantería limpia al hijo limpio
        return hijoLimpio





    def createIndividuo(csv):
        individuo = []
        paquetesSinGuardar = []
        paquetesColocados = set()
        for _ in range(estanterias):
            estanteria = []
            for _ in range(repisas):
                c = 0

                repisa = Repisa(0, 0, 0)  # Crear una nueva instancia de Repisa
                espacioEstanteria = espacios
                while espacioEstanteria >= 0:
                    indice = random.randint(0, len(csv) - 1)
                    paquete = csv[indice]
                    volumePaquete = paquete.volumen
                    if (
                        paquete.id not in paquetesColocados
                        and espacioEstanteria >= volumePaquete
                    ):
                        repisa.paquetes.append(paquete) 
                        espacioEstanteria -= volumePaquete
                        paquetesColocados.add(paquete.id)
                    elif paquete.id in paquetesColocados and c != len(csv):
                        c += 1
                        continue
                    else:
                        for paquete in csv:
                            if (
                                paquete.id not in paquetesColocados
                                and espacioEstanteria >= paquete.volumen
                            ):
                                repisa.paquetes.append(paquete) 
                                espacioEstanteria -= paquete.volumen
                                paquetesColocados.add(paquete.id)
                        break

                estanteria.append(repisa)
            individuo.append(estanteria)

        paquetesGuardados = set(
            paquete.id
            for estanteria in individuo
            for repisa in estanteria
            for paquete in repisa.paquetes
        )
        for paquete in csv:
            if paquete.id not in paquetesGuardados:
                paquetesSinGuardar.append(paquete)
        return individuo



    def visualizarPoblacion(population):
        for _, individuo in enumerate(population):
            print(f"Individuo {_ + 1}:")
            visualizarIndividuos(individuo[0])
            print("-----------------------")


    def visualizarIndividuos(individuo):
        fig, ax = plt.subplots(figsize=(10, 6))

        for i, estanteria in enumerate(individuo):
            volumen_usado = sum(paquete.volumen for repisa in estanteria for paquete in repisa.paquetes)
            ax.barh(i, volumensado, color="blue")

        ax.set_yticks(range(len(individuo)))
        ax.set_yticklabels([f"Estantería {i+1}" for i in range(len(individuo))])
        ax.set_xlabel("Volumen ocupado")
        ax.set_ylabel("Estanterías")
        ax.set_title("Visualización de la población generada")
        plt.show()


    def visualizarIndividuos3D(individuo):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')

        for estanteria in individuo:
            for repisa in estanteria:
                ax.bar3d(repisa.x, repisa.y, repisa.z,
                        repisa.longitud, repisa.anchura, repisa.altura, alpha=0.6, linewidth=0.5)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Visualización de la población generada')
        plt.show()



    for _ in range(iteraciones):
        csv = ReadData(ruta_archivo).readCsv()
        poblacion = [createIndividuo(csv) for _ in range(poblacionSize)]
        poblacion = cruza(poblacion, csv, probCruza)
        poblacion = mutacion(poblacion, probMuta, csv)
        poblacion = seleccionarMejoresIndividuos(poblacion, csv, poblacionMaxima)

    poblacion.sort(key=lambda individuo: evaluarIndividuo(individuo, csv))
    visualizarIndividuos(poblacion[0][0])
    visualizarIndividuos3D(poblacion[0][0])
    paquetes = contarPaquetes(poblacion[0])
    print(paquetes - len(csv), "paquetes")
    paquetes = contarPaquetes(poblacion[len(poblacion[0])])
