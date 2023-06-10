import customtkinter as ctk
import tkinter.messagebox as messagebox
from LogicaAgenda import crear_agenda, agregar_participante, agregar_apartado, agregar_punto
from datetime import datetime

class VentanaPrincipal:
    def __init__(self):
        self.ventana_principal = ctk.CTk()
        self.ventana_principal.geometry("750x500")
        self.ventana_principal.title("Agenda Web")
        self.ventana_principal._set_appearance_mode("dark")

        self.nombre_agenda = ctk.CTkLabel(self.ventana_principal, text="Nombre para la Agenda:", font=("Arial", 18, "bold"))
        self.nombre_agenda.place(x=32, y=20)

        self.entry_nombre_agenda = ctk.CTkEntry(self.ventana_principal, width=250, placeholder_text="Nombre de la agenda", justify="center")
        self.entry_nombre_agenda.place(x=235, y=21)

        self.boton_guardar_agenda = ctk.CTkButton(self.ventana_principal, text="Guardar nombre de la agenda", font=("Arial", 15), command=self.guardar_agenda)
        self.boton_guardar_agenda.place(x=500, y=21)
        self.boton_guardar_agenda.configure(fg_color="black")

        self.barra_lateral = ctk.CTkFrame(self.ventana_principal, width=200)
        self.barra_lateral.place(x=10, y=70)

        self.boton_participantes = ctk.CTkButton(self.barra_lateral, text="Participantes", font=("Arial", 14), command=self.mostrar_ventana_participantes)
        self.boton_participantes.pack(pady=10, padx=20, fill="x")

        self.boton_apartados = ctk.CTkButton(self.barra_lateral, text="Apartados", font=("Arial", 14), command=self.mostrar_ventana_apartados)
        self.boton_apartados.pack(pady=10, padx=20, fill="x")

        self.boton_discusion = ctk.CTkButton(self.barra_lateral, text="Discusiones", font=("Arial", 14), command=self.mostrar_ventana_discusion)
        self.boton_discusion.pack(pady=10, padx=20, fill="x")

        self.boton_html = ctk.CTkButton(self.barra_lateral, text="Generar HTML", font=("Arial", 14), command=self.generar_html)
        self.boton_html.pack(pady=10, padx=20, fill="x")

        self.agenda_nombre_asignado = False

        self.ventana_principal.mainloop()

    def mostrar_ventana_participantes(self):
        if not self.agenda_nombre_asignado:
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.")
            return
        VentanaSuperpuesta(self.ventana_principal, "Participantes")

    def mostrar_ventana_apartados(self):
        if not self.agenda_nombre_asignado:
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.")
            return
        VentanaSuperpuesta(self.ventana_principal, "Apartados")

    def mostrar_ventana_discusion(self):
        if not self.agenda_nombre_asignado:
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.")
            return
        VentanaSuperpuesta(self.ventana_principal, "Discusiones")

    def generar_html(self):
        if not self.agenda_nombre_asignado:
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.")
            return

    def guardar_agenda(self):
        fecha = datetime.today().strftime("%d/%m/%Y")
        nombre = self.entry_nombre_agenda.get()

        if nombre.strip() == "":
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.")
            return

        crear_agenda(nombre)

        self.entry_nombre_agenda.destroy()
        self.boton_guardar_agenda.destroy()

        self.label_agenda = ctk.CTkLabel(self.ventana_principal, text=nombre, font=("Arial", 18, "bold"))
        self.label_agenda.place(x=235, y=20)

        self.label_fecha = ctk.CTkLabel(self.ventana_principal, text="Fecha: " + fecha, font=("Arial", 18, "bold"))
        self.label_fecha.place(x=500, y=20)

        self.agenda_nombre_asignado = True

