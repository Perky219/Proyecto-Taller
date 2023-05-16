from Avance_Proyecto import registro_agenda, lista_participantes, speech, seleccionar_espacio_agenda, seleccionar_participante
import tkinter as tk
from tkinter import ttk, messagebox

def crear_pestana_inicio(notebook):
    frame_inicio = tk.Frame(notebook)

    label = tk.Label(frame_inicio, text="¡Bienvenido a mi aplicación!")
    label.pack(padx=10, pady=10)

    notebook.add(frame_inicio, text="Inicio")

def crear_pestana_agenda(notebook):
    frame_agenda = tk.Frame(notebook)

    label = tk.Label(frame_agenda, text="Registro de agenda")
    label.pack(padx=10, pady=10)

    boton_registrar = tk.Button(frame_agenda, text="Registrar", command=registro_agenda)
    boton_registrar.pack(pady=10)

    notebook.add(frame_agenda, text="Agenda")

def registro_agenda():
    ventana_agenda = tk.Toplevel()
    ventana_agenda.title("Agenda")

    # Crear los campos de texto y botones necesarios
    titulo_entry = tk.Entry(ventana_agenda, width=50)
    punto_entry = tk.Entry(ventana_agenda, width=50)
    agregar_button = tk.Button(ventana_agenda, text="Agregar", command=lambda: agregar_item())
    editar_button = tk.Button(ventana_agenda, text="Editar", command=lambda: editar_item())
    eliminar_button = tk.Button(ventana_agenda, text="Eliminar", command=lambda: eliminar_item())
    lista_agenda = tk.Listbox(ventana_agenda, height=15, width=60)
    lista_agenda.grid(row=1, column=0, padx=20, pady=10)

    # Creamos un encabezado para la lista en forma de frame con dos etiquetas
    encabezado_lista = tk.Frame(ventana_agenda)
    encabezado_lista.grid(row=0, column=0, padx=20, pady=10, sticky="w")

    titulo_apartado = tk.Label(encabezado_lista, text="Apartado", font=("Arial", 12, "bold"))
    titulo_apartado.grid(row=0, column=0, padx=5)

    titulo_puntos = tk.Label(encabezado_lista, text="Puntos", font=("Arial", 12, "bold"))
    titulo_puntos.grid(row=0, column=1, padx=5)

    for elem in lista_agenda:
        lista_agenda.insert("end", f"{elem[0]}\t{elem[1]}")
    # lista_agenda = tk.Listbox(ventana_agenda, height=15, width=60)

    # Funciones para agregar, editar y eliminar items de la lista
    def agregar_item():
        titulo = titulo_entry.get()
        punto = punto_entry.get()
        lista_agenda.insert(tk.END, f"{titulo}: {punto}")
        titulo_entry.delete(0, tk.END)
        punto_entry.delete(0, tk.END)

    def editar_item():
     # Obtener el índice del elemento seleccionado
        seleccion = lista_agenda.curselection()
        if seleccion:
            indice = seleccion[0]

            # Obtener el texto actual del elemento seleccionado
            texto_actual = lista_agenda.get(indice)

            # Crear una nueva ventana para editar el texto
            ventana_edicion = tk.Toplevel(ventana_agenda)
            tk.Label(ventana_edicion, text="Editar elemento:").pack()

            # Crear un cuadro de texto para editar el texto
            texto_editado = tk.StringVar()
            texto_editado.set(texto_actual)
            tk.Entry(ventana_edicion, textvariable=texto_editado).pack()

            # Crear un botón para aceptar los cambios
            def aceptar_cambios():
                nuevo_texto = texto_editado.get()
                lista_agenda.delete(indice)
                lista_agenda.insert(indice, nuevo_texto)
                ventana_edicion.destroy()

            tk.Button(ventana_edicion, text="Aceptar", command=aceptar_cambios).pack()

        else:
            messagebox.showerror("Error", "Selecciona un elemento para editarlo")


    def eliminar_item():
        if lista_agenda.curselection():
            lista_agenda.delete(lista_agenda.curselection())

    # Crear la estructura de la ventana
    titulo_label = tk.Label(ventana_agenda, text="Apartado")
    titulo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    titulo_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")
    punto_label = tk.Label(ventana_agenda, text="Punto")
    punto_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    punto_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
    agregar_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    editar_button.grid(row=2, column=1, padx=10, pady=10, sticky="we")
    eliminar_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")
    lista_agenda.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="we")
    ventana_agenda.protocol("WM_DELETE_WINDOW", ventana_agenda.destroy)

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

# def registro_agenda():
#     ventana_agenda = tk.Toplevel(ventana_principal)
#     ventana_agenda.title("Agenda")

#     # Crear los campos de texto y botones necesarios
#     titulo_entry = tk.Entry(ventana_agenda, width=50)
#     punto_entry = tk.Entry(ventana_agenda, width=50)
#     agregar_button = tk.Button(ventana_agenda, text="Agregar", command=lambda: agregar_item())
#     eliminar_button = tk.Button(ventana_agenda, text="Eliminar", command=lambda: eliminar_item())
#     lista_agenda = tk.Listbox(ventana_agenda, height=15, width=60)

#     # Funciones para agregar y eliminar items de la lista
#     def agregar_item():
#         titulo = titulo_entry.get()
#         punto = punto_entry.get()
#         lista_agenda.insert(tk.END, f"{titulo}: {punto}")

#     def eliminar_item():
#         if lista_agenda.curselection():
#             lista_agenda.delete(lista_agenda.curselection()[0])

#     # Agregar los widgets a la ventana
#     titulo_label = tk.Label(ventana_agenda, text="Título:")
#     titulo_label.grid(row=0, column=0, padx=10, pady=10)
#     titulo_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")
#     punto_label = tk.Label(ventana_agenda, text="Punto:")
#     punto_label.grid(row=1, column=0, padx=10, pady=10)
#     punto_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
#     agregar_button.grid(row=2, column=0, padx=10, pady=10)
#     eliminar_button.grid(row=2, column=1, padx=10, pady=10)
#     lista_agenda.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# def lista_participantes():
#     ventana_participantes = tk.Toplevel(ventana_principal)
#     ventana_participantes.title("Lista de participantes")

#     # Crear el campo de texto y la lista
#     participante_entry = tk.Entry(ventana_participantes, width=50)
#     agregar_button = tk.Button(ventana_participantes, text="Agregar", command=lambda: agregar_participante())
#     lista_participantes = tk.Listbox(ventana_participantes, height=15, width=60)

#     # Función para agregar un participante a la lista
#     def agregar_participante():
#         participante = participante_entry.get()
#         lista_participantes.insert(tk.END, participante)

#     # Agregar los widgets a la ventana
#     participante_label = tk.Label(ventana_participantes, text="Participante:")
#     participante_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")