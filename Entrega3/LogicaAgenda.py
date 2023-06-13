from Agenda import agenda as Agenda, persona as Persona, apartados as Apartados, puntos as Puntos, discusion as Discusion, lista as Lista
from datetime import datetime

agenda = None # Instancia de la agenda

class MiAgenda(Agenda):
    """
    Estructura de datos tipo árbol m-vías para la representación de agendas
    """
    def __init__(self,titulo:str,fecha:datetime) -> None:
        """
        Constructor de la agenda

        Args:
            titulo (str): Título de la agenda
            fecha (datetime): Fecha de la agenda
        """
        super().__init__() # Inicializa el puntero de lista
        self.titulo:str=titulo # Título de la agenda
        self.fecha:datetime=fecha # Fecha de la agenda
        self.participantes:MiPersona=None # Listado de participantes
        self.apartados:MiApartado=None # Listado de apartados
        
    def crear_participante(self, nombre: str, apellido1: str, apellido2: str):
        """
        Método para agregar participantes a la agenda

        Args:
            nombre (str): Nombre del participante
            apellido1 (str): Primer apellido del participante
            apellido2 (str): Segundo apellido del participante
        """
        if self.participantes == None: # Si no hay participantes
            self.participantes = MiPersona(nombre=nombre, apellido1=apellido1, apellido2=apellido2) # Se crea el primer participante
        else: # Si ya hay participantes
            self.participantes.agregar(nombre, apellido1, apellido2) # Se agrega el participante

    def crear_apartado(self, apartado: str):
        """
        Método para agregar apartados a la agenda

        Args:
            apartado (str): Nombre del apartado
        """
        if self.apartados == None: # Si no hay apartados
            self.apartados = MiApartado(apartado) # Se crea el primer apartado
        else: # Si ya hay apartados
            self.apartados.agregar(apartado) # Se agrega el apartado

    def crear_punto(self, punto: str, apartado: str):
        """
        Método para agregar puntos a la agenda

        Args:
            punto (str): Nombre del punto
            apartado (str): Nombre del apartado
        """
        if self.apartados is not None: # Si hay apartados
            self.apartados.agregar_punto_recursivo(punto, apartado) # Se agrega el punto
        else: # Si no hay apartados
            self.apartados = MiApartado(apartado) # Se crea el primer apartado
            self.apartados.puntos = MiPunto(punto) # Se crea el primer punto

    def crear_discusion(self, persona, apartado, punto, discusion):
        """
        Método para agregar discusiones a la agenda

        Args:
            persona (str): Nombre de la persona que inicia la discusión
            apartado (str): Nombre del apartado
            punto (str): Nombre del punto
            discusión (str): Descripción de la discusión
        """
        nueva_discusion = MiDiscusion(persona, discusion) # Se crea la discusión
        nodo_actual = self.apartados # Se obtiene el primer apartado
        while nodo_actual is not None: # Se recorren los apartados
            if nodo_actual.apartado == apartado: # Si el apartado es el buscado
                nodo_puntos = nodo_actual.puntos # Se obtiene el primer punto
                while nodo_puntos is not None: # Se recorren los puntos
                    if nodo_puntos.punto == punto: # Si el punto es el buscado
                        nodo_puntos.discusiones = self._agregar(nodo_puntos.discusiones, nueva_discusion) # Se agrega la discusión
                        break # Se termina el ciclo
                    nodo_puntos = nodo_puntos.sig # Se obtiene el siguiente punto
                break # Se termina el ciclo
            nodo_actual = nodo_actual.sig # Se obtiene el siguiente apartado

    def _agregar(self, r, d):
        """
        Método recursivo para agregar discusiones a la agenda

        Args:
            r (MiDiscusion): Nodo actual
            d (MiDiscusion): Discusión a agregar
        """
        if r is None: # Si no hay discusiones
            return d # Se retorna la discusión
        else: # Si hay discusiones
            r.sig = self._agregar(r.sig, d) # Se agrega la discusión
            return r # Se retorna el nodo actual

    @property
    def asDict(self):
        """
        Método para obtener la agenda como un diccionario

        Returns:
            dict: Diccionario con la información de la agenda
        """
        return {"Título":self.titulo,"fecha":self.fecha.__str__(),"participantes":self.participantes.asList} # Se retorna la información de la agenda

def crear_agenda(titulo:str) -> None:
    """
    Función que crea una instancia de la clase Agenda.

    Args:
        titulo (str): Nombre de la agenda creada.
    """
    global agenda # Se declara la variable global
    agenda = MiAgenda(titulo=titulo, fecha=datetime.today().strftime("%d/%m/%Y")) # Se crea la agenda

