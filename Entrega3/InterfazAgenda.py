import customtkinter as ctk
import tkinter.messagebox as messagebox
from LogicaAgenda import crear_agenda
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

        self.agenda_nombre_asignado = False

        self.barra_lateral = ctk.CTkFrame(self.ventana_principal, width=200)
        self.barra_lateral.place(x=10, y=70)

        self.boton_participantes = ctk.CTkButton(self.barra_lateral, text="Participantes", font=("Arial", 14), command=self.mostrar_ventana_participantes)
        self.boton_participantes.pack(pady=10, padx=20, fill="x")

        self.boton_apartados = ctk.CTkButton(self.barra_lateral, text="Apartados", font=("Arial", 14), command=self.mostrar_ventana_apartados)
        self.boton_apartados.pack(pady=10, padx=20, fill="x")

        self.boton_discusion = ctk.CTkButton(self.barra_lateral, text="Discusión", font=("Arial", 14), command=self.mostrar_ventana_discusion)
        self.boton_discusion.pack(pady=10, padx=20, fill="x")

        self.boton_html = ctk.CTkButton(self.barra_lateral, text="Generar HTML", font=("Arial", 14), command=self.generar_html)
        self.boton_html.pack(pady=10, padx=20, fill="x")

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
        VentanaSuperpuesta(self.ventana_principal, "Discusion")

    def generar_html(self):
        if not self.agenda_nombre_asignado:
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.")
            return

    def guardar_agenda(self):
        nombre_agenda = self.entry_nombre_agenda.get()

        if nombre_agenda.strip() == "":
            messagebox.showerror("Error", "Debe agregar un nombre a la agenda.")
            return

        fecha = datetime.today().strftime("%d/%m/%Y")
        nombre = self.entry_nombre_agenda.get()
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
            label_nombre = ctk.CTkLabel(self.mini_window, text="Nombre: ", font=("Arial", 15))
            label_apellido1 = ctk.CTkLabel(self.mini_window, text="Primer Apellido: ", font=("Arial", 15))
            label_apellido2 = ctk.CTkLabel(self.mini_window, text="Segundo Apellido: ", font=("Arial", 15))

            label_nombre.place(x=10, y=10)
            label_apellido1.place(x=10, y=60)
            label_apellido2.place(x=10, y=110)

            entry_nombre = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el nombre", justify="center")
            entry_apellido1 = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el primer apellido", justify="center")
            entry_apellido2 = ctk.CTkEntry(self.mini_window, width=250, placeholder_text="Ingrese el segundo apellido", justify="center")

            entry_nombre.place(x=220, y=10)
            entry_apellido1.place(x=220, y=60)
            entry_apellido2.place(x=220, y=110)

            boton_guardar = ctk.CTkButton(self.mini_window, text="Guardar")
            boton_guardar.place(x=85, y=145)

            boton_eliminar = ctk.CTkButton(self.mini_window, text="Eliminar")
            boton_eliminar.place(x=285, y=145)

            lista_participantes = ctk.CTkTextbox(self.mini_window, width=480, height=200, state="disabled")
            lista_participantes.place(x=10, y=185)

        elif value == "Apartados":
            pass

        elif value == "Discusiones":
            pass

ventana = VentanaPrincipal()
ventana.ventana_principal.mainloop()