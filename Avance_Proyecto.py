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
    participantes=[]

    # Se solicita al usuario que ingrese los nombres y carnets de los participantes
    while True:
        nombre=input("Ingrese el nombre completo del participante o escriba 'fin' para terminar: ")
        if nombre.lower()=="fin":
            break
        carnet=int(input("Ingrese el número de carnet del participante: "))
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
        puntos = []
        while True:
            nombre_punto = input("Ingrese el nombre del punto o escriba 'fin' para terminar el apartado: ")
            if nombre_punto.lower() == "fin":
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
    Se hará un reconocimiento de voz que imprime lo dicho por el usuario

    Args: 
        i(int): Contador de errores
        text(str): Almacena el texto escuchado
        r(Recognizer): Realiza la tarea de reconocimiento de voz
        audio(AudioData): Almacena el audio capturado por el microfono

    Attributes: 
        tex_cap(list): Lista que contiene el texto entendido

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


