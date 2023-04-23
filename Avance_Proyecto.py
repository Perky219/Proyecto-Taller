import speech_recognition as sr
import datetime
import time
import os

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
    # Se crea una lista vacía para almacenar los nombres y carnets de los participantes
    global participantes
    participantes=[]

    # Se solicita al usuario que ingrese los nombres y carnets de los participantes
    while True:
        nombre=input("Ingrese el nombre completo del participante o escriba 'fin' para terminar: ")
        if nombre.lower()=="fin":
            break
        carnet=input("Ingrese el número de carnet del participante: ")
        # Se valida si el número de carnet ya ha sido registrado previamente
        carnet_existente=False
        for participante in participantes:
            if participante["carnet"]==carnet:
                print("Error: el número de carnet ya ha sido registrado para", participante["nombre"])
                carnet_existente=True
                break

        # Se valida que el número de carnet sea un valor numérico.
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
        nombre_apartado=input("Ingrese el nombre del apartado o escriba 'fin' para terminar: ")
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

def speech():
    """
    Se hará un reconocimiento de voz que imprime lo dicho por el usuario, seleccionando qué participante es el que habla y en qué apartado lo hace.

    Args: 
        asd

    Attributes: 
        asd
    """
    # Se selecciona apartado y punto de la agenda.
    print("Seleccione un apartado:")
    for i, apartado in enumerate(agenda):
        print(f"{i + 1}. {apartado[0]}")
    seleccion_apartado=int(input("Ingrese el número del apartado: "))

    # Se obtiene el nombre del apartado seleccionado.
    apartado_seleccionado=agenda[seleccion_apartado - 1][0]

    # Se solicita al usuario la selección del punto de agenda.
    print(f"Seleccione un punto de agenda para {apartado_seleccionado}:")
    for i, punto in enumerate(agenda[seleccion_apartado - 1][1]):
        print(f"{i + 1}. {punto}")
    seleccion_punto=int(input("Ingrese el número del punto de agenda: "))

    # Se obtiene el nombre del punto de agenda seleccionado.
    punto_seleccionado=agenda[seleccion_apartado - 1][1][seleccion_punto - 1]

    # Se registra la hora de inicio del punto de agenda seleccionado.
    hora_inicio = datetime.datetime.now()
    print(f"Se ha iniciado la discusión del punto de agenda '{punto_seleccionado}' a las {hora_inicio}")

    # Se selecciona participante.
    nombre_participantes=[participante["nombre"] for participante in participantes]

    # Se comienza bucle para seleccionar participantes hasta que se escriba 'fin'.
    while True:
        print("Lista de participantes: ")
        for i, nombre in enumerate(nombre_participantes):
            print(f"{i+1}. {nombre}")
        seleccion = input("Seleccione el número del participante que tomará la palabra o escriba 'fin' para terminar: ")
        if seleccion.lower()=="fin":
            break
        elif not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(nombre_participantes):
            print("Error: selección no válida")
            continue
        
        # Se obtiene el participante seleccionado.
        participante_seleccionado = participantes[int(seleccion)-1]
        print(f"{participante_seleccionado['nombre']} ha sido seleccionado para participar en el punto de la agenda '{punto_seleccionado}'")

        # Se inicia reconocimiento de voz para el participante seleccionado.
        print(f"Iniciando reconocimiento de voz para el punto '{punto_seleccionado}' y el participante '{participante_seleccionado['nombre']}'...")
        with sr.Microphone() as source:
            r=sr.Recognizer()
            r.adjust_for_ambient_noise(source) # Ajustar nivel de ruido
            audio=r.listen(source)

        # Se realiza reconocimiento de voz.
        try:
            print("Procesando audio...")
            texto_reconocido=r.recognize_google(audio, language="es-ES")
            print(f"Texto reconocido: '{texto_reconocido}'")
        except sr.UnknownValueError:
            print("No se pudo reconocer el audio.")
        except sr.RequestError as e:
            print(f"No se pudo conectar con el servicio de reconocimiento de voz; {e}")

def ver_agenda():
    """
    Función que permite hacer una impresión de la lista de participantes y de la agenda.

    Args:
        participante (list): Condicional del for dentro de los participantes, que toma valor de lista.
        apartado (list): Condicional del for dentro de la agenda, que toma valor de lista sobre apartados.
        puntos (list): Condicional del for dentro de la agenda, que toma valor de lista sobre apartados.
        punto (list): Condicional del ciclo for anidado, que toma el valor de un punto dentro de cada apartado.
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
            print(" - " + punto)

def menu():
    """
    Función que genera un menú en terminal, para que el programa sea manejado a preferencia.

    Args:
        opcion (str): Viariable que se utiliza para realizar comparaciones.
    """
    while True:
        os.system('clear')
        print("Menú:")
        print("1. Registrar participantes")
        print("2. Definir agenda")
        print("3. Reconocimiento de voz")
        print("4. Ver agenda")
        print("5. Salir")
        opcion=input("Ingrese la opción deseada: ")

        if opcion=="1":
            os.system('clear')
            lista_participantes()
        elif opcion=="2":
            os.system('clear')
            registro_agenda()
        elif opcion=="3":
            os.system('clear')
            speech()
        elif opcion=="4":
            while True:
                os.system('clear')
                ver_agenda()
                opcion=input("Ingrese 'salir' para regresar al menú principal: ")
                if opcion=="salir":
                    break
                else:
                    print("Opción no válida.")
        elif opcion=="5":
            os.system('clear')
            print("¡Gracias por utilizar nuestro programa!")
            time.sleep(3)
            os.system('clear')
            break
        else:
            print("Opción no válida.")

menu()