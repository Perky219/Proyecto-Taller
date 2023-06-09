class Participante:
    def __init__(self, nombre, apellido1, apellido2):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2

class Discusion:
    def __init__(self, participante, transcripcion):
        self.participante = participante
        self.transcripcion = transcripcion

class Punto:
    def __init__(self, descripcion):
        self.descripcion = descripcion
        self.discusiones = []

class Apartado:
    def __init__(self, descripcion):
        self.descripcion = descripcion
        self.puntos = []

class NodoMVias:
    def __init__(self, orden):
        self.orden = orden
        self.claves = [None] * (orden - 1)
        self.hijos = [None] * orden
        self.n = 0

class Agenda:
    def __init__(self, titulo, fecha_creacion, orden_arbol):
        self.titulo = titulo
        self.fecha_creacion = fecha_creacion
        self.participantes = []
        self.apartados = []
        self.arbol = NodoMVias(orden_arbol)

    def agregar_participante(self, participante):
        self.participantes.append(participante)

    def eliminar_participante(self, participante):
        self.participantes.remove(participante)

    def agregar_apartado(self, apartado):
        self.apartados.append(apartado)

    def eliminar_apartado(self, apartado):
        self.apartados.remove(apartado)

    def agregar_punto(self, apartado, punto):
        apartado.puntos.append(punto)

    def eliminar_punto(self, apartado, punto):
        apartado.puntos.remove(punto)

    def agregar_discusion(self, punto, discusion):
        punto.discusiones.append(discusion)

    def eliminar_discusion(self, punto, discusion):
        punto.discusiones.remove(discusion)