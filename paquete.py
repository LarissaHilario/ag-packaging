import numpy as np
class Paquete:
    def __init__(self, id, tamaño, peso, volumen, longitud, anchura, altura, x=0, y=0, z=0):
        self.id = id
        self.tamaño = tamaño
        self.peso = peso
        self.volumen = volumen
        self.longitud = longitud
        self.anchura = anchura
        self.altura = altura
        self.x = x
        self.y = y
        self.z = z
        self.color = np.random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k', '#FF6000', '#43FF00', '#FCFF00', '#8400FF', '#0095FF', '#603702',
                  '#8B8B8B'])