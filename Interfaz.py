from Avance_Proyecto import registro_agenda, lista_participantes, speech, seleccionar_espacio_agenda, seleccionar_participante
import tkinter as tk
from tkinter import ttk, messagebox

class AgendaGUI:
    def __init__(self, master):
        self.master = master
        master.title("Agenda")

        # creación de pestañas
        self.notebook = tk.ttk.Notebook(master)
        self.tab_registro = tk.Frame(self.notebook)
        self.tab_lista = tk.Frame(self.notebook)
        self.tab_speech = tk.Frame(self.notebook)

        # agregando pestañas al notebook
        self.notebook.add(self.tab_registro, text="Registro")
        self.notebook.add(self.tab_lista, text="Lista")
        self.notebook.add(self.tab_speech, text="Speech")
        self.notebook.pack(expand=True, fill='both')

        # creación de widgets de la pestaña registro
        self.label_registro = tk.Label(self.tab_registro, text="Registro de Agenda")
        self.label_registro.pack(pady=10)

        self.button_agregar = tk.Button(self.tab_registro, text="Agregar apartado y puntos", command=self.agregar_apartado_puntos)
        self.button_agregar.pack(pady=10)

        # creación de widgets de la pestaña lista
        self.label_lista = tk.Label(self.tab_lista, text="Lista de Participantes")
        self.label_lista.pack(pady=10)

        # creación de widgets de la pestaña speech
        self.label_speech = tk.Label(self.tab_speech, text="Speech")
        self.label_speech.pack(pady=10)

        self.agenda = set()

    def agregar_apartado_puntos(self):
        # ventana para ingresar apartado y puntos
        ventana_ap = tk.Toplevel(self.master)
        ventana_ap.title("Agregar Apartado y Puntos")

        label_ap = tk.Label(ventana_ap, text="Ingrese el nombre del apartado:")
        label_ap.pack(pady=10)

        entry_ap = tk.Entry(ventana_ap)
        entry_ap.pack(pady=10)

        label_puntos = tk.Label(ventana_ap, text="Ingrese los puntos del apartado (separados por coma):")
        label_puntos.pack(pady=10)

        entry_puntos = tk.Entry(ventana_ap)
        entry_puntos.pack(pady=10)

        button_guardar = tk.Button(ventana_ap, text="Guardar", command=lambda: self.guardar_apartado_puntos(entry_ap.get(), entry_puntos.get()))
        button_guardar.pack(pady=10)

    def guardar_apartado_puntos(self, apartado, puntos):
        # guardar apartado y puntos en la agenda
        puntos_lista = puntos.split(",")
        self.agenda.add((apartado, puntos_lista))

    def guardar_agenda(self):
        # guardar agenda en una variable global
        global agenda_guardada
        agenda_guardada = self.agenda

    def cargar_agenda(self):
        # cargar agenda desde la variable global
        global agenda_guardada
        self.agenda = agenda_guardada

if __name__ == '__main__':
    root = tk.Tk()
    agenda_gui = AgendaGUI(root)
    root.mainloop()

    # guardar agenda antes de salir
    agenda_gui.guardar_agenda()