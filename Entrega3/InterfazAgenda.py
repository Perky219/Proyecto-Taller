from tkinter import Tk, Label, Entry, Button
import datetime

class AgendaInterface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Agenda Web")
        
        # Obtener la fecha actual
        fecha_actual = datetime.date.today()
        
        # Crear etiqueta y campo de entrada para el título
        self.label_title = Label(self.window, text="Título:")
        self.entry_title = Entry(self.window)
        
        # Crear etiqueta para la fecha de creación
        self.label_date = Label(self.window, text="Fecha de creación:")
        self.label_date_value = Label(self.window, text=str(fecha_actual))
        
        # Crear botón para guardar el título
        self.button_save_title = Button(self.window, text="Guardar título", command=self.save_title)
        
        # Posicionamiento de los elementos en la ventana usando grid
        self.label_title.grid(row=0, column=0, sticky="e")
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)
        self.label_date.grid(row=1, column=0, sticky="e")
        self.label_date_value.grid(row=1, column=1, padx=5, pady=5)
        self.button_save_title.grid(row=2, columnspan=2, padx=5, pady=5)
        
        self.window.mainloop()
    
    def save_title(self):
        title = self.entry_title.get()
        self.entry_title.config(state="disabled")
        self.button_save_title.config(state="disabled")
        
AgendaInterface()