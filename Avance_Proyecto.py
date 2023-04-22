apartados=[]
puntos=[]
participantes=[]

def registro_agenda():
    """
    función que crea y organiza una agenda por apartados y puntos distribuídos en cada apartado.
    """
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


def participantes():
    """
    faf
    """
    while True:
        print('Ingrese el participante:')
        nuevo_participante = input()
        if nuevo_participante.lower() not in [a.lower() for a in participantes]:
            participantes.append(nuevo_participante)
        else:
            print('El participante ya está incluído en la lista')
        
        print('¿Desea agregar otro participante? (si/no)')
        respuesta = input()
        if respuesta.lower() == 'no':
            print('Su lista de participantes está completa')
            break
    

"""
import speech_recognition as sr
r=sr.Recognizer()

with sr.Microphone() as source:
    audio=r.listen(source)
    try:
        text=r.recognize_assemblyai(audio, language="es-ES")
"""
import speech_recognition as sr
import time
def speech():
    r = sr.Recognizer()
    i=0
    l=[]
    with sr.Microphone() as source:
        while True:
            print("Intervención:\n")
            print("Di algo...")
            r.energy_threshold = 700  # valor en decibeles
            r.adjust_for_ambient_noise(source)  # Ajusta el ruido del ambiente para mejorar la calidad del reconocimiento de vos
            audio = r.listen(source)
            if i>=5:
                print("Se ha alcanzado el límite de intentos.")
                break  # Sale del bucle si se alcanza el límite de intentos
            try:
                # Convertir audio a texto
                text = r.recognize_google(audio, language='es-ES')
                print("Momento de inicio",(time.strftime("%Y-%m-%d %H:%M:%S")),"/ Escrito: " + text)
                if text.lower() == "finalizar":
                    break  # Sale del bucle si el usuario dice "Finalizar"
                l.append(time.strftime("%H:%M:%S"))#Da la hora 
                l.append(text )
                i=0 #Reinicia el conteo
            except sr.UnknownValueError:
                print("No se pudo entender lo que dijiste.")
                i+=1
            except sr.RequestError as e:
                print("No se pudo conectar al servicio de reconocimiento de voz; {0}".format(e))
                i+=1
    return l
result = speech()
print(result)


