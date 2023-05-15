import os
import speech_recognition as sr
import time
import tkinter as tk
participantes = set()
agenda = set()
text_cap = {}

def lista_participantes():
    """
    Se creará un conjunto de participantes, en el cual cada uno de los integrantes, tendrá un número de carnet.

    Returns:
        set: Conjunto de participantes completo.
    """
    # Se crea un conjunto vacío para almacenar los nombres y carnets de los participantes.
    global participantes

    # Se solicita al usuario que ingrese los nombres y carnets de los participantes.
    while True:
        nombre = input("Ingrese el nombre completo del participante o escriba 'fin' para terminar: ")
        if nombre.lower() == "fin":
            break
        carnet = input("Ingrese el número de carnet del participante: ")

        # Se comprueba si el número de carnet ya ha sido registrado previamente.
        if any(participante.startswith(carnet) for participante in participantes):
            print("Error: el número de carnet ya ha sido registrado")
        else:
            participantes.add(f"{carnet} - {nombre}")
    
    return participantes

def registro_agenda():
    """
    Se creará un registro de agenda, que estará dividida en apartados, donde cada uno de estos tendrá puntos.

    Args:
        agenda (set): Conjunto de apartados y sus puntos.
        puntos (list): Lista de puntos de un apartado.
        respuesta (str): Respuesta de la persona a la pregunta '¿Agregar otro punto/apartado?'.

    Attributes:
        nombre_apartado (str): Apartado que se va agregar a la agenda.
        nombre_punto (str): Punto que se va a agregar a la agenda.

    Returns:
        set: Conjunto de apartados y sus puntos.
    """

    # Se inicializa la variable agenda como un conjunto vacío.
    global agenda

    # Se solicita el nombre del primer apartado.
    while True:
        nombre_apartado = input("Ingrese el nombre del apartado o escriba 'fin' para terminar el registro de la agenda: ")
        if nombre_apartado.lower() == "fin":
            break

        # Se verifica si el apartado ya existe en la agenda.
        for apartado in agenda:
            if apartado[0] == nombre_apartado:
                print(f"El apartado '{nombre_apartado}' ya existe en la agenda.")
                break
        else:
            # Se inicializa la variable puntos como una lista vacía.
            puntos = []

            # Se solicitan los puntos del apartado.
            while True:
                nombre_punto = input("Ingrese el nombre del punto o escriba 'fin' para terminar el apartado: ")
                if nombre_punto.lower() == "fin":
                    break

                # Se verifica si el punto ya existe en el apartado actual.
                if nombre_punto in puntos:
                    print(f"El punto '{nombre_punto}' ya está en el apartado actual.")
                else:
                    # Se agrega el punto a la lista de puntos del apartado actual.
                    puntos.append(nombre_punto)

            # Se convierte la lista de puntos en una tupla y se agrega el apartado y sus puntos al conjunto de la agenda.
            agenda.add((nombre_apartado, tuple(puntos)))

    return agenda

def seleccionar_participante(participantes):
    """
    Permite seleccionar un participante del conjunto de participantes a través de un índice numérico.

    Args:
        participantes (set): Conjunto de participantes.

    Returns:
        str: Nombre completo y número de carnet del participante seleccionado.
    """
    # Convertir el conjunto de participantes a una lista para poder indexar.
    lista_participantes = list(participantes)

    # Imprimir la lista de participantes con índices numéricos.
    print("Seleccione un participante por su índice:")
    for i, participante in enumerate(lista_participantes):
        print(f"{i+1}. {participante}")

    # Solicitar al usuario que ingrese el número correspondiente al participante deseado.
    while True:
        try:
            num_participante = int(input("Número del participante: "))
            if num_participante < 1 or num_participante > len(participantes):
                print("Error: seleccione un número válido")
            else:
                break
        except ValueError:
            print("Error: seleccione un número válido")

    # Retornar el participante seleccionado.
    return lista_participantes[num_participante-1]

