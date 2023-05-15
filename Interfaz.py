from Avance_Proyecto import registro_agenda, lista_participantes, speech, seleccionar_espacio_agenda, seleccionar_participante
import tkinter as tk
from tkinter import ttk
ventana_principal = None

def main():
    global ventana_principal  # Indicar que se usará la variable global

    # Crear la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Mi aplicación")

    # Crear las pestañas
    pestanas = ttk.Notebook(ventana_principal)
    pestana_agenda = tk.Frame(pestanas)
    pestana_participantes = tk.Frame(pestanas)
    pestana_reconocimiento = tk.Frame(pestanas)

    # Agregar las pestañas a la ventana principal
    pestanas.add(pestana_agenda, text="Agenda")
    pestanas.add(pestana_participantes, text="Lista de participantes")
    pestanas.add(pestana_reconocimiento, text="Reconocimiento de voz")
    pestanas.pack(expand=1, fill="both")

    # Agregar los botones a cada pestaña
    agenda_button = tk.Button(pestana_agenda, text="Registro de agenda", command=registro_agenda)
    agenda_button.pack(padx=10, pady=10)
    participantes_button = tk.Button(pestana_participantes, text="Lista de participantes", command=lista_participantes)
    participantes_button.pack(padx=10, pady=10)
    reconocimiento_button = tk.Button(pestana_reconocimiento, text="Reconocimiento de voz", command=speech)
    reconocimiento_button.pack(padx=10, pady=10)

    # Iniciar la aplicación
    ventana_principal.mainloop()

if __name__ == "__main__":
    main()

def registro_agenda():
    ventana_agenda = tk.Toplevel(ventana_principal)
    ventana_agenda.title("Agenda")

    # Crear los campos de texto y botones necesarios
    titulo_entry = tk.Entry(ventana_agenda, width=50)
    punto_entry = tk.Entry(ventana_agenda, width=50)
    agregar_button = tk.Button(ventana_agenda, text="Agregar", command=lambda: agregar_item())
    editar_button = tk.Button(ventana_agenda, text="Editar", command=lambda: editar_item())
    eliminar_button = tk.Button(ventana_agenda, text="Eliminar", command=lambda: eliminar_item())
    lista_agenda = tk.Listbox(ventana_agenda, height=15, width=60)

    # Funciones para agregar, editar y eliminar items de la lista
    def agregar_item():
        titulo = titulo_entry.get()
        punto = punto_entry.get()
        lista_agenda.insert(tk.END, f"{titulo}: {punto}")

    def editar_item():
        if lista_agenda.curselection():
            titulo, punto = lista_agenda.get(lista_agenda.curselection()[0]).split(": ")
            titulo_entry.delete(0, tk.END)
            titulo_entry.insert(tk.END, titulo)
            punto_entry.delete(0, tk.END)
            punto_entry.insert(tk.END, punto)
            lista_agenda.delete(lista_agenda.curselection()[0])

    def eliminar_item():
        if lista_agenda.curselection():
            lista_agenda.delete(lista_agenda.curselection()[0])

    # Agregar los widgets a la ventana
    titulo_label = tk.Label(ventana_agenda, text="Título:")
    titulo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    titulo_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")
    punto_label = tk.Label(ventana_agenda, text="Punto:")
    punto_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    punto_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
    agregar_button.grid(row=2, column=0, padx=10, pady=10)
    editar_button.grid(row=2, column=1, padx=10, pady=10)
    eliminar_button.grid(row=2, column=2, padx=10, pady=10)
    lista_agenda.grid(row=3, column=0, sticky="we", columnspan=3)

def lista_participantes():
    ventana_participantes = tk.Toplevel(ventana_principal)
    ventana_participantes.title("Lista de participantes")

    # Crear el campo de texto y la lista
    participante_entry = tk.Entry(ventana_participantes, width=50)
    agregar_button = tk.Button(ventana_participantes, text="Agregar", command=lambda: agregar_participante())
    lista_participantes = tk.Listbox(ventana_participantes, height=15, width=60)

    # Función para agregar un participante a la lista
    def agregar_participante():
        participante = participante_entry.get()
        lista_participantes.insert(tk.END, participante)

    # Agregar los widgets a la ventana
    participante_label = tk.Label(ventana_participantes, text="Participante:")
    participante_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")