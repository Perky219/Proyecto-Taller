import os
import speech_recognition as sr
import time
text_cap = []

def lista_participantes():
    """
    Se creará una lista de participantes, en la cual cada uno de los integrantes, tendrá un número de carnet.

    Args:
        participantes (list): Lista de participantes completa.
        carnet_existente (bool): Variable que se genera para realizar comparación de existencia, definida default como 'False'.
        participante (dict): Toma el valor de cada diccionario dentro del ciclo 'for'.
        participantes_str (str): Lista de participantes en string (solo para impresión).

    Attributes:
        nombre (str): Nombre que se le asignará a cada integrante.
        carnet (int): Carnet que se le asignará a cada integrante.
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
        agenda (list): Apartados dentro de la agenda.
        puntos (list): Puntos dentro de la agenda.
        respuesta (str): Respuesta de la persona a la pregunta '¿Agregar otro punto/apartado?'.

    Attributes:
        nombre_apartado (str): Apartado que se va agregar a la agenda.
        nombre_punto (str): Punto que se va a agregar a la agenda.
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
        i (int): Da la numeracion a cada participante de la lista

    Attributes:
        seleccion (int): Contiene el indice de la persona seleccionada
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
        i (int): Da una enumeracion a cada apartado y punto.
        agenda (list): Es una lista de tuplas, donde cada tupla contiene un apartado y una lista de puntos correspondientes a ese apartado.
        apartado (list): Almacena el nombre del apartado seleccionado por el usuario a partir de la lista agenda.
        punto (list): Almacena el punto específico seleccionado por el usuario a partir de la lista agenda.

    Attributes:
        seleccion_apartado (int): Contiene el indice del apartado a seleccionar.
        seleccion_punto (int): Contiene el indice del punto a seleccionar.

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
        text_cap (list): Lista que contiene el texto entendido.
        i (int): Contador de errores.
        text_cap (list): Almacena el texto capturado.
        r (Recognizer): Realiza la tarea de reconocimiento de voz.
        audio (AudioData): Almacena el audio capturado por el micrófono.
        
    Returns:
        list: Retorna la lista 'text_cap' que contiene el texto entendido.
    """
    r = sr.Recognizer()
    i = 0
    global text_cap
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
    """_summary_
    """
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

def segundo_reporte():
    """_summary_
    """
    # Diccionario para almacenar la cantidad de palabras reconocidas de cada participante.
    palabras_por_participante = {}

    # Recorremos las transcripciones y contamos las palabras de cada participante.
    for transcripcion in text_cap:
        participante = transcripcion[0]["nombre"]
        palabras = len(transcripcion[3][0].split())
        if participante in palabras_por_participante:
            palabras_por_participante[participante] += palabras
        else:
            palabras_por_participante[participante] = palabras

    # Ordenamos el diccionario en base a la cantidad de palabras reconocidas.
    ordenado = sorted(palabras_por_participante.items(), key=lambda x: x[1], reverse=True)

    # Imprimimos el resultado.
    print("\nCantidad de palabras reconocidas por participante:")
    for participante, cantidad_palabras in ordenado:
        print(f"{participante}: {cantidad_palabras} palabras")

def tercer_reporte():
    """_summary_
    """
    # Diccionario para la cantidad de participaciones por persona y por punto.
    participaciones_por_punto = {}

    # Diccionario para el listado de personas que participaron por punto.
    personas_por_punto = {}

    # Recorrer las transcripciones.
    for transcripcion in text_cap:
        nombre = transcripcion[0]["nombre"]
        punto = transcripcion[1]
        
        # Actualizar la cantidad de participaciones por persona y por punto.
        if nombre not in participaciones_por_punto:
            participaciones_por_punto[nombre] = {}
        if punto not in participaciones_por_punto[nombre]:
            participaciones_por_punto[nombre][punto] = 0
        participaciones_por_punto[nombre][punto] += 1
        
        # Actualizar el listado de personas que participaron por punto.
        if punto not in personas_por_punto:
            personas_por_punto[punto] = []
        participo = False
        for i, tupla in enumerate(personas_por_punto[punto]):
            if tupla[0] == nombre:
                personas_por_punto[punto][i] = (nombre, tupla[1] + 1)
                participo = True
                break
        if not participo:
            personas_por_punto[punto].append((nombre, 1))

    # Imprimir la cantidad total de participaciones por persona y por punto.
    print("\nCantidad total de participaciones por persona y por punto:")
    for nombre, participaciones in participaciones_por_punto.items():
        print(f"\n{nombre}:")
        for punto, cantidad in participaciones.items():
            print(f"  - En el apartado {punto[0]}, punto {punto[1]}: {cantidad}")

    # Imprimir el listado de personas que participaron por punto.
    print("\nListado de personas que participaron por punto:")
    for punto, personas in personas_por_punto.items():
        print(f"\nApartado {punto[0]}, punto {punto[1]}:")
        for persona in personas:
            print(f"  - {persona[0]}: {persona[1]} veces")

def menu_reportes():
    """
    Función que muestra un menú para seleccionar uno de los tres reportes disponibles y lo genera.

    Attributes:
        opcion (str): Opción seleccionada por el usuario.
    """
    while True:
        print("\n--- MENÚ DE REPORTES ---")
        print("1. Reporte de participaciones por apartado de la agenda")
        print("2. Reporte de cantidad total de palabras reconocidas por persona")
        print("3. Reporte de cantidad total de participaciones por persona y por punto de la agenda")
        print("4. Salir")
        opcion = input("Seleccione el número del reporte que desea generar: ")
        
        if opcion == "1":
            os.system('clear')
            primer_reporte()
            os.system('clear')
        elif opcion == "2":
            os.system('clear')
            segundo_reporte()
            os.system('clear')
        elif opcion == "3":
            os.system('clear')
            tercer_reporte()
            os.system('clear')
        elif opcion == "4":
            os.system('clear')
            print("¡Hasta luego!")
            time.sleep(3)
            os.system('clear')
            break
        else:
            print("Opción inválida, por favor intente de nuevo.")

def menu_principal():
    """
    Función que genera un menú en terminal, en dónde el usuario puede seleccionar distintas opciones para ejecutar lo que prefiera.

    Attributes:
        opcion (str): Opción seleccionada por el usuario.
    """
    while True:
        os.system('clear')
        print("Menú:")
        print("1. Registrar participantes")
        print("2. Definir agenda")
        print("3. Reconocimiento de voz")
        print("4. Generar reportes")
        print("5. Salir")
        opcion = input("Ingrese la opción deseada: ")

        if opcion == "1":
            os.system('clear')
            lista_participantes()
        elif opcion == "2":
            os.system('clear')
            registro_agenda()
        elif opcion == "3":
            os.system('clear')
            speech()
        elif opcion == "4":
            os.system('clear')
            menu_reportes()
        elif opcion=="5":
            os.system('clear')
            print("¡Gracias por utilizar nuestro programa!")
            time.sleep(3)
            os.system('clear')
            break
        else:
            print("Opción no válida.")

menu_principal()