def seleccionar_espacio_agenda(agenda):
    """
    Permite seleccionar un apartado y un punto específico dentro de la agenda.

    Args:
        agenda (set): Conjunto de apartados y sus puntos.

    Returns:
        tuple: Tupla con el nombre del apartado y el nombre del punto seleccionado.
    """
    # Se convierte el conjunto de la agenda en una lista para poder indexar los elementos.
    agenda_list = list(agenda)
    
    # Se verifica si la agenda está vacía.
    if not agenda_list:
        print("No hay apartados registrados en la agenda.")
        return None

    # Se muestra una lista de los nombres de los apartados registrados.
    print("Apartados disponibles:")
    for i, apartado in enumerate(agenda_list):
        print(f"{i+1}. {apartado[0]}")

    # Se solicita el número correspondiente al apartado deseado.
    while True:
        seleccion = input("Seleccione un apartado (ingrese el número correspondiente): ")
        try:
            seleccion = int(seleccion)
            if seleccion < 1 or seleccion > len(agenda_list):
                raise ValueError
            break
        except ValueError:
            print("Error: selección inválida.")

    # Se obtiene el apartado correspondiente a la selección y se muestra una lista de los puntos del apartado.
    apartado = agenda_list[seleccion-1]
    print(f"Puntos del apartado '{apartado[0]}':")
    for i, punto in enumerate(apartado[1]):
        print(f"{i+1}. {punto}")

    # Se solicita el número correspondiente al punto deseado.
    while True:
        seleccion = input("Seleccione un punto (ingrese el número correspondiente): ")
        try:
            seleccion = int(seleccion)
            if seleccion < 1 or seleccion > len(apartado[1]):
                raise ValueError
            break
        except ValueError:
            print("Error: selección inválida.")

    # Se obtiene el punto correspondiente a la selección y se devuelve la tupla con el nombre del apartado y del punto.
    punto = apartado[1][seleccion-1]
    return apartado[0], punto

def speech(participantes, agenda):
    """
    Reconocedor de voz que imprime lo dicho por el usuario y la hora en que se inició.

    Args:
        participantes (dict): Diccionario que contiene los participantes.
        agenda (dict): Diccionario que contiene la agenda.

    Returns:
        dict: Retorna el diccionario 'text_cap' que contiene el registro de participaciones.
    """
    r = sr.Recognizer()
    i = 0
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
                    ultima_participacion = {
                        'participante': participante,
                        'apartado': apartado,
                        'hora': time.strftime("%H:%M:%S"),
                        'texto': text
                    }
                    text_cap.append(ultima_participacion)
            except sr.UnknownValueError:
                print("No se pudo entender lo que dijiste.")
                i += 1
            except sr.RequestError as e:
                print("No se pudo conectar al servicio de reconocimiento de voz; {0}".format(e))
                i += 1
    print("Fin del reconocimiento de voz.")
    return text_cap
#---------------------------------------------------------------------------------------------------#
# def primer_reporte():
#     """
#     Esta función imprime la lista de participantes, la agenda completa y las transcripciones de cada participante.

#     Args:
#         participante (str): Condicional de un ciclo for que toma las credenciales de cada participante para imprimir.
#         puntos (tuple): Condicional de un ciclo for que toma el valor de cada sección de la agenda.
#         punto (str): Condicional de ciclo for anidado que toma el valor de un punto específico de cada sección de la agenda.
#         i (list): Toma cada sublista como condicional de un ciclo for, para poder hacer una impresión.
#     """
#     # Se imprime la lista de participantes.
#     print("\nLista de participantes:")
#     for participante in participantes:
#         print(participante["nombre"] + " - " + participante["carnet"])

#     # Se imprime la agenda completa.
#     print("\nAgenda:")
#     for apartado, puntos in agenda:
#         print(apartado)
#         for punto in puntos:
#             print(" - " + punto+'\n')

#     # Imprimir transcripciones de cada participante
#     for i in text_cap:
#         print(f"{i[0]['nombre']} en el punto '{i[1][1]}' del apartado '{i[1][0]}' a las {i[2]} dijo: '{i[3][0]}'\n")

# def segundo_reporte():
#     """
#     Esta función cuenta la cantidad de palabras reconocidas por participante y las imprime en orden descendente.

#     Args:
#         palabras_por_participante (dict): Diccionario que contendrá las palabras que dice cada participante.
#         transcripcion (list): Toma el valor de las sublistas dentro de "text_cap".
#         participante (str): Toma el nombre de cada participante contenido en "text_cap".
#         palabras (int): Valor numérico del total de palabras.
#         ordenado (dict): Contiene las personas ordenadas por cantidad de palabras.
#         cantidad_palabras (int): Condicional del ciclo for que toma el valor de la cantidad de palabras de cada participante dentro de "ordenado".
#     """
#     # Diccionario para almacenar la cantidad de palabras reconocidas de cada participante.
#     palabras_por_participante = {}

#     # Recorremos las transcripciones y contamos las palabras de cada participante.
#     for transcripcion in text_cap:
#         participante = transcripcion[0]["nombre"]
#         palabras = len(transcripcion[3][0].split())
#         if participante in palabras_por_participante:
#             palabras_por_participante[participante] += palabras
#         else:
#             palabras_por_participante[participante] = palabras

#     # Ordenamos el diccionario en base a la cantidad de palabras reconocidas.
#     ordenado = sorted(palabras_por_participante.items(), key=lambda x: x[1], reverse=True)

#     # Imprimimos el resultado.
#     print("\nCantidad de palabras reconocidas por participante:")
#     for participante, cantidad_palabras in ordenado:
#         print(f"{participante}: {cantidad_palabras} palabras")

