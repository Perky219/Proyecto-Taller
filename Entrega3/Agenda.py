class lista:
    """
    Estructura base de lista para ser heredada por otras clases que requieran su definición como lista de punteros
    """
    def __init__(self) -> None:
        """
        Construtor de la clase lista, inicaliza el puntero siguiente
        """
        self.sig:lista=None # Puntero siguiente

class persona(lista):
    """
    Estructura de datos tipo lista punteros para el registro de personas
    """
    def __init__(self, nombre: str, apellido1:str, apellido2:str) -> None:
        """
        Constructor de la clase personas

        Args:
            nombre (str): Nombre de la persona
            apellido1 (str): Primer apellido de la persona
            apellido2 (str): Segundo apellido de la persona
        """
        super().__init__() # Inicaliza el puntero de lista
        self.nombre:str=nombre # Nombre de la persona
        self.apellido1:str=apellido1 # Primer apellido de la persona
        self.apellido2:str=apellido2 # Segundo apellido de la persona

class discusion(lista):
    """
    Estructura de datos tipo lista, para el registro de discusiones tratadas en los puntos de agenda
    """
    def __init__(self, persona:persona, discusion:str) -> None:
        """
        Constructor de discusiones

        Args:
            persona (persona): Persona quien emite la discusión
            discusion (str): trasncripción de lo comentado en la discusión
        """
        super().__init__() # Inicializa el puntero de lista
        self.persona:persona=persona # Persona quien realiza la discusión
        self.discusion:str=discusion # Transcrición o SpeechRecognition de lo expuesto por la persona

class puntos(lista):
    """
    Estructura de datos tipo árbol m-vías para la representación de puntos de agenda
    """
    def __init__(self,punto:str) -> None:
        """
        Constructor del tercer nivel del árbol de agenda (puntos)

        Args:
            punto (str): Descripción del tema a tratar
        """
        super().__init__() # Inicializa el puntero de lista
        self.punto:str=punto # Descrición del punto
        self.discusiones:discusion=None # Listado de discusiones del punto

class apartados(lista):
    """
    Estructura de datos tipo árbol m-vías para la representación de apartados de agenda
    """
    def __init__(self,apartado:str) -> None:
        """
        Constructor del tercer nivel del árbol de agenda (apartados)

        Args:
            apartado (str): Descripción del apartado
        """
        super().__init__() # Inicializa el puntero de lista
        self.apartado:str=apartado # Descripcion del apartado
        self.puntos:puntos=None # Listado de puntos de agenda por apartado

class agenda:
    """
    Estructura de datos tipo árbol m-vías para la representación de agendas
    """
    def __init__(self) -> None:
        """
        Constructor de la agenda
        """
        self.participantes:persona=None # Listado de participantes
        self.apartados:apartados=None # Listado de apartados