class VentanaSuperpuesta:
    """Clase que crea la ventana secundaria de la aplicación"""

    def __init__(self, ventana_principal, value):
        """Constructor de la clase VentanaSuperpuesta"""
        self.mini_window = ctk.CTkFrame(ventana_principal, width=500, height=400, fg_color="gray")
        self.mini_window.place(x=200, y=70)

        if value == "Participantes":
            self.label_nombre = ctk.CTkLabel(self.mini_window, text="Nombre: ", font=("Arial", 15))
            self.label_apellido1 = ctk.CTkLabel(self.mini_window, text="Primer Apellido: ", font=("Arial", 15))
            self.label_apellido2 = ctk.CTkLabel(self.mini_window, text="Segundo Apellido: ", font=("Arial", 15))

            self.label_nombre.place(x=10, y=10)
            self.label_apellido1.place(x=10, y=60)
            self.label_apellido2.place(x=10, y=110)

            self.entry_nombre = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el nombre", justify="center")
            self.entry_apellido1 = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el primer apellido", justify="center")
            self.entry_apellido2 = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el segundo apellido", justify="center")

            self.entry_nombre.place(x=220, y=10)
            self.entry_apellido1.place(x=220, y=60)
            self.entry_apellido2.place(x=220, y=110)

            self.boton_guardar_participante = ctk.CTkButton(self.mini_window, text="Guardar", command=self.guardar_participante)
            self.boton_guardar_participante.place(x=85, y=145)

            self.boton_eliminar_participante = ctk.CTkButton(self.mini_window, text="Eliminar")
            self.boton_eliminar_participante.place(x=285, y=145)

        elif value == "Apartados":
            self.label_apartado = ctk.CTkLabel(self.mini_window, text="Apartado: ", font=("Arial", 15))
            self.label_apartado.place(x=10, y=10)
            self.entry_apartado = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el nombre del apartado", justify="center")
            self.entry_apartado.place(x=220, y=10)

            self.label_cant_puntos = ctk.CTkLabel(self.mini_window, text="Cantidad de puntos: ", font=("Arial", 15))
            self.label_cant_puntos.place(x=10, y=60)
            self.entry_cant_puntos = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese la cantidad de puntos", justify="center")
            self.entry_cant_puntos.place(x=220, y=60)

            self.boton_cant_puntos = ctk.CTkButton(self.mini_window, text="Aceptar", command=self.crear_entries)
            self.boton_cant_puntos.place(x=220, y=100)

            self.boton_guardar_apartado = ctk.CTkButton(self.mini_window, text="Guardar", command=self.guardar_todo)
            self.boton_guardar_apartado.place(x=35, y=100)

            self.boton_eliminar_apartado = ctk.CTkButton(self.mini_window, text="Eliminar")
            self.boton_eliminar_apartado.place(x=35, y=140)

        elif value == "Discusiones":
            self.label_seleccionar_apartados = ctk.CTkLabel(self.mini_window, text=" Seleccione el apartado: ", font=("Arial", 15)) # se crea el label que indica seleccionar el apartado
            self.label_seleccionar_punto = ctk.CTkLabel(self.mini_window, text=" Seleccione el punto: ", font=("Arial", 15)) # se crea el label que indica seleccionar el punto
            self.label_seleccionar_participante = ctk.CTkLabel(self.mini_window, text=" Seleccione el participante: ", font=("Arial", 15)) # se crea el label que indica seleccionar el participante
            self.label_seleccionar_discusiones = ctk.CTkLabel(self.mini_window, text=" Seleccione la discusión: ", font=("Arial", 15)) # se crea el label que indicia seleccionar la discusion
            self.discusion = ctk.CTkLabel(self.mini_window, text=" Discusion: ", font=("Arial", 15)) # se crea el label que indica la discusion que se va a crear

            self.menu_opciones_apartados = ctk.CTkOptionMenu(self.mini_window) # se crea el menu de apartados
            self.menu_opciones_puntos = ctk.CTkOptionMenu(self.mini_window, values=["Puntos"]) # se crea el menu de puntos
            self.menu_opciones_participantes = ctk.CTkOptionMenu(self.mini_window, values=["Participantes"]) # se crea el menu de participantes
            self.menu_opciones_discusion = ctk.CTkOptionMenu(self.mini_window, values=["Discusiones"]) # se crea el menu de discusiones

            self.label_seleccionar_apartados.place(x=50, y=10) # se le da una ubicacion al label de seleccionar
            self.label_seleccionar_punto.place(x=50, y=80) # se le da una ubicaion al label al label de seleccionar punto
            self.label_seleccionar_participante.place(x=50, y=150) # se le da una ubicacion al label de seleccionar participante
            self.label_seleccionar_discusiones.place(x=50, y=210) # se le da una ubicacion al label de seleccionar discusiones
            self.discusion.place(x=50, y=260) # se la da una ubicacion al label de donde se ingresan las discusiones

            self.menu_opciones_apartados.place(x=250, y=10) # se le da una ubicacion al menu de apartados
            self.menu_opciones_puntos.place(x=250, y=80) # se le da una ubicacion al menu de puntos
            self.menu_opciones_participantes.place(x=250, y=150) # se le da una ubicacion al menu de participantes
            self.menu_opciones_discusion.place(x=250, y=210) # se le da una ubicacion al menu de discusiones

            self.btn_guardar = ctk.CTkButton(self.mini_window, text="Guardar") # se crea el boton guardar
            self.btn_guardar.place(x=520, y=10) # se le da una ubicacion

            self.btn_eliminar = ctk.CTkButton(self.mini_window, text="Eliminar") # se crea el boton de eliminar
            self.btn_eliminar.place(x=520, y=45) # se le da una ubicacion

            self.btn_modificar = ctk.CTkButton(self.mini_window, text="Modificar") # se crea el boton de modificar
            self.btn_modificar.place(x=520, y=80) # se le da una ubicacion


    def crear_entries(self):
        num_puntos = int(self.entry_cant_puntos.get())  # Obtener el número de puntos ingresado como entero
        self.entries = []

        for i in range(num_puntos):
            entry = ctk.CTkEntry(self.mini_window, width=250, placeholder_text=f"Ingrese el punto {i+1}", justify="center")
            entry.place(x=220, y=100 + i * 40)
            self.entries.append(entry)

    def guardar_participante(self):
        nombre_participante = self.entry_nombre.get()
        apellido1_participante = self.entry_apellido1.get()
        apellido2_participante = self.entry_apellido2.get()

        self.entry_nombre.delete(0, "end")
        self.entry_apellido1.delete(0, "end")
        self.entry_apellido2.delete(0, "end")

        if nombre_participante.strip() == "":
            messagebox.showerror("Error", "Debe agregar un nombre.")
            return
        elif apellido1_participante.strip() == "":
            messagebox.showerror("Error", "Debe agregar un primer apellido.")
            return
        elif apellido2_participante.strip() == "":
            messagebox.showerror("Error", "Debe agregar un segundo apellido.")
            return
        else:
            messagebox.showinfo("Información", "Participante agregado correctamente.")

        agregar_participante(nombre_participante, apellido1_participante, apellido2_participante)

    def guardar_apartado(self):
        nombre_apartado = self.entry_apartado.get()

        self.entry_apartado.delete(0, "end")

        if nombre_apartado.strip() == "":
            messagebox.showerror("Error", "Debe agregar un nombre al apartado.")
            return
        else:
            messagebox.showinfo("Información", "Apartado agregado correctamente.")

        agregar_apartado(nombre_apartado)

    def guardar_puntos(self, nombre_apartado):
        puntos = []

        for entry in self.entries:
            punto = entry.get()
            entry.destroy()
            puntos.append(punto)

        for nombre_punto in puntos:
            agregar_punto(nombre_punto, nombre_apartado)

    def guardar_todo(self):
        self.guardar_apartado()
        self.guardar_puntos(self.entry_apartado.get())


            

ventana = VentanaPrincipal()
ventana.ventana_principal.mainloop()