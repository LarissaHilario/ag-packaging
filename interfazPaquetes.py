from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton
from tkinter import filedialog
from ag_original import algoritmo_gen
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MiVentana(CTk):

    button_a_enabled = True
    button_b_enabled = True

    def __init__(self):
        super().__init__()

        self.title("Algoritmos Geneticos")
        self.geometry("610x400")
        self.resizable(False, False)   

        # POBLACIÓN

        self.labelPoblacionSize = CTkLabel(self, text="Población Size:", text_color="#103766")
        self.labelPoblacionSize.place(x=40, y=20)
        self.labelPoblacionSize.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaPoblacionSize = CTkEntry(self, placeholder_text="Población Size", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaPoblacionSize.place(x=180, y=20)
        self.entradaPoblacionSize.configure(width=140, height=30)

        self.labelPoblacionMaxima = CTkLabel(self, text="Población Máxima:", text_color="#103766")
        self.labelPoblacionMaxima.place(x=40, y=60)
        self.labelPoblacionMaxima.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaPoblacionMaxima = CTkEntry(self, placeholder_text="Población Máxima", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaPoblacionMaxima.place(x=180, y=60)
        self.entradaPoblacionMaxima.configure(width=140, height=30)

        # MUTACIÓN

        self.labelProbCruza = CTkLabel(self, text="Probabilidad de Cruza:", text_color="#103766")
        self.labelProbCruza.place(x=40, y=110)
        self.labelProbCruza.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaProbCruza = CTkEntry(self, placeholder_text="Probabilidad de Cruza", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaProbCruza.place(x=180, y=110)
        self.entradaProbCruza.configure(width=140, height=30)

        self.labelProbMuta = CTkLabel(self, text="Probabilidad de Mutación:", text_color="#103766")
        self.labelProbMuta.place(x=40, y=150)
        self.labelProbMuta.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaProbMuta = CTkEntry(self, placeholder_text="Probabilidad de Mutación", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaProbMuta.place(x=180, y=150)
        self.entradaProbMuta.configure(width=140, height=30)

        # ESTANTERÍAS Y REPISAS

        self.labelEstanterias = CTkLabel(self, text="Estanterías", text_color="#103766")
        self.labelEstanterias.place(x=40, y=200)
        self.labelEstanterias.configure(font=("TkDefaultFont", 12, "bold"))

        self.labelNumAnaqueles = CTkLabel(self, text="Número de anaqueles:", text_color="#103766")
        self.labelNumAnaqueles.place(x=40, y=240)
        self.labelNumAnaqueles.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaNumAnaqueles = CTkEntry(self, placeholder_text="Número de anaqueles", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaNumAnaqueles.place(x=200, y=240)
        self.entradaNumAnaqueles.configure(width=140, height=30)

        self.labelNumRepisas = CTkLabel(self, text="Número de repisas:", text_color="#103766")
        self.labelNumRepisas.place(x=40, y=280)
        self.labelNumRepisas.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaNumRepisas = CTkEntry(self, placeholder_text="Número de repisas", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaNumRepisas.place(x=200, y=280)
        self.entradaNumRepisas.configure(width=140, height=30)

        # CARGAR ARCHIVO CSV

        def cargar_archivo():
            ruta_archivo = filedialog.askopenfilename(initialdir="/", title="Seleccionar archivo", filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
            if ruta_archivo:
                self.algoritmo_gen(ruta_archivo)

        self.labelCargarCSV = CTkLabel(self, text="Subir archivo CSV", text_color="#103766")
        self.labelCargarCSV.place(x=40, y=320)
        self.labelCargarCSV.configure(font=("TkDefaultFont", 12, "bold"))

        self.botonCargarCSV = CTkButton(self, text="Cargar Archivo", fg_color="#103766", hover_color="#00B1BD", text_color="#FFFFFF", width=120, font=("Arial", 11, "bold"), command=cargar_archivo)
        self.botonCargarCSV.place(x=200, y=320)

        # ITERACIONES

        self.labelIteraciones = CTkLabel(self, text="Iteraciones:", text_color="#103766")
        self.labelIteraciones.place(x=40, y=370)
        self.labelIteraciones.configure(font=("TkDefaultFont", 12, "bold"))

        self.entradaIteraciones = CTkEntry(self, placeholder_text="Número de iteraciones", border_color="#A5A5A5", placeholder_text_color="#A5A5A5")
        self.entradaIteraciones.place(x=200, y=370)
        self.entradaIteraciones.configure(width=140, height=30)

        # BOTÓN PARA EJECUTAR EL ALGORITMO

        boton_Algorit = CTkButton(self, text="Realizar algoritmo", fg_color="#103766", text_color="#FFFFFF", hover_color="#A8E3E7")
        boton_Algorit.place(x=180, y=420)
        boton_Algorit.configure(width=250, height=30, font=("Arial", 12, "bold"))
        boton_Algorit.configure(command=self.algoritmo_gen)

    def algoritmo_gen(self, ruta_archivo=None):
        poblacionSize = self.entradaPoblacionSize.get()
        poblacionMaxima = self.entradaPoblacionMaxima.get()
        probCruza = self.entradaProbCruza.get()
        probMuta = self.entradaProbMuta.get()
        estanterias = self.entradaNumAnaqueles.get()
        repisas = self.entradaNumRepisas.get()
        iteraciones = self.entradaIteraciones.get()

        if not (poblacionSize and poblacionMaxima and probCruza and probMuta and estanterias and repisas and iteraciones):
            # Mostrar un mensaje de error indicando que todos los campos deben estar llenos
            print("Todos los campos deben estar llenos.")
            return

        poblacionSize = int(poblacionSize)
        poblacionMaxima = int(poblacionMaxima)
        probCruza = float(probCruza)
        probMuta = float(probMuta)
        estanterias = int(estanterias)
        repisas = int(repisas)
        iteraciones = int(iteraciones)

        # Llamar a la función algoritmo_gen
        mejor_ajuste = algoritmo_gen(poblacionSize, poblacionMaxima, probCruza, probMuta, estanterias, repisas, iteraciones, ruta_archivo)


    # Devolver el mejor acomodo de cajas encontrado
        return mejor_ajuste

       
    
  
mi_ventana = MiVentana()
mi_ventana.configure(fg_color="#F8FDFD")
mi_ventana.mainloop()