class MiLista(Lista):
    """
    Clase que representa una lista enlazada

    Args:
        Lista (class): Lista enlazada
    """
    def __init__(self) -> None:
        """
        Constructor de la clase MiLista
        """
        super().__init__() # Inicializa el puntero de lista
    
    def _agregar(self,r ,e):
        """
        Método recursivo para agregar elementos a la lista

        Args:
            r (Nodo): Puntero al nodo actual durnte la recursión
            e (Any): Elemento que se desea agregar

        Returns:
            Nodo: Nodo actualizado con el elemento agregado
        """
        if self==None: # Si no hay elementos
            return e # Se retorna el elemento
        else: # Si hay elementos
            self.sig=self._agregar(r.sig,e) # Se agrega el elemento

class MiPersona(Persona):
    """
    Clase que representa una persona

    Args:
        Persona (class): Persona enlazada
    """
    def __init__(self, nombre: str, apellido1: str, apellido2: str) -> None:
        """
        Constructor de la clase MiPersona

        Args:
            nombre (str): Nombre de la persona
            apellido1 (str): Primer apellido de la persona
            apellido2 (str): Segundo apellido de la persona
        """
        super().__init__(nombre, apellido1, apellido2) # Inicializa la persona

    def agregar (self,nombre: str, apellido1: str, apellido2: str):
        """
        Método para agregar una persona a la lista

        Args:
            nombre (str): Nombre de la persona
            apellido1 (str): Primer apellido de la persona
            apellido2 (str): Segundo apellido de la persona
        """
        nueva_persona= MiPersona(nombre,apellido1,apellido2) # Se crea la persona
        self._agregar(self,nueva_persona) # Se agrega la persona

    def _agregar(self,r,p):
        """
        Método recursivo para agregar una persona a la lista

        Args:
            r (Nodo): Puntero al nodo actual durante la recursión
            p (MiPersona): Persona que se desea agregar

        Returns:
            Nodo: Nodo actualizado con la persona agregada
        """
        if r==None: # Si no hay personas
            return p # Se retorna la persona
        else: # Si hay personas
            r.sig=self._agregar(r.sig,p) # Se agrega la persona
            return r # Conserva la referencias referencias anteriores

    @property
    def asList(self):
        """
        Método para obtener la lista de personas

        Returns:
            list: Lista de personas
        """
        if self==None: # Si no hay personas
            return [] # Se retorna una lista vacía
        else: # Si hay personasdict
            return self._asList(self) # Se retorna la lista de personas
        
    def _asList(self,r):
        """
        Método recursivo para obtener la lista de personas

        Args:
            r (MiPersona): Puntero al nodo actual durante la recursión

        Returns:
            list: Lista de representaciones en cadena de las personas
        """
        r:MiPersona=r # Se declara la persona
        if r.sig==None: # Si no hay personas
            return [r.__str__()] # Se retorna la persona
        else: # Si hay personas
            return [r.__str__()]+self._asList(r.sig) # Se retorna la lista de personas
    
    def __str__(self) -> str:
        """
        Método para obtener la representación en cadena de la persona

        Returns:
            str: Representación en cadena de la persona
        """
        return ("{0} {1} {2}".format(self.nombre,self.apellido1,self.apellido2)) # Se retorna la representación en cadena de la persona
    
def crear_participante(nombre: str, apellido1: str, apellido2: str) -> None:
    """
    Función que agrega un participante a la agenda.

    Args:
        nombre (str): Nombre del participante.
        apellido1 (str): Primer apellido del participante.
        apellido2 (str): Segundo apellido del participante.
    """
    global agenda # Se declara la variable global
    agenda.crear_participante(nombre, apellido1, apellido2) # Se agrega el participante

def personas_asList() -> list:
    """
    Función que devuelve una lista con los participantes de la agenda.

    Returns:
        list: Lista con los participantes de la agenda.
    """
    global agenda # Se declara la variable global
    try: # Se intenta
        return agenda.participantes.asList # Se retorna la lista de participantes
    except: # Si no se puede
        return [] # Se retorna una lista vacía

