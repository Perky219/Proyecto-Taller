import customtkinter as ctk # se importa la librería customtkinter
import tkinter.messagebox as messagebox # se importa la librería messagebox de tkinter
from datetime import datetime # se importa la librería datetime
import webbrowser # se importa la librería webbrowser
import webview # se importa la librería webview
from LogicaAgenda import ( 
    crear_agenda,
    crear_participante,
    crear_apartado,
    crear_punto,
    crear_discusion,
    personas_asList,
    puntos_asDict
) # se importan las funciones de la lógica de la agenda

class Main:
    """
    Clase que crea la ventana principal de la aplicación
    """
    def __init__(self):
        """
        Constructor de la clase Main
        """
        self.main_window = ctk.CTk() # se crea la ventana principal
        self.main_window.geometry("750x500") # se le asigna un tamaño a la ventana principal
        self.main_window.title("Agenda Web") # se le asigna un título a la ventana principal
        self.main_window._set_appearance_mode("dark") # se le asigna un modo oscuro a la ventana principal

        self.label_nombre_agenda = ctk.CTkLabel(self.main_window, text="Nombre para la Agenda:", font=("Arial", 18, "bold")) # se crea un label para el nombre de la agenda
        self.label_nombre_agenda.place(x=32, y=20) # se le asigna una posición al label

        self.entry_nombre_agenda = ctk.CTkEntry(self.main_window, width=250, placeholder_text="Nombre de la agenda", justify="center") # se crea un entry para el nombre de la agenda
        self.entry_nombre_agenda.place(x=235, y=21) # se le asigna una posición al entry

        self.boton_guardar_agenda = ctk.CTkButton(self.main_window, text="Guardar nombre de la agenda", font=("Arial", 15), command=self.guardar_agenda) # se crea un botón para guardar el nombre de la agenda
        self.boton_guardar_agenda.place(x=500, y=21) # se le asigna una posición al botón
        self.boton_guardar_agenda.configure(fg_color="black") # se le asigna un color al botón

        self.barra_lateral = ctk.CTkFrame(self.main_window, width=200) # se crea una barra lateral
        self.barra_lateral.place(x=10, y=70) # se le asigna una posición a la barra lateral

        self.boton_participantes = ctk.CTkButton(self.barra_lateral, text="Participantes", font=("Arial", 14), command=self.mostrar_ventana_participantes) # se crea un botón para mostrar la ventana de participantes
        self.boton_participantes.pack(pady=10, padx=20, fill="x") # se le asigna una posición al botón

        self.boton_apartados = ctk.CTkButton(self.barra_lateral, text="Apartados", font=("Arial", 14), command=self.mostrar_ventana_apartados) # se crea un botón para mostrar la ventana de apartados
        self.boton_apartados.pack(pady=10, padx=20, fill="x") # se le asigna una posición al botón

        self.boton_discusion = ctk.CTkButton(self.barra_lateral, text="Discusiones", font=("Arial", 14), command=self.mostrar_ventana_discusion) # se crea un botón para mostrar la ventana de discusiones
        self.boton_discusion.pack(pady=10, padx=20, fill="x") # se le asigna una posición al botón

        self.boton_html = ctk.CTkButton(self.barra_lateral, text="Generar HTML", font=("Arial", 14), command=self.generar_html) # se crea un botón para generar el HTML
        self.boton_html.pack(pady=10, padx=20, fill="x") # se le asigna una posición al botón

        self.agenda_nombre_asignado = False # se crea una variable para saber si se le asignó un nombre a la agenda

        self.main_window.mainloop() # se ejecuta la ventana principal

    def mostrar_ventana_participantes(self):
        """
        Método que muestra la ventana de participantes
        """
        if not self.agenda_nombre_asignado: # si no se le asignó un nombre a la agenda
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.") # se muestra un mensaje de error
            return # se retorna
        VentanaSuperpuesta(self.main_window, "Participantes") # se crea una ventana superpuesta

    def mostrar_ventana_apartados(self):
        """
        Método que muestra la ventana de apartados
        """
        if not self.agenda_nombre_asignado: # si no se le asignó un nombre a la agenda
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.") # se muestra un mensaje de error
            return # se retorna
        VentanaSuperpuesta(self.main_window, "Apartados") # se crea una ventana superpuesta

    def mostrar_ventana_discusion(self):
        """
        Método que muestra la ventana de discusiones
        """
        if not self.agenda_nombre_asignado: # si no se le asignó un nombre a la agenda
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.") # se muestra un mensaje de error
            return # se retorna
        VentanaSuperpuesta(self.main_window, "Discusiones") # se crea una ventana superpuesta

    def generar_html(self):
        if not self.agenda_nombre_asignado:
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.")
            return

        messagebox.showinfo("Éxito", "Página HTML generada correctamente.")

        # Abrir el archivo HTML en el navegador web predeterminado
        webbrowser.open("Agenda.html", new=1)

    def guardar_agenda(self):
        """
        Método que guarda el nombre de la agenda
        """
        fecha = datetime.today().strftime("%d/%m/%Y") # se obtiene la fecha actual
        nombre = self.entry_nombre_agenda.get() # se obtiene el nombre de la agenda

        if nombre.strip() == "": # si el nombre de la agenda está vacío
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.") # se muestra un mensaje de error
            return # se retorna

        crear_agenda(nombre) # se crea la agenda

        self.entry_nombre_agenda.destroy() # se destruye el entry
        self.boton_guardar_agenda.destroy() # se destruye el botón

        self.label_agenda = ctk.CTkLabel(self.main_window, text=nombre, font=("Arial", 18, "bold")) # se crea un label con el nombre de la agenda
        self.label_agenda.place(x=235, y=20) # se le asigna una posición al label

        self.label_fecha = ctk.CTkLabel(self.main_window, text="Fecha: " + fecha, font=("Arial", 18, "bold")) # se crea un label con la fecha
        self.label_fecha.place(x=500, y=20) # se le asigna una posición al label

        self.agenda_nombre_asignado = True # se le asigna True a la variable que indica si se le asignó un nombre a la agenda 

