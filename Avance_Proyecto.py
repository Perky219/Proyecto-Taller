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
    # Se crea una lista vacía para almacenar los nombres y carnets de los participantes
    global participantes
    participantes = []

    # Se solicita al usuario que ingrese los nombres y carnets de los participantes
    while True:
        nombre = str(input("Ingrese el nombre completo del participante o escriba 'fin' para terminar: "))
        if nombre.lower() == "fin":
            break
        carnet = int(input("Ingrese el número de carnet del participante: "))
        # Se valida si el número de carnet ya ha sido registrado previamente
        carnet_existente = False
        for participante in participantes:
            if participante["carnet"] == carnet:
                print("Error: el número de carnet ya ha sido registrado para", participante["nombre"])
                carnet_existente = True
                break

        # Se valida que el número de carnet sea un valor numérico
        if not carnet.isdigit():
            print("Error: el número de carnet debe ser un valor numérico")
        elif not carnet_existente:
            participantes.append({"nombre": nombre, "carnet": carnet})

    # Se crea una cadena de texto con los nombres y carnets de los participantes
    participantes_str = "\nLista de participantes:\n"
    for participante in participantes:
        participantes_str += participante["nombre"] + " - " + participante["carnet"] + "\n"

    # Se muestra la lista de participantes registrados
    print(participantes_str)

def registro_agenda():
    """
    función que crea y organiza una agenda por apartados y puntos distribuídos en cada apartado.
    """
    global apartados
    global puntos
    apartados=[]
    puntos=[]
    while True:
        print('Ingrese el nombre del apartado que desea agregar a la agenda:')
        nuevo_apartado = input()
        if nuevo_apartado.lower() not in [a.lower() for a in apartados]: #linea para definir que un apartado no está repetido
            apartados.append(nuevo_apartado)
            print(f'Ha agregado el apartado "{nuevo_apartado}" a la lista de apartados.\n')

            while True:
                print('Ingrese el punto que desea agregar a la agenda:')
                nuevo_punto = input()
                puntos.append((nuevo_apartado, nuevo_punto))
                print(f'Ha agregado el punto "{nuevo_punto}" al apartado "{nuevo_apartado}".\n')
                
                print('¿Desea agregar otro punto a la agenda? (si/no)')
                respuesta = input()
                if respuesta.lower() == 'no':
                    break
        else:
            print('Ese apartado ya existe, agregue uno distinto')
        print('¿Desea agregar otro apartado a la agenda? (si/no)')
        respuesta = input()
        if respuesta.lower() == 'no':
            print('Su agenda está lista')
            break
    
def speech():
    """
    Se hará un reconocimiento de voz que imprime lo dicho por el usuario

    Args: 
        i(int): Contador de errores
        text(str): Almacena el texto escuchado
        r(Recognizer): Realiza la tarea de reconocimiento de voz
        audio(AudioData): Almacena el audio capturado por el microfono

    Atributos: tex_cap(list): Lista que contiene el texto entendido

    Returns:
        list: Returna la lista 'text_cap' que contiene el texto entendido
    """
    import speech_recognition as sr

    r = sr.Recognizer()
    i=0

    global text_cap
    text_cap=[]

    with sr.Microphone() as source:
        while True:
            print("Intervención:\n")
            print("Habla ahora...")
            r.energy_threshold = 700  # valor en decibeles
            r.adjust_for_ambient_noise(source)  # Ajusta el ruido del ambiente para mejorar la calidad del reconocimiento de voz
            audio = r.listen(source)
            if i>=3:
                print("Se ha alcanzado el límite de intentos.")
                break  # Sale del bucle si se alcanza el límite de intentos
            try:
                # Convertir audio a texto
                text = r.recognize_google(audio, language='es-ES')
                print("Momento de inicio",(time.strftime("%Y-%m-%d %H:%M:%S")),"/ Escrito: " + text)
                if text.lower() == "finalizar":
                    break  # Sale del bucle si el usuario dice "Finalizar"
                else:
                    text_cap.append(time.strftime("%H:%M:%S"))#Da la hora 
                    text_cap    .append(text )
                    i=0 #Reinicia el conteo
            except sr.UnknownValueError:
                print("No se pudo entender lo que dijiste.")
                i+=1
            except sr.RequestError as e:
                print("No se pudo conectar al servicio de reconocimiento de voz; {0}".format(e))
                i+=1
    return text_cap
result = speech()
print(result)


