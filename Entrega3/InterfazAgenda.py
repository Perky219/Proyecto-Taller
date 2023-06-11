import customtkinter as ctk
import tkinter.messagebox as messagebox
from LogicaAgenda import crear_agenda, agregar_participante, agregar_apartado, agregar_punto, personas_asList, puntos_asDict
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

class VentanaSuperpuesta: # se crea la clase VentanaSuperpuesta
    """Clase que crea la ventana secundaria de la aplicación"""

    def __init__(self, ventana_principal, value): # se recibe la ventana principal y el valor que indica que ventana secundaria se va a crear
        """Constructor de la clase VentanaSuperpuesta"""
        lista_participantes = personas_asList() # se crea una lista con los participantes
        apartados_puntos = puntos_asDict() # se crea un diccionario con los apartados y sus puntos
        apartados = apartados_puntos.keys() # se crea una lista con los apartados

        self.mini_window = ctk.CTkFrame(ventana_principal, width=500, height=400, fg_color="gray") # se crea la ventana secundaria
        self.mini_window.place(x=200, y=70) # se posiciona la ventana secundaria

        if value == "Participantes": # si el valor es "Participantes" se crea la ventana de participantes
            self.label_nombre = ctk.CTkLabel(self.mini_window, text="Nombre: ", font=("Arial", 15)) # se crea el label de nombre
            self.label_apellido1 = ctk.CTkLabel(self.mini_window, text="Primer Apellido: ", font=("Arial", 15)) # se crea el label de primer apellido
            self.label_apellido2 = ctk.CTkLabel(self.mini_window, text="Segundo Apellido: ", font=("Arial", 15)) # se crea el label de segundo apellido

            self.label_nombre.place(x=10, y=10) # se posiciona el label de nombre
            self.label_apellido1.place(x=10, y=60) # se posiciona el label de primer apellido
            self.label_apellido2.place(x=10, y=110) # se posiciona el label de segundo apellido

            self.entry_nombre = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el nombre", justify="center") # se crea el entry de nombre
            self.entry_apellido1 = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el primer apellido", justify="center") # se crea el entry de primer apellido
            self.entry_apellido2 = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el segundo apellido", justify="center") # se crea el entry de segundo apellido

            self.entry_nombre.place(x=220, y=10) # se posiciona el entry de nombre
            self.entry_apellido1.place(x=220, y=60) # se posiciona el entry de primer apellido
            self.entry_apellido2.place(x=220, y=110) # se posiciona el entry de segundo apellido

            self.boton_guardar_participante = ctk.CTkButton(self.mini_window, text="Guardar", command=self.guardar_participante) # se crea el boton de guardar
            self.boton_guardar_participante.place(x=85, y=145) # se posiciona el boton de guardar

            self.boton_eliminar_participante = ctk.CTkButton(self.mini_window, text="Eliminar") # se crea el boton de eliminar
            self.boton_eliminar_participante.place(x=285, y=145) # se posiciona el boton de eliminar

        elif value == "Apartados": # si el valor es "Apartados" se crea la ventana de apartados
            self.label_apartado = ctk.CTkLabel(self.mini_window, text="Apartado: ", font=("Arial", 15)) # se crea el label de apartado
            self.label_apartado.place(x=10, y=10) # se posiciona el label de apartado
            self.entry_apartado = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el nombre del apartado", justify="center") # se crea el entry de apartado
            self.entry_apartado.place(x=220, y=10) # se posiciona el entry de apartado

            self.label_cant_puntos = ctk.CTkLabel(self.mini_window, text="Cantidad de puntos: ", font=("Arial", 15)) # se crea el label de cantidad de puntos
            self.label_cant_puntos.place(x=10, y=60) # se posiciona el label de cantidad de puntos
            self.entry_cant_puntos = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese la cantidad de puntos", justify="center") # se crea el entry de cantidad de puntos
            self.entry_cant_puntos.place(x=220, y=60) # se posiciona el entry de cantidad de puntos

            self.boton_cant_puntos = ctk.CTkButton(self.mini_window, text="Aceptar", command=self.crear_entries) # se crea el boton de aceptar
            self.boton_cant_puntos.place(x=220, y=100) # se posiciona el boton de aceptar

            self.boton_guardar_apartado = ctk.CTkButton(self.mini_window, text="Guardar", command=self.guardar_todo) # se crea el boton de guardar
            self.boton_guardar_apartado.place(x=35, y=100) # se posiciona el boton de guardar

            self.boton_eliminar_apartado = ctk.CTkButton(self.mini_window, text="Eliminar") # se crea el boton de eliminar
            self.boton_eliminar_apartado.place(x=35, y=140) # se posiciona el boton de eliminar

        elif value == "Discusiones": # si el valor es "Discusiones" se crea la ventana de discusiones
            self.label_seleccionar_apartados = ctk.CTkLabel(self.mini_window, text="Apartado", font=("Arial", 18)) # se crea el label que indica seleccionar el apartado
            self.label_seleccionar_punto = ctk.CTkLabel(self.mini_window, text="Punto del apartado", font=("Arial", 18)) # se crea el label que indica seleccionar el punto
            self.label_seleccionar_participante = ctk.CTkLabel(self.mini_window, text="Participante", font=("Arial", 18)) # se crea el label que indica seleccionar el participante

            self.menu_opciones_apartados = ctk.CTkOptionMenu(self.mini_window, values=apartados) # se crea el menu de apartados
            self.menu_opciones_puntos = ctk.CTkOptionMenu(self.mini_window, values=["Puntos"]) # se crea el menu de puntos
            self.menu_opciones_participantes = ctk.CTkOptionMenu(self.mini_window, values=lista_participantes) # se crea el menu de participantes

            self.label_seleccionar_apartados.place(x=50, y=10) # se le da una ubicacion al label de seleccionar
            self.label_seleccionar_punto.place(x=170, y=10) # se le da una ubicaion al label al label de seleccionar punto
            self.label_seleccionar_participante.place(x=350, y=10) # se le da una ubicacion al label de seleccionar participante

            self.discusion = ctk.CTkLabel(self.mini_window, text=" Discusion: ", font=("Arial", 18)) # se crea el label que indica la discusion que se va a crear
            self.discusion.place(x=50, y=100) # se la da una ubicacion al label de donde se ingresan las discusiones
            self.entry_discusion = ctk.CTkEntry(self.mini_window, width=400, height=65, placeholder_text="Ingrese la discusion", justify="center") # se crea el entry donde se ingresan las discusiones
            self.entry_discusion.place(x=50, y=135) # se le da una ubicacion al entry de las discusiones

            self.menu_opciones_apartados.place(x=25, y=43) # se le da una ubicacion al menu de apartados
            self.menu_opciones_puntos.place(x=175, y=43) # se le da una ubicacion al menu de puntos
            self.menu_opciones_participantes.place(x=330, y=43) # se le da una ubicacion al menu de participantes

            self.btn_guardar = ctk.CTkButton(self.mini_window, text="Guardar") # se crea el boton guardar
            self.btn_guardar.place(x=25, y=210) # se le da una ubicacion

            self.btn_eliminar = ctk.CTkButton(self.mini_window, text="Eliminar") # se crea el boton de eliminar
            self.btn_eliminar.place(x=175, y=210) # se le da una ubicacion

            self.btn_modificar = ctk.CTkButton(self.mini_window, text="Modificar") # se crea el boton de modificar
            self.btn_modificar.place(x=325, y=210) # se le da una ubicacion

    def crear_entries(self): # Crear los entries para ingresar los puntos
        num_puntos = int(self.entry_cant_puntos.get())  # Obtener el número de puntos ingresado como entero
        self.entries = [] # Lista para guardar los entries

        for i in range(num_puntos): # Crear los entries
            entry = ctk.CTkEntry(self.mini_window, width=250, placeholder_text=f"Ingrese el punto {i+1}", justify="center") # Crear el entry
            entry.place(x=220, y=100 + i * 40) # Posicionar el entry
            self.entries.append(entry) # Agregar el entry a la lista

    def guardar_participante(self): # Guardar un participante
        nombre_participante = self.entry_nombre.get() # Obtener el nombre del participante
        apellido1_participante = self.entry_apellido1.get() # Obtener el primer apellido del participante
        apellido2_participante = self.entry_apellido2.get() # Obtener el segundo apellido del participante

        self.entry_nombre.delete(0, "end") # Borrar el nombre del entry
        self.entry_apellido1.delete(0, "end") # Borrar el primer apellido del entry
        self.entry_apellido2.delete(0, "end") # Borrar el segundo apellido del entry

        if nombre_participante.strip() == "": # Verificar que el nombre no esté vacío
            messagebox.showerror("Error", "Debe agregar un nombre.") # Mostrar mensaje de error
            return # Terminar la función
        elif apellido1_participante.strip() == "": # Verificar que el primer apellido no esté vacío
            messagebox.showerror("Error", "Debe agregar un primer apellido.") # Mostrar mensaje de error
            return # Terminar la función
        elif apellido2_participante.strip() == "": # Verificar que el segundo apellido no esté vacío
            messagebox.showerror("Error", "Debe agregar un segundo apellido.") # Mostrar mensaje de error
            return # Terminar la función
        else: # Si no hay errores
            messagebox.showinfo("Información", "Participante agregado correctamente.") # Mostrar mensaje de información

        agregar_participante(nombre_participante, apellido1_participante, apellido2_participante) # Agregar el participante a la base de datos

    def guardar_apartado(self): # Guardar un apartado
        self.nombre_apartado = self.entry_apartado.get() # Obtener el nombre del apartado

        self.entry_apartado.delete(0, "end") # Borrar el nombre del entry

        if self.nombre_apartado.strip() == "": # Verificar que el nombre no esté vacío
            messagebox.showerror("Error", "Debe agregar un nombre al apartado.") # Mostrar mensaje de error
            return # Terminar la función
        else: # Si no hay errores
            messagebox.showinfo("Información", "Apartado agregado correctamente.") # Mostrar mensaje de información

        agregar_apartado(self.nombre_apartado) # Agregar el apartado a la base de datos

    def guardar_puntos(self, nombre_apartado): # Guardar los puntos
        puntos = [] # Lista para guardar los puntos

        for entry in self.entries: # Recorrer los entries
            punto = entry.get() # Obtener el punto
            entry.destroy() # Eliminar el entry
            puntos.append(punto) # Agregar el punto a la lista

        for nombre_punto in puntos: # Recorrer los puntos
            agregar_punto(nombre_punto, nombre_apartado) # Agregar el punto a la base de datos

    def guardar_todo(self): # Guardar todo
        self.guardar_apartado() # Guardar el apartado
        self.guardar_puntos(self.nombre_apartado) # Guardar los puntos

ventana = VentanaPrincipal() # Crear la ventana
ventana.ventana_principal.mainloop() # Mostrar la ventana