# def tercer_reporte():
#     """
#     Esta función cuenta la cantidad total de participaciones por persona y por punto, y también imprime el listado de personas que participaron por punto.

#     Args:
#         participaciones_por_punto (dict): Diccionario que registra las participaciones por punto de cada persona.
#         personas_por_punto (dict): Diccionario que registra las personas que participaron por punto.
#         transcripcion (list): Recorre la lista "text_cap" y toma el valor de las listas dentro de esta.
#         nombre (str): Valor de nombre que se toma dentro de las sublistas en "text_cap".
#         punto (str): Valor de punto que se toma dentro de las sublistas en "text_cap".
#         participo (bool): Condicional que toma valor inicial en False para realizar comparaciones.
#     """
#     # Diccionario para la cantidad de participaciones por persona y por punto.
#     participaciones_por_punto = {}

#     # Diccionario para el listado de personas que participaron por punto.
#     personas_por_punto = {}

#     # Recorrer las transcripciones.
#     for transcripcion in text_cap:
#         nombre = transcripcion[0]["nombre"]
#         punto = transcripcion[1]
        
#         # Actualizar la cantidad de participaciones por persona y por punto.
#         if nombre not in participaciones_por_punto:
#             participaciones_por_punto[nombre] = {}
#         if punto not in participaciones_por_punto[nombre]:
#             participaciones_por_punto[nombre][punto] = 0
#         participaciones_por_punto[nombre][punto] += 1
        
#         # Actualizar el listado de personas que participaron por punto.
#         if punto not in personas_por_punto:
#             personas_por_punto[punto] = []
#         participo = False
#         for i, tupla in enumerate(personas_por_punto[punto]):
#             if tupla[0] == nombre:
#                 personas_por_punto[punto][i] = (nombre, tupla[1] + 1)
#                 participo = True
#                 break
#         if not participo:
#             personas_por_punto[punto].append((nombre, 1))

#     # Imprimir la cantidad total de participaciones por persona y por punto.
#     print("\nCantidad total de participaciones por persona y por punto:")
#     for nombre, participaciones in participaciones_por_punto.items():
#         print(f"\n{nombre}:")
#         for punto, cantidad in participaciones.items():
#             print(f"  - En el apartado {punto[0]}, punto {punto[1]}: {cantidad}")

#     # Imprimir el listado de personas que participaron por punto.
#     print("\nListado de personas que participaron por punto:")
#     for punto, personas in personas_por_punto.items():
#         print(f"\nApartado {punto[0]}, punto {punto[1]}:")
#         for persona in personas:
#             print(f"  - {persona[0]}: {persona[1]} veces")

# def menu_reportes():
#     """
#     Función que muestra un menú para seleccionar uno de los tres reportes disponibles y lo genera.

#     Attributes:
#         opcion (str): Opción seleccionada por el usuario.
#     """
#     while True:
#         print("\n--- MENÚ DE REPORTES ---")
#         print("1. Reporte de participaciones por apartado de la agenda")
#         print("2. Reporte de cantidad total de palabras reconocidas por persona")
#         print("3. Reporte de cantidad total de participaciones por persona y por punto de la agenda")
#         print("4. Salir")
#         opcion = input("Seleccione el número del reporte que desea generar: ")
        
#         if opcion == "1":
#             os.system('clear')
#             primer_reporte()
#         elif opcion == "2":
#             os.system('clear')
#             segundo_reporte()
#         elif opcion == "3":
#             os.system('clear')
#             tercer_reporte()
#         elif opcion == "4":
#             os.system('clear')
#             print("¡Hasta luego!")
#             time.sleep(3)
#             os.system('clear')
#             break
#         else:
#             print("Opción inválida, por favor intente de nuevo.")

# def menu_principal():
#     """
#     Función que genera un menú en terminal, en dónde el usuario puede seleccionar distintas opciones para ejecutar lo que prefiera.

#     Attributes:
#         opcion (str): Opción seleccionada por el usuario.
#     """
#     while True:
#         os.system('clear')
#         print("Menú:")
#         print("1. Registrar participantes")
#         print("2. Definir agenda")
#         print("3. Reconocimiento de voz")
#         print("4. Generar reportes")
#         print("5. Salir")
#         opcion = input("Ingrese la opción deseada: ")

#         if opcion == "1":
#             os.system('clear')
#             lista_participantes()
#         elif opcion == "2":
#             os.system('clear')
#             registro_agenda()
#         elif opcion == "3":
#             os.system('clear')
#             speech(participantes, agenda)
#         elif opcion == "4":
#             os.system('clear')
#             menu_reportes()
#         elif opcion=="5":
#             os.system('clear')
#             print("¡Gracias por utilizar nuestro programa!")
#             time.sleep(3)
#             os.system('clear')
#             break
#         else:
#             print("Opción no válida.")

# menu_principal()