from customtkinter import Tk, Label, Entry, Button, Listbox
import LogicaAgenda

class AgendaInterface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Agenda Web")
        
        self.agenda = LogicaAgenda.Agenda("", "", 3)
        
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
        
        self.window.mainloop()
    
    def add_participant(self):
        participant_name = self.entry_name.get()
        participant_last_name1 = self.entry_last_name1.get()
        participant_last_name2 = self.entry_last_name2.get()
        
        participant = LogicaAgenda.Participante(participant_name, participant_last_name1, participant_last_name2)
        
        self.agenda.agregar_participante(participant)
        
        self.update_participants_listbox()
        
    def remove_participant(self):
        selected_participant = self.participants_listbox.get(self.participants_listbox.curselection())
        
        for participant in self.agenda.participantes:
            if participant.nombre == selected_participant:
                self.agenda.eliminar_participante(participant)
                break
        
        self.update_participants_listbox()
        
    def update_participants_listbox(self):
        self.participants_listbox.delete(0, "end")
        
        for participant in self.agenda.participantes:
            self.participants_listbox.insert("end", participant.nombre)