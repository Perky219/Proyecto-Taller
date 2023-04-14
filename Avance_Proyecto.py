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



#prueba del commit en git