from customtkinter import Tk, Label, Entry, Button, Listbox
#import agenda_logic

class AgendaInterface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Agenda Web")
        
        # Crear etiquetas y campos de entrada para el registro de agenda
        self.label_title = Label(self.window, text="Título:")
        self.entry_title = Entry(self.window)
        self.label_date = Label(self.window, text="Fecha de creación:")
        self.entry_date = Entry(self.window)
        
        # Crear lista para mostrar participantes
        self.participants_listbox = Listbox(self.window)
        
        # Crear botones para agregar participantes y eliminar participantes seleccionados
        self.button_add_participant = Button(self.window, text="Agregar Participante", command=self.add_participant)
        self.button_remove_participant = Button(self.window, text="Eliminar Participante", command=self.remove_participant)
        
        # Otros elementos de la interfaz...
        
        # Configurar el posicionamiento de los elementos en la ventana
        self.label_title.pack()
        self.entry_title.pack()
        self.label_date.pack()
        self.entry_date.pack()
        self.participants_listbox.pack()
        self.button_add_participant.pack()
        self.button_remove_participant.pack()
        
        # Iniciar la interfaz
        self.window.mainloop()
    
    def add_participant(self):
        # Lógica para agregar un participante a la agenda
        # Obtener los datos del participante desde los campos de entrada
        participant_name = self.entry_name.get()
        participant_last_name1 = self.entry_last_name1.get()
        participant_last_name2 = self.entry_last_name2.get()
        
        # Crear una instancia de la clase Participante
#        participant = agenda_logic.Participante(participant_name, participant_last_name1, participant_last_name2)
        
        # Agregar el participante a la agenda
        
        # Actualizar la lista de participantes en la interfaz
        
    def remove_participant(self):
        # Lógica para eliminar un participante seleccionado de la agenda
        
        # Obtener el participante seleccionado desde la lista
        pass
