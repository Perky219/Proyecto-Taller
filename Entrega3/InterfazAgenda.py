import customtkinter as ctk
import tkinter.messagebox as messagebox
from NuevaAgenda import MiAgenda
from datetime import datetime

agenda = None

class VentanaPrincipal:
    """Clase que crea la ventana principal de la aplicación
    """
    def __init__(self):
        """Constructor de la clase VentanaPrincipal"""
        # SE CREA LA VENTANA PRINCIPAL Y SE LE DA UN TAMAÑO Y UN TITULO
        self.ventana_principal = ctk.CTk()
        self.ventana_principal.geometry("750x500")
        self.ventana_principal.title("Agenda Web")
        self.ventana_principal._set_appearance_mode("dark")

        # # SE CREA EL BOTON DE OPCIONES Y SE LE DA UN TAMAÑO Y UNA POSICION, CONJUNTO DE TODA SU CONFIGURACION Y DETALLES
        # self.btn_opciones = ctk.CTkSegmentedButton(self.ventana_principal, selected_color="red", values=["Apartados", "Participantes", "Discusiones"], command=lambda value: self.segmented_button_callback(value))
        # self.btn_opciones.configure(unselected_color="blue")
        # self.btn_opciones.configure(font=("Arial", 15))
        # self.btn_opciones.configure(fg_color="sky blue")
        # self.btn_opciones.configure(corner_radius=10)
        # self.btn_opciones.configure(border_width=5)
        # self.btn_opciones.pack(side="top", fill="x", padx=30, pady=70)

        # SE CREA EL LABEL DE NOMBRE DE LA AGENDA Y SE LE DA UNA POSICION Y UNA CONFIGURACION
        self.nombre_agenda = ctk.CTkLabel(self.ventana_principal, text="Nombre para la Agenda:", font=("Arial", 18, "bold"))
        self.nombre_agenda.place(x=32, y=20)

        # SE CREA EL ENTRY DE NOMBRE DE LA AGENDA Y SE LE DA UNA POSICION Y UNA CONFIGURACION
        self.entry_nombre_agenda = ctk.CTkEntry(self.ventana_principal, width=250, placeholder_text="Nombre de la agenda", justify="center")
        self.entry_nombre_agenda.place(x=235, y=21)

        # SE CREA EL BOTON DE GUARDAR Y SE LE DA UNA POSICION Y UNA CONFIGURACION
        self.btn_guardar_agenda = ctk.CTkButton(self.ventana_principal, text="Guardar nombre de la agenda", font=("Arial", 15), command=self.guardar_agenda)
        self.btn_guardar_agenda.place(x=500, y=21)
        self.btn_guardar_agenda.configure(fg_color="black")

        # SE CREA LA VARIABLE DE INSTANCIA PARA LA BARRA DE ENTRADA DE LA AGENDA
        self.agenda_nombre_asignado = False  # VARIABLE DE INSTANCIA PARA SABER SI SE HA ASIGNADO UN NOMBRE A LA AGENDA

        # SE INICIA EL BUCLE DE LA VENTANA PRINCIPAL
        self.ventana_principal.mainloop()

    def segmented_button_callback(self, value):
        """Función que se ejecuta cuando se presiona un botón del SegmentedButton de opciones de la ventana principal
        """
        if not self.agenda_nombre_asignado:  # Verificar si se ha asignado un nombre a la agenda
            messagebox.showerror("Error", "Debe asignar un nombre a la agenda primero.")
            return
        ventana_secundaria = VentanaSecundaria(self.ventana_principal, value, self.btn_opciones)

    def guardar_agenda(self):
        """Función que se ejecuta cuando se presiona el botón de guardar agenda
        sirve para guardar el nombre de la agenda y desactivar los botones de agregar nombre de la agenda y guardar agenda"""
        global agenda

        nombre_agenda = self.entry_nombre_agenda.get()

        if nombre_agenda.strip() == "":
            messagebox.showerror("ERROR!!", "Debe agregar un nombre a la agenda")
            return

        fecha = datetime.today().strftime("%d/%m/%Y")
        agenda = MiAgenda(self.entry_nombre_agenda.get(), fecha)

        if agenda:
            self.entry_nombre_agenda.destroy()
            self.btn_guardar_agenda.destroy()

            self.label_agenda = ctk.CTkLabel(self.ventana_principal, text=agenda.titulo, font=("Arial", 18, "bold"))
            self.label_agenda.place(x=235, y=20)

            self.label_fecha = ctk.CTkLabel(self.ventana_principal, text= "Fecha: " + fecha, font=("Arial", 18, "bold"))
            self.label_fecha.place(x=500, y=20)

            self.agenda_nombre_asignado = True  # Marcar que se ha asignado un nombre a la agenda

