import os
import speech_recognition as sr
import time

def lista_participantes():
    """
    Se creará una lista de participantes, en la cual cada uno de los integrantes, tendrá un número de carnet.

    Args:
        nombre (str): Nombre que se le asignará a cada integrante.
        carnet (int): Carnet que se le asignará a cada integrante.
        carnet_existente (bool): Variable que se genera para realizar comparación de existencia, definida default como 'False'.
        participante (dict): Toma el valor de cada diccionario dentro del ciclo 'for'.
        participantes_str (str): Lista de participantes en string (solo para impresión).

    Attributes:
        participantes (list): Lista de participantes completa.
    """
    # Se crea una lista vacía para almacenar los nombres y carnets de los participantes.
    global participantes
    participantes=[]

    # Se solicita al usuario que ingrese los nombres y carnets de los participantes.
    while True:
        nombre=input("Ingrese el nombre completo del participante o escriba 'fin' para terminar: ")
        if nombre.lower()=="fin":
            break
        carnet=input("Ingrese el número de carnet del participante: ")
        
        # Se comprueba si el número de carnet ya ha sido registrado previamente.
        carnet_existente=False
        for participante in participantes:
            if participante["carnet"]==carnet:
                print("Error: el número de carnet ya ha sido registrado para", participante["nombre"])
                carnet_existente=True
                break

        # Se comprueba que el número de carnet sea un valor numérico.
        if not carnet.isdigit():
            print("Error: el número de carnet debe ser un valor numérico")
        elif not carnet_existente:
            participantes.append({"nombre": nombre, "carnet": carnet})

def registro_agenda():
    """
    Se creará un registro de agenda, que estará dividida en apartados, donde cada uno de estos tendrá puntos.

    Args:
        nombre_apartado (str): Apartado que se va agregar a la agenda.
        nombre_punto (str): Punto que se va a agregar a la agenda.
        respuesta (str): Respuesta de la persona a la pregunta '¿Agregar otro punto/apartado?'.

    Attributes:
        agenda (list): Apartados dentro de la agenda.
        puntos (list): Puntos dentro de la agenda.
    """
    global agenda
    agenda=[]
    while True:
        # Se solicita el nombre del apartado.
        nombre_apartado=input("Ingrese el nombre del apartado o escriba 'fin' para terminar el registro de la agenda: ")
        if nombre_apartado.lower()=="fin":
            break
        
        # Se verifica si el apartado ya existe.
        if nombre_apartado in [a[0] for a in agenda]:
            print(f"El apartado '{nombre_apartado}' ya existe en la agenda.")
            continue
        
        # Se solicitan los puntos del apartado.
        global puntos
        puntos=[]
        while True:
            nombre_punto=input("Ingrese el nombre del punto o escriba 'fin' para terminar el apartado: ")
            if nombre_punto.lower()=="fin":
                break
            
            # Se verifica si el punto ya existe en el apartado actual.
            if nombre_punto in puntos:
                print(f"El punto '{nombre_punto}' ya está en el apartado actual.")
                continue
            
            puntos.append(nombre_punto)
        
        # Se agrega el apartado y sus puntos a la agenda.
        agenda.append((nombre_apartado, puntos))

def seleccionar_participante(participantes):
    """
    Permite al usuario seleccionar una persona registrada de la lista de participantes.

    Args:
        participantes (list): Lista de participantes registrados.
        seleccion (int): Contiene el indice de la persona seleccionada
        i (int): Da la numeracion a cada participante de la lista


    """
    # Mostrar la lista de participantes
    print("Seleccione una persona registrada:")
    for i, participante in enumerate(participantes):
        print(f"{i+1}. {participante['nombre']} ({participante['carnet']})")

    # Pedir al usuario que seleccione un participante
    while True:
        try:
            seleccion = int(input("Ingrese el número de la persona que desea seleccionar: "))
            if seleccion < 1 or seleccion > len(participantes):
                print(f"Error: el número debe estar entre 1 y {len(participantes)}")
            else:
                return participantes[seleccion-1]
        except ValueError:
            print("Error: debe ingresar un número")