class MiApartado(Apartados):
    """
    Clase que representa un apartado

    Args:
        Apartados (class): Apartado enlazado
    """
    def __init__(self, apartado: str) -> None:
        """
        Constructor de la clase MiApartado

        Args:
            apartado (str): Nombre del apartado
        """
        super().__init__(apartado) # Inicializa el apartado

    def agregar(self, apartado: str):
        """
        Método para agregar un apartado a la lista

        Args:
            apartado (str): Nombre del apartado
        """
        nuevo_apartado = MiApartado(apartado) # Se crea el apartado
        self._agregar_recursivo(self, nuevo_apartado) # Se agrega el apartado

    def agregar_punto_recursivo(self, punto: str, apartado: str):
        """
        Método recursivo para agregar un punto a un apartado

        Args:
            punto (str): Nombre del punto
            apartado (str): Nombre del apartado
        """
        if self.apartado == apartado: # Si el apartado es el mismo
            if self.puntos is None: # Si no hay puntos
                self.puntos = MiPunto(punto) # Se crea el punto
            else: # Si hay puntos
                self.puntos.agregar_punto_recursivo(punto) # Se agrega el punto
        elif self.sig is not None: # Si hay apartados
            self.sig.agregar_punto_recursivo(punto, apartado) # Se agrega el punto
        else: # Si no hay apartados
            nuevo_apartado = MiApartado(apartado) # Se crea el apartado
            nuevo_apartado.puntos = MiPunto(punto) # Se crea el punto
            self.sig = nuevo_apartado # Se agrega el apartado

    def _agregar_recursivo(self, r, a):
        """
        Método recursivo para agregar un apartado a la lista

        Args:
            r (MiApartado): Apartado actual durante la recursión
            a (MiApartado): Apartado que se desea agregar

        Returns:
            MiApartado: El apartado actual modificado con el apartado agregado
        """
        if r is None: # Si no hay apartados
            return a # Se retorna el apartado
        else: # Si hay apartados
            r.sig = self._agregar_recursivo(r.sig, a) # Se agrega el apartado
            return r # Se retorna el apartado
        
    def obtener_puntos(self):
        """
        Método para obtener los puntos de un apartado

        Returns:
            List[str]: Lista de puntos del apartado
        """
        result = [] # Se declara la lista de puntos

        current = self.puntos # Se declara el punto actual
        while current is not None: # Mientras haya puntos
            result.append(current.punto) # Se agrega el punto a la lista
            current = current.sig # Se pasa al siguiente punto

        return result # Se retorna la lista de puntos
        
    @property
    def asDict(self):
        """
        Método para obtener la representación en diccionario de los puntos

        Returns:
            dict: Representación en diccionario de los puntos
        """
        result = {} # Se declara el diccionario de puntos

        current = self # Se declara el apartado actual
        while current is not None: # Mientras haya apartados
            result[current.apartado] = current.obtener_puntos() # Se agrega el apartado y sus puntos al diccionario
            current = current.sig # Se pasa al siguiente apartado

        return result # Se retorna el diccionario de puntos

def crear_apartado(apartado:str) -> None:
    """
    Función que agrega un apartado a la agenda.

    Args:
        apartado (str): Nombre del apartado.
    """
    global agenda # Se declara la variable global
    agenda.crear_apartado(apartado) # Se agrega el apartado

class MiPunto(Puntos):
    """
    Clase que representa un punto

    Args:
        Puntos (class): Punto enlazado
    """
    def __init__(self, punto: str) -> None:
        """
        Constructor de la clase MiPunto

        Args:
            punto (str): Nombre del punto
        """
        super().__init__(punto) # Inicializa el punto

    def agregar_punto_recursivo(self, punto: str):
        """
        Método recursivo para agregar un punto a la lista
        
        Args:
            punto (str): Nombre del punto
        """
        if self.sig is None: # Si no hay puntos
            self.sig = MiPunto(punto) # Se crea el punto
        else: # Si hay puntos
            self.sig.agregar_punto_recursivo(punto) # Se agrega el punto

    @property
    def asList(self):
        """
        Método para obtener la representación en lista de los puntos

        Returns:
            list: Representación en lista de los puntos
        """
        if self==None: # Si no hay puntos
            return [] # Se retorna una lista vacía
        else: # Si hay puntos
            return self._asList(self) # Se retorna la lista de puntos
        
    def _asList(self,r):
        """
        Método recursivo para obtener la representación en lista de los puntos

        Args:
            r (MiPunto): Punto actual en el proceso de recursión

        Returns:
            list: Representación en lista de los puntos
        """
        r:MiPunto=r # Se declara el punto actual
        if r.sig==None: # Si no hay puntos
            return [r.punto] # Se retorna una lista con el punto
        else: # Si hay puntos
            return [r.punto]+self._asList(r.sig) # Se retorna la lista de puntos
        