class VentanaSecundaria:
    """Clase que crea la ventana secundaria de la aplicación"""

    def __init__(self, ventana_principal, value, btn_opciones):
        """Constructor de la clase VentanaSecundaria"""
        self.mini_window = ctk.CTkFrame(ventana_principal, fg_color="gray")
        self.mini_window.place(x=30, y=110, relwidth=btn_opciones.winfo_width() / ventana_principal.winfo_width(), relheight=0.75)
        self.barra_adicional_puntos = None  # VARIABLE PARA AGREGAR PUNTOS EN APARTADOS
        self.barra_discusion = None  # VARIABLE PARA AGREGAR DISCUSIONES EN APARTADOS
        self.agenda = MiAgenda(titulo="", fecha= "")

        if value == "Apartados":
            label_apartados = ctk.CTkLabel(self.mini_window, text=" Apartados: ", font=("Arial", 15))
            label_puntos = ctk.CTkLabel(self.mini_window, text= "Puntos: ", font=("Arial", 15))

            label_apartados.configure(bg_color="green")
            label_puntos.configure(bg_color= "green")

            label_apartados.place(x=10, y=10)
            label_puntos.place(x=10, y=50)

            barra_entrada = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el apartado", justify="center")
            barra_entrada.place(x=250, y=10) # Creamos la barra de entrada

            barra_entrada_puntos = ctk.CTkEntry(self.mini_window, width=250, placeholder_text= "Ingrese el punto correspondiente", justify="center")
            barra_entrada_puntos.place(x=250, y=50)

            btn_guardar = ctk.CTkButton(self.mini_window, text="Guardar", command= lambda: self.agenda.agregar_apartado(    ))
            btn_guardar.place(x=200, y=100) # Le damos una posicion al boton de guardar

            btn_eliminar = ctk.CTkButton(self.mini_window, text="Eliminar")
            btn_eliminar.place(x=400, y=100)

        elif value == "Participantes":
            nombre = ctk.CTkLabel(self.mini_window, text="Nombre: ", font=("Arial", 15))
            apellido1 = ctk.CTkLabel(self.mini_window, text="Primer Apellido: ", font=("Arial", 15))
            apellido2 = ctk.CTkLabel(self.mini_window, text="Segundo Apellido: ", font=("Arial", 15))

            nombre.configure(bg_color="green")
            apellido1.configure(bg_color="green")
            apellido2.configure(bg_color="green")

            nombre.place(x=10, y=10)
            apellido1.place(x=10, y=60)
            apellido2.place(x=10, y=110)

            barra_entrada_nombre = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el nombre", justify="center")
            barra_entrada_apellido1 = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el primer apellido", justify="center")
            barra_entrada_apellido2 = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el segundo apellido", justify="center")

            barra_entrada_nombre.place(x=220, y=10)
            barra_entrada_apellido1.place(x=220, y=60)
            barra_entrada_apellido2.place(x=220, y=110)

            btn_guardar = ctk.CTkButton(self.mini_window, text="Guardar")
            btn_guardar.place(x=520, y=10)
            btn_guardar.configure(command= self.agenda.agregar_participante(barra_entrada_nombre, barra_entrada_apellido1, barra_entrada_apellido2))

            btn_eliminar = ctk.CTkButton(self.mini_window, text="Eliminar")
            btn_eliminar.place(x=520, y=45)

        elif value == "Discusiones":
            label_seleccionar_apartados = ctk.CTkLabel(self.mini_window, text=" Seleccione el apartado: ", font=("Arial", 15))
            label_seleccionar_punto = ctk.CTkLabel(self.mini_window, text=" Seleccione el punto: ", font=("Arial", 15))
            label_seleccionar_participante = ctk.CTkLabel(self.mini_window, text=" Seleccione el participante: ", font=("Arial", 15))
            label_seleccionar_discusiones = ctk.CTkLabel(self.mini_window, text=" Seleccione la discusión: ", font=("Arial", 15))
            discusion = ctk.CTkLabel(self.mini_window, text=" Discusion: ", font=("Arial", 15))

            menu_opciones_apartados = ctk.CTkOptionMenu(self.mini_window, values=["Apartados"])
            menu_opciones_puntos = ctk.CTkOptionMenu(self.mini_window, values=["Puntos"])
            menu_opciones_participantes = ctk.CTkOptionMenu(self.mini_window, values=["Participantes"])
            menu_opciones_discusion = ctk.CTkOptionMenu(self.mini_window, values=["Discusiones"])

            menu_opciones_apartados.configure(dropdown_fg_color= "cyan")
            menu_opciones_puntos.configure(dropdown_fg_color="cyan")
            menu_opciones_participantes.configure(dropdown_fg_color="cyan")
            menu_opciones_discusion.configure(dropdown_fg_color="cyan")

            label_seleccionar_apartados.configure(bg_color="orange")
            label_seleccionar_punto.configure(bg_color="orange")
            label_seleccionar_participante.configure(bg_color="orange")
            label_seleccionar_discusiones.configure(bg_color="orange")
            discusion.configure(bg_color="orange")

            label_seleccionar_apartados.place(x=50, y=10)
            label_seleccionar_punto.place(x=50, y=80)
            label_seleccionar_participante.place(x=50, y=150)
            label_seleccionar_discusiones.place(x=50, y=210)
            discusion.place(x=50, y=260)

            menu_opciones_apartados.place(x=250, y=10)
            menu_opciones_puntos.place(x=250, y=80)
            menu_opciones_participantes.place(x=250, y=150)
            menu_opciones_discusion.place(x=250, y=210)

            btn_guardar = ctk.CTkButton(self.mini_window, text="Guardar")
            btn_guardar.place(x=520, y=10)

            btn_eliminar = ctk.CTkButton(self.mini_window, text="Eliminar")
            btn_eliminar.place(x=520, y=45)

            btn_modificar = ctk.CTkButton(self.mini_window, text="Modificar", command=self.desplegar_entrada_discusion)
            btn_modificar.place(x=520, y=80)

            btn_imprimir = ctk.CTkButton(self.mini_window, text= "Imprimir en HTML")
            btn_imprimir.place(x=520, y=115)

    def desplegar_entrada_discusion(self):
        if self.barra_discusion is None:
            self.barra_discusion = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese la discusión", justify="center")
            self.barra_discusion.place(x=250, y=260)
        else:
            self.barra_discusion.destroy()
            self.barra_discusion = None

ventana = VentanaPrincipal()
ventana.ventana_principal.mainloop()