def seleccionar_espacio_agenda(agenda):
    """
    Permite al usuario seleccionar un punto específico de la agenda.

    Args:
        agenda (list): Lista de apartados y puntos de la agenda.
        i (int): Da una enumeracion a cada apartado y punto
        seleccion_apartado (int): Contiene el indice del apartado a seleccionar
        agenda (list): Es una lista de tuplas, donde cada tupla contiene un apartado y una lista de puntos correspondientes a ese apartado.
        apartado (list): Almacena el nombre del apartado seleccionado por el usuario a partir de la lista agenda
        punto (list):Almacena el punto específico seleccionado por el usuario a partir de la lista agenda.

    Returns:
        tuple: Tupla con el apartado y punto seleccionados.
    """
    # Mostrar la lista de apartados y puntos
    print("Seleccione un apartado y punto de la agenda:")
    for i, (apartado, puntos) in enumerate(agenda):
        print(f"{i+1}. {apartado}:")
        for j, punto in enumerate(puntos):
            print(f"\t{j+1}. {punto}")

    # Pedir al usuario que seleccione un apartado y punto
    while True:
        try:
            seleccion_apartado = int(input("Ingrese el número del apartado que desea seleccionar: "))
            if seleccion_apartado < 1 or seleccion_apartado > len(agenda):
                print(f"Error: el número debe estar entre 1 y {len(agenda)}")
                continue

            seleccion_punto = int(input("Ingrese el número del punto que desea seleccionar: "))
            if seleccion_punto < 1 or seleccion_punto > len(agenda[seleccion_apartado-1][1]):
                print(f"Error: el número debe estar entre 1 y {len(agenda[seleccion_apartado-1][1])}")
                continue

            apartado = agenda[seleccion_apartado-1][0]
            punto = agenda[seleccion_apartado-1][1][seleccion_punto-1]
            return (apartado, punto)

        except ValueError:
            print("Error: debe ingresar un número")

def speech():
    """
    Reconocedor de voz que imprime lo dicho por el usuario y la hora en que se inició.

    Args:
        i (int): Contador de errores.
        text_cap (list): Almacena el texto capturado.
        r (Recognizer): Realiza la tarea de reconocimiento de voz.
        audio (AudioData): Almacena el audio capturado por el micrófono.

    Atributos:
        text_cap (list): Lista que contiene el texto entendido.

    Returns:
        list: Returna la lista 'text_cap' que contiene el texto entendido.
    """
    r = sr.Recognizer()
    i = 0
    text_cap = []
    participante = seleccionar_participante(participantes)
    apartado = seleccionar_espacio_agenda(agenda)
    start_time = time.time()
    print("Habla ahora...")
    with sr.Microphone() as source:
        while (time.time() - start_time) < 30: # Límite de 30 segundos para la ejecución de la función
            r.energy_threshold = 700
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language='es-ES')
                print("Hablaste a las", time.strftime("%Y-%m-%d %H:%M:%S"), "y dijiste:", text)
                if text.lower() == "finalizar":
                    break
                else:
                    ultima_participacion = [participante, apartado, time.strftime("%H:%M:%S"), [text]]
                    text_cap.append(ultima_participacion)
                    i = 0
            except sr.UnknownValueError:
                print("No se pudo entender lo que dijiste.")
                i += 1
            except sr.RequestError as e:
                print("No se pudo conectar al servicio de reconocimiento de voz; {0}".format(e))
                i += 1
    print("Fin del reconocimiento de voz.")
    return text_cap

def primer_reporte():
    # Se imprime la lista de participantes.
    print("\nLista de participantes:")
    for participante in participantes:
        print(participante["nombre"] + " - " + participante["carnet"])

    # Se imprime la agenda completa.
    print("\nAgenda:")
    for apartado, puntos in agenda:
        print(apartado)
        for punto in puntos:
            print(" - " + punto+'\n')

    # Imprimir transcripciones de cada participante
    for i in text_cap:
        print(f"{i[0]['nombre']} en el punto '{i[1][1]}' del apartado '{i[1][0]}'a las {i[2]} dijo: '{i[3][0]}'\n")