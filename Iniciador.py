import tkinter as tk
from Interfaz import VentanaDivisorAudio, VentanaListaParticipantes, VentanaRegistroAgenda, VentanaTranscripcion

class VentanaPrincipal:
    def __init__(self, master):
        """
        Constructor de la clase VentanaPrincipal.

        Args:
            master (): Objeto de la clase Tk.
        """
        self.master = master
        self.agenda = set()  # Conjunto de apartados con sus puntos asignados
        self.participantes = set()  # Conjunto de participantes

        master.title("Interfaz de usuario")

        # creación de pestañas
        self.notebook = tk.ttk.Notebook(master)
        self.tab_registro = tk.Frame(self.notebook)
        self.tab_lista = tk.Frame(self.notebook)
        self.tab_divisor = tk.Frame(self.notebook)
        self.tab_transcripcion = tk.Frame(self.notebook)

        # agregando pestañas al notebook
        self.notebook.add(self.tab_registro, text="Registro de agenda")
        self.notebook.add(self.tab_lista, text="Lista de participantes")
        self.notebook.add(self.tab_divisor, text="Divisor de Audio")
        self.notebook.add(self.tab_transcripcion, text="Transcripción")
        self.notebook.pack(expand=True, fill='both')

        # agregando VentanaRegistroAgenda a la pestaña "Registro de agenda"
        self.ventana_registro = VentanaRegistroAgenda(self.tab_registro)
        self.ventana_registro.pack(fill=tk.BOTH, expand=True)

        # agregando VentanaListaParticipantes a la pestaña "Lista de participantes"
        self.ventana_lista = VentanaListaParticipantes(self.tab_lista, self.participantes)
        self.ventana_lista.pack(fill=tk.BOTH, expand=True)

        # agregando VentanaDivisorAudio a la pestaña "Divisor de Audio"
        self.ventana_divisor = VentanaDivisorAudio(self.tab_divisor)
        self.ventana_divisor.pack(fill=tk.BOTH, expand=True)

        # agregando VentanaTranscripcion a la pestaña "Transcripción"
        self.ventana_transcripcion = VentanaTranscripcion(self.tab_transcripcion, self.ventana_registro.apartados, self.ventana_lista.lista_participantes)
        self.ventana_transcripcion.pack(fill=tk.BOTH, expand=True)

    def actualizar_agenda(self):
        """
        Método para actualizar la agenda en la pestaña de transcripción.

        Args:
            agenda (set): Conjunto de apartados con sus puntos asignados.
        """
        self.ventana_transcripcion.actualizar_agenda(self.agenda)

    def actualizar_participantes(self):
        """
        Método para actualizar la lista de participantes en la pestaña de transcripción.

        Args:
            participantes (set): Conjunto de participantes.
        """
        self.ventana_transcripcion.actualizar_participantes(self.participantes)

    def agregar_participante(self):
        """
        Método para agregar un participante a la lista de participantes.

        Attributes:
            participante (str): Nombre del participante.
        """
        participante = self.ventana_lista.entry_participante.get()
        self.participantes.add(participante)
        self.ventana_lista.actualizar_participantes()  # Llamada al método para actualizar la lista en la pestaña de transcripción
        self.ventana_lista.actualizar_tabla_participantes()  # Llamada al método para actualizar la tabla de participantes
        self.ventana_lista.entry_participante.delete(0, tk.END)  # Limpia la entrada de texto

if __name__ == '__main__':
    root = tk.Tk()
    ventana_principal = VentanaPrincipal(root)
    root.mainloop()