class VentanaSuperpuesta:
    """
    Clase que crea la ventana secundaria de la aplicación
    """
    def __init__(self, main_window, value):
        """
        Constructor de la clase VentanaSuperpuesta
        """
        self.lista_participantes = personas_asList() # se crea una lista con los participantes
        self.dict_apartados_puntos = puntos_asDict() # se crea un diccionario con los apartados y sus puntos
        self.apartados = list(self.dict_apartados_puntos.keys()) # se crea una lista con los apartados
        self.puntos = [] # se crea una lista vacía para los puntos

        self.mini_window = ctk.CTkFrame(main_window, width=500, height=400, fg_color="gray") # se crea la ventana secundaria
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

            self.boton_cant_puntos = ctk.CTkButton(self.mini_window, text="Aceptar", command=self.entries) # se crea el boton de aceptar
            self.boton_cant_puntos.place(x=220, y=100) # se posiciona el boton de aceptar

            self.boton_guardar_apartado = ctk.CTkButton(self.mini_window, text="Guardar", command=self.guardar_todo) # se crea el boton de guardar
            self.boton_guardar_apartado.place(x=35, y=100) # se posiciona el boton de guardar

            self.boton_eliminar_apartado = ctk.CTkButton(self.mini_window, text="Eliminar") # se crea el boton de eliminar
            self.boton_eliminar_apartado.place(x=35, y=140) # se posiciona el boton de eliminar

        elif value == "Discusiones": # si el valor es "Discusiones" se crea la ventana de discusiones
            self.label_seleccionar_apartados = ctk.CTkLabel(self.mini_window, text="Apartado", font=("Arial", 18)) # se crea el label que indica seleccionar el apartado
            self.label_seleccionar_punto = ctk.CTkLabel(self.mini_window, text="Punto del apartado", font=("Arial", 18)) # se crea el label que indica seleccionar el punto
            self.label_seleccionar_participante = ctk.CTkLabel(self.mini_window, text="Participante", font=("Arial", 18)) # se crea el label que indica seleccionar el participante

            self.label_seleccionar_apartados.place(x=50, y=10) # se le da una ubicacion al label de seleccionar
            self.label_seleccionar_punto.place(x=170, y=10) # se le da una ubicaion al label al label de seleccionar punto
            self.label_seleccionar_participante.place(x=350, y=10) # se le da una ubicacion al label de seleccionar participante

            self.men_apart = ctk.CTkOptionMenu(self.mini_window, values=self.apartados) # se crea el menu de apartados
            self.men_punt = ctk.CTkOptionMenu(self.mini_window, values=self.puntos) # se crea el menu de puntos
            self.men_part = ctk.CTkOptionMenu(self.mini_window, values=self.lista_participantes) # se crea el menu de participantes

            self.men_apart.place(x=25, y=43) # se le da una ubicacion al menu de apartados
            self.men_punt.place(x=175, y=43) # se le da una ubicacion al menu de puntos
            self.men_part.place(x=330, y=43) # se le da una ubicacion al menu de participantes

            self.men_apart.set(value="No hay apartados") # se le da un valor por defecto al menu de apartados
            self.men_punt.set(value="No hay puntos") # se le da un valor por defecto al menu de puntos
            self.men_part.set(value="No hay participantes") # se le da un valor por defecto al menu de participantes

            self.label_discusion = ctk.CTkLabel(self.mini_window, text=" Discusion: ", font=("Arial", 18)) # se crea el label que indica la discusion que se va a crear
            self.label_discusion.place(x=50, y=120) # se la da una ubicacion al label de donde se ingresan las discusiones
            self.entry_discusion = ctk.CTkEntry(self.mini_window, width=400, height=65, placeholder_text="Ingrese la discusion", justify="center") # se crea el entry donde se ingresan las discusiones
            self.entry_discusion.place(x=50, y=155) # se le da una ubicacion al entry de las discusiones

            self.boton_guardar = ctk.CTkButton(self.mini_window, text="Guardar", command=self.guardar_discusion) # se crea el boton guardar
            self.boton_guardar.place(x=25, y=240) # se le da una ubicacion

            self.boton_eliminar = ctk.CTkButton(self.mini_window, text="Eliminar") # se crea el boton de eliminar
            self.boton_eliminar.place(x=175, y=240) # se le da una ubicacion

            self.boton_modificar = ctk.CTkButton(self.mini_window, text="Modificar") # se crea el boton de modificar
            self.boton_modificar.place(x=325, y=240) # se le da una ubicacion

            self.boton_actualizar = ctk.CTkButton(self.mini_window, text="Actualizar puntos", command=self.actualizar_puntos) # se crea el boton de actualizar
            self.boton_actualizar.place(x=25, y=80) # se le da una ubicacion


    def entries(self):
        """
        Método para crear los entries para ingresar los puntos
        """
        num_puntos = int(self.entry_cant_puntos.get())  # Obtener el número de puntos ingresado como entero
        self.entry_cant_puntos.delete(0, "end") # Borrar el número de puntos ingresado
        self.entry_cant_puntos.configure(state="disabled") # Deshabilitar el entry de número de puntos
        self.entries = [] # Lista para guardar los entries

        for i in range(num_puntos): # Crear los entries
            entry = ctk.CTkEntry(self.mini_window, width=250, placeholder_text=f"Ingrese el punto {i+1}", justify="center") # Crear el entry
            entry.place(x=220, y=100 + i * 40) # Posicionar el entry
            self.entries.append(entry) # Agregar el entry a la lista

    def guardar_participante(self):
        """
        Método para guardar un participante 
        """
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

        crear_participante(nombre_participante, apellido1_participante, apellido2_participante) # Agregar el participante a la base de datos

    def guardar_apartado(self):
        """
        Método para guardar un apartado
        """
        self.nombre_apartado = self.entry_apartado.get() # Obtener el nombre del apartado

        self.entry_apartado.delete(0, "end") # Borrar el nombre del entry

        self.entry_cant_puntos.configure(state="normal") # Habilitar el entry de número de puntos

        if self.nombre_apartado.strip() == "": # Verificar que el nombre no esté vacío
            messagebox.showerror("Error", "Debe agregar un nombre al apartado.") # Mostrar mensaje de error
            return # Terminar la función
        else: # Si no hay errores
            messagebox.showinfo("Información", "Apartado agregado correctamente.") # Mostrar mensaje de información

        crear_apartado(self.nombre_apartado) # Agregar el apartado a la base de datos

    def guardar_puntos(self, nombre_apartado):
        """
        Método para guardar los puntos de un apartado

        Args:
            nombre_apartado (str): Nombre del apartado
        """
        puntos = [] # Lista para guardar los puntos

        for entry in self.entries: # Recorrer los entries
            punto = entry.get() # Obtener el punto
            entry.destroy() # Eliminar el entry
            puntos.append(punto) # Agregar el punto a la lista

        for nombre_punto in puntos: # Recorrer los puntos
            crear_punto(nombre_punto, nombre_apartado) # Agregar el punto a la base de datos

    def guardar_todo(self):
        """
        Método para guardar todo el apartado
        """
        self.guardar_apartado() # Guardar el apartado
        self.guardar_puntos(self.nombre_apartado) # Guardar los puntos

    def actualizar_puntos(self):
        """
        Método para actualizar los puntos en el menú de opciones
        """
        self.apartado_seleccionado=self.men_apart.get() # Obtener el apartado seleccionado
        self.puntos = list(self.dict_apartados_puntos.get(self.apartado_seleccionado,[])) # Obtener los puntos del apartado seleccionado
        self.men_punt.configure(values=self.puntos) # Actualizar los puntos en el menú de opciones

    def guardar_discusion(self):
        """
        Método para guardar una discusión
        """
        apartado_seleccionado=self.men_apart.get()
        punto_seleccionado=self.men_punt.get()
        persona_seleccionada=self.men_part.get()
        discusion=self.entry_discusion.get()

        self.entry_discusion.delete(0, "end") # Borrar la discusión del entry
        self.men_part.set("Participante") # Reiniciar el menú de opciones de participantes
        self.men_apart.set("Apartado") # Reiniciar el menú de opciones de apartados
        self.men_punt.set("Punto") # Reiniciar el menú de opciones de puntos

        messagebox.showinfo("Información", "Discusión agregada correctamente.") # Mostrar mensaje de información

        crear_discusion(apartado_seleccionado, punto_seleccionado, persona_seleccionada, discusion) # Agregar la discusión a la base de datos

ventana = Main() # Crear la ventana
ventana.main_window.mainloop() # Mostrar la ventana