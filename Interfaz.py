from Avance_Proyecto import registro_agenda, lista_participantes, speech, seleccionar_espacio_agenda, seleccionar_participante
import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Mi aplicación")

# Crear el contenedor de pestañas
pestanas = ttk.Notebook(ventana_principal)

# Crear la pestaña de agenda
pestaña_agenda = ttk.Frame(pestanas)
pestanas.add(pestaña_agenda, text="Agenda")

# Crear la pestaña de lista de participantes
pestaña_participantes = ttk.Frame(pestanas)
pestanas.add(pestaña_participantes, text="Lista de participantes")

# Crear la pestaña de reconocimiento de voz
pestaña_reconocimiento = ttk.Frame(pestanas)
pestanas.add(pestaña_reconocimiento, text="Reconocimiento de voz")

# Empacar el contenedor de pestañas
pestanas.pack(expand=1, fill="both")

ventana_principal.mainloop()

# # Crear la ventana principal
# ventana_principal = tk.Tk()
# ventana_principal.geometry("500x500")

# # Crear las pestañas
# pestanas = tk.Notebook(ventana_principal)

# # Pestaña de agenda
# pestana_agenda = tk.Frame(pestanas)
# btn_registro_agenda = tk.Button(pestana_agenda, text="Registrar evento", command=registro_agenda)
# btn_registro_agenda.pack(pady=20, padx=20)
# pestanas.add(pestana_agenda, text="Agenda")

# # Pestaña de lista de participantes
# pestana_participantes = tk.Frame(pestanas)
# btn_lista_participantes = tk.Button(pestana_participantes, text="Mostrar lista", command=lista_participantes)
# btn_lista_participantes.pack(pady=20, padx=20)
# pestanas.add(pestana_participantes, text="Lista de participantes")

# # Pestaña de reconocimiento de voz
# pestana_speech = tk.Frame(pestanas)
# btn_speech = tk.Button(pestana_speech, text="Activar reconocimiento de voz", command=speech)
# btn_speech.pack(pady=20, padx=20)
# pestanas.add(pestana_speech, text="Reconocimiento de voz")

# # Mostrar las pestañas
# pestanas.pack(expand=1, fill="both")

# # Iniciar el bucle de la ventana principal
# ventana_principal.mainloop()