def crear_punto(punto: str, apartado: str) -> None:
    """
    Función que agrega un punto a un apartado de la agenda.

    Args:
        punto (str): Nombre del punto.
        apartado (str): Nombre del apartado.
    """
    global agenda # Se declara la variable global
    agenda.crear_punto(punto, apartado) # Se agrega el punto

def puntos_asDict() -> dict:
    """
    Función que devuelve un diccionario con los apartados y sus puntos.

    Returns:
        dict: Diccionario con los apartados y sus puntos.
    """
    global agenda # Se declara la variable global
    try: # Se intenta
        return agenda.apartados.asDict # Se retorna el diccionario de puntos
    except: # Si no se puede
        return {"": ""} # Se retorna un diccionario vacío

class MiDiscusion(Discusion):
    """
    Clase que representa una discusión

    Args:
        Discusion (class): Discusión enlazada
    """
    def __init__(self,persona,discusion) -> None:
        """
        Constructor de la clase MiDiscusion

        Args:
            persona (str): Nombre de la persona
            discusion (str): Discusión
        """
        super().__init__(persona,discusion) # Inicializa la discusión

def crear_discusion(persona: str, apartado: str, punto: str, discusion: str) -> None:
    """
    Función que agrega una discusión a un punto de un apartado de la agenda.

    Args:
        persona (str): Nombre de la persona
        apartado (str): Nombre del apartado
        punto (str): Nombre del punto
        discusion (str): Discusión
    """
    global agenda # Se declara la variable global
    agenda.crear_discusion(persona, apartado, punto, discusion) # Se agrega la discusión
#-----------------------------------------------------------------------------------------------------------------------#
# Ciclos para generación del HTML
def obtener_nombre_fecha_agenda(agenda):
    """
    Función para obtener el nombre y la fecha de una agenda.

    Args:
        agenda (MiAgenda): Objeto de la clase MiAgenda.

    Returns:
        tuple: Tupla que contiene el nombre y la fecha de la agenda.
    """
    nombre = agenda.titulo
    fecha = agenda.fecha.strftime("%d/%m/%Y")
    return nombre, fecha

def obtener_apartados(self):
    """
    Método para obtener los apartados y sus respectivos puntos de la agenda

    Returns:
        dict: Diccionario con los apartados y sus puntos
    """
    if self.apartados is None: # Si no hay apartados
        return {} # Se retorna un diccionario vacío

    return self.apartados.asDict # Se retorna la representación en diccionario de los apartados y sus puntos

def generar_registro_discusion(self):
    """
    Método para generar el registro de la discusión de la agenda

    Returns:
        dict: Diccionario con la información de la discusión
    """
    registro_discusion = {} # Diccionario para almacenar la información de la discusión

    apartados = self.obtener_apartados() # Obtener los apartados y sus puntos

    for apartado, puntos in apartados.items(): # Iterar sobre los apartados y sus puntos
        for punto in puntos: # Iterar sobre los puntos
            discusiones = self.obtener_discusiones(apartado, punto) # Obtener las discusiones del punto
            if discusiones: # Si hay discusiones
                registro_discusion.setdefault(apartado, {}).setdefault(punto, discusiones) # Agregar las discusiones al registro

    return registro_discusion # Retornar el registro de la discusión

def obtener_discusiones(self, apartado, punto):
    """
    Método para obtener las discusiones de un punto de un apartado

    Args:
        apartado (str): Nombre del apartado
        punto (str): Nombre del punto

    Returns:
        list: Lista de discusiones del punto
    """
    nodo_actual = self.apartados # Se obtiene el primer apartado
    while nodo_actual is not None: # Se recorren los apartados
        if nodo_actual.apartado == apartado: # Si el apartado es el buscado
            nodo_puntos = nodo_actual.puntos # Se obtiene el primer punto
            while nodo_puntos is not None: # Se recorren los puntos
                if nodo_puntos.punto == punto: # Si el punto es el buscado
                    return nodo_puntos.obtener_discusiones() # Se retornan las discusiones del punto
                nodo_puntos = nodo_puntos.sig # Se obtiene el siguiente punto
            break # Se termina el ciclo
        nodo_actual = nodo_actual.sig # Se obtiene el siguiente apartado

    return [] # Si no se encontró el apartado o el punto, se retorna una lista vacía

def generar_registro_discusion() -> dict:
    """
    Función que genera el registro de discusión de la agenda.

    Returns:
    dict: Registro de discusión.
    """
    global agenda # Se declara la variable global
    return agenda.asDict # Se retorna el registro de discusión