from Agenda import agenda as Agenda, persona as Persona, apartados as Apartados, puntos as Puntos, discusion as Discusion, lista as Lista
from datetime import datetime
from tkinter import messagebox

class MiAgenda(Agenda):
    def __init__(self,titulo:str,fecha:datetime) -> None:
        super().__init__()
        self.titulo:str=titulo
        self.fecha:datetime=fecha
        self.participantes:MiPersona=None
        self.apartados:MiApartado=None
        
    def agregar_participante(self, nombre: str, apellido1: str, apellido2: str):
        if self.participantes==None:
            self.participantes=MiPersona(nombre=nombre,apellido1=apellido1,apellido2=apellido2)
        else:
            self.participantes.agregar(nombre,apellido1,apellido2)

    def agregar_apartado(self,apartado:str):
        if self.apartados==None:
            self.apartados=MiApartado(apartado)
        else:
            self.apartados.agregar(apartado)

    def agregar_punto(self, punto: str, apartado: str):
        if self.apartados is not None:
            nodo_actual = self.apartados
            while nodo_actual is not None:
                if nodo_actual.apartado == apartado:
                    if nodo_actual.puntos is None:
                        nodo_actual.puntos = MiPunto(punto)
                    else:
                        nodo_puntos = nodo_actual.puntos
                        while nodo_puntos.sig is not None:
                            nodo_puntos = nodo_puntos.sig
                        nodo_puntos.sig = MiPunto(punto)
                    break
                else:
                    nodo_actual = nodo_actual.sig
        else:
            self.apartados = MiApartado(apartado)
            self.apartados.puntos = MiPunto(punto)

    def agregar_discusión(self, persona, apartado, punto, discusión):
        nueva_discusión = MiDiscusión(persona, discusión)
        nodo_actual = self.apartados
        while nodo_actual is not None:
            if nodo_actual.apartado == apartado:
                nodo_puntos = nodo_actual.puntos
                while nodo_puntos is not None:
                    if nodo_puntos.punto == punto:
                        nodo_puntos.discusiones = self._agregar(nodo_puntos.discusiones, nueva_discusión)
                        break
                    nodo_puntos = nodo_puntos.sig
                break
            nodo_actual = nodo_actual.sig

    def _agregar(self, r, d):
        if r is None:
            return d
        else:
            r.sig = self._agregar(r.sig, d)
            return r

    @property
    def asDict(self):
        return {"Título":self.titulo,"fecha":self.fecha.__str__(),"participantes":self.participantes.asList}

def crear_agenda(titulo:str) -> None:
    """Función que crea una instancia de la clase Agenda.

    Args:
        titulo (str): Nombre de la agenda creada.
    """
    global agenda
    agenda = MiAgenda(titulo=titulo, fecha=datetime.today().strftime("%d/%m/%Y"))

class MiLista(Lista):
    def __init__(self) -> None:
        super().__init__()
    
    def _agregar(self,r ,e):
        if self==None:
            return e
        else:
            self.sig=self._agregar(r.sig,e)

class MiPersona(Persona):
    def __init__(self, nombre: str, apellido1: str, apellido2: str) -> None:
        super().__init__(nombre, apellido1, apellido2)

    def agregar (self,nombre: str, apellido1: str, apellido2: str):
        nueva_persona= MiPersona(nombre,apellido1,apellido2)
        self._agregar(self,nueva_persona)

    def _agregar(self,r,p):
        if r==None:
            return p
        else:
            r.sig=self._agregar(r.sig,p)
            return r # Conserva la referencias referencias anteriores

    @property
    def asList(self):
        if self==None:
            return []
        else:
            return self._asList(self)
        
    def _asList(self,r):
        r:MiPersona=r
        if r.sig==None:
            return [r.__str__()]
        else:
            return [r.__str__()]+self._asList(r.sig)
    
    def __str__(self) -> str:
        return ("{0} {1} {2}".format(self.nombre,self.apellido1,self.apellido2))
    
def agregar_participante(nombre: str, apellido1: str, apellido2: str) -> None:
    """Función que agrega un participante a la agenda.

    Args:
        nombre (str): Nombre del participante.
        apellido1 (str): Primer apellido del participante.
        apellido2 (str): Segundo apellido del participante.
    """
    global agenda
    agenda.agregar_participante(nombre, apellido1, apellido2)

def personas_asList() -> list:
    """Función que devuelve una lista con los participantes de la agenda.

    Returns:
        list: Lista con los participantes de la agenda.
    """
    global agenda
    try:
        return agenda.participantes.asList
    except:
        return []

class MiApartado(Apartados):
    def __init__(self, apartado: str) -> None:
        super().__init__(apartado)

    def agregar(self,apartado:str):
        nuevo_apartado= MiApartado(apartado)
        self._agregar(self,nuevo_apartado)

    def _agregar(self,r,a):
        if r==None:
            return a
        else:
            r.sig=self._agregar(r.sig,a)
            return r # Conserva la referencias referencias anteriores
        
    def obtener_puntos(self):
        result = []

        current = self.puntos
        while current is not None:
            result.append(current.punto)
            current = current.sig

        return result
        
    @property
    def asDict(self):
        result = {}

        current = self
        while current is not None:
            result[current.apartado] = current.obtener_puntos()
            current = current.sig

        return result

def agregar_apartado(apartado:str) -> None:
    """Función que agrega un apartado a la agenda.

    Args:
        apartado (str): Nombre del apartado.
    """
    global agenda
    agenda.agregar_apartado(apartado)

class MiPunto(Puntos):
    def __init__(self, punto: str) -> None:
        super().__init__(punto)

    @property
    def asList(self):
        if self==None:
            return []
        else:
            return self._asList(self)
        
    def _asList(self,r):
        r:MiPunto=r
        if r.sig==None:
            return [r.punto]
        else:
            return [r.punto]+self._asList(r.sig)
        
def agregar_punto(punto: str, apartado: str) -> None:
    """Función que agrega un punto a un apartado de la agenda.

    Args:
        punto (str): Nombre del punto.
        apartado (str): Nombre del apartado.
    """
    global agenda
    agenda.agregar_punto(punto, apartado)

class MiDiscusión(Discusion):
    def __init__(self,persona,discusión) -> None:
        super().__init__(persona,discusión)

def agregar_discusión(persona: str, apartado: str, punto: str, discusión: str) -> None:
    global agenda
    agenda.agregar_discusión(persona, apartado, punto, discusión)

def puntos_asDict() -> list:
    """Función que devuelve un diccionario con los apartados y sus puntos.

    Returns:
        list: Lista con los apartados y sus puntos.
    """
    global agenda
    try:
        return agenda.apartados.asDict
    except:
        return {"apartado": []}






def recorrer_arbol():
    global agenda
    
    apartado_actual = agenda.apartados
    while apartado_actual is not None:
        print("Apartado: ", apartado_actual.apartado)

        punto_actual = apartado_actual.puntos
        while punto_actual is not None:
            print("Punto: ", punto_actual.punto)

            discusion_actual = punto_actual.discusiones
            while discusion_actual is not None:
                print("Discusión: ", discusion_actual.discusion)
                print("Persona: ", discusion_actual.persona)
                discusion_actual = discusion_actual.sig

            punto_actual = punto_actual.sig

        apartado_actual = apartado_actual.sig