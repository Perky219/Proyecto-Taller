import tkinter as tk
from tkinter import ttk, messagebox
from Logic import eliminar_segmento_usado, convertir_audio_a_texto, corregir_ruta_archivo, seleccionar_carpeta_segmentos, modificar_participante, seleccionar_archivo, seleccionar_carpeta_destino, dividir_audio, participantes, agenda    

class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        master.title("App")

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
        self.ventana_lista = VentanaListaParticipantes(self.tab_lista)
        self.ventana_lista.pack(fill=tk.BOTH, expand=True)

        # agregando VentanaDivisorAudio a la pestaña "Divisor de Audio"
        self.ventana_divisor = VentanaDivisorAudio(self.tab_divisor)
        self.ventana_divisor.pack(fill=tk.BOTH, expand=True)

        # agregando VentanaTranscripcion a la pestaña "Transcripción"
        self.ventana_transcripcion = VentanaTranscripcion(self.tab_transcripcion)

class VentanaDivisorAudio(tk.Frame):
    """
    Clase que contiene los elementos de la ventana de división de audio.
    """
    def __init__(self, ventana=None):
        """
        Constructor de la clase divisor_audio.
        """
        super().__init__(ventana, width=700, height=500)
        self.ventana = ventana

        # Etiqueta y botón para seleccionar el archivo de audio
        etiqueta_archivo = tk.Label(self, text="Archivo de audio:")
        etiqueta_archivo.grid(row=0, column=0, padx=5, pady=5)
        etiqueta_archivo.config(font=("arial", 12, "bold"))

        boton_seleccionar_archivo = tk.Button(self, text="Seleccionar archivo", command=lambda: seleccionar_archivo(self.ruta_texto))
        boton_seleccionar_archivo.grid(row=1, column=0, padx=10, pady=10)
        boton_seleccionar_archivo.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

        self.ruta_texto = tk.Text(self, height=1)
        self.ruta_texto.grid(row=2, column=0, padx=10, pady=10)

        # Etiqueta y campo de texto para especificar la carpeta de destino
        etiqueta_carpeta_destino = tk.Label(self, text="Carpeta de destino:")
        etiqueta_carpeta_destino.grid(row=3, column=0, padx=5, pady=5)
        etiqueta_carpeta_destino.config(font=("arial", 12, "bold"))

        boton_seleccionar_carpeta = tk.Button(self, text="Seleccionar carpeta", command=lambda: seleccionar_carpeta_destino(self.ruta_carpeta_texto))
        boton_seleccionar_carpeta.grid(row=4, column=0, padx=10, pady=10)
        boton_seleccionar_carpeta.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

        self.ruta_carpeta_texto = tk.Text(self, height=1)
        self.ruta_carpeta_texto.grid(row=5, column=0, padx=10, pady=10)

        # Botón para iniciar la división del audio
        boton_dividir_audio = tk.Button(self, text="Dividir audio", command=lambda: dividir_audio(self.ruta_carpeta_texto, self.ruta_texto))
        boton_dividir_audio.grid(row=6, column=0, padx=10, pady=10)
        boton_dividir_audio.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

class VentanaTranscripcion(tk.Frame):
    """
    Clase que crea un frame de transcripción.
    """
    def __init__(self, ventana=None):
        """
        Constructor de mi clase transcripción.
        """
        super().__init__(ventana, width=700, height=500)
        self.ventana = ventana

        # Etiqueta y botón para seleccionar el archivo de audio.
        self.boton_seleccionar_archivo = tk.Button(self, text="Seleccionar archivo",
                                                   command=self.mostar_tabla_segmentos)
        self.boton_seleccionar_archivo.grid(row=0, column=0, padx=5, pady=10,columnspan=2)
        self.boton_seleccionar_archivo.config(width=30, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

        self.ruta_texto = tk.Text(self, height=1, width=30)
        self.ruta_texto.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.ruta_texto.config(width = 50 , font = ("arial",12, ))

        # Crear el label con texto rojo, centrado y dos líneas
        texto = "El audio debe de estar segmentado \n si lo necesita utilice la función dividir audio"
        self.advertencia = tk.Label(self, text=texto, foreground="red", justify="center", wraplength=200, height=2,font=("arial", 8, "bold"))
        self.advertencia.grid(row=2, column=0, padx=10, pady=10,ipadx=10, ipady=10,columnspan=2)

        self.tabla = None  # Agregamos el atributo de la tabla

    def almacenar_información(self, parrafo: str):
        """
        Almacena la información de la transcripción en un diccionario.
        """
        # Ocultar elementos de la interfaz
        self.tabla.grid_forget()
        self.boton_transcribir.grid_forget()
        self.boton_ver_reportes.grid_forget()

        # Label de selección de tema y subtema
        self.label_persona = tk.Label(self, text="Seleccione el carnet de la persona correspondiente")
        self.label_persona.config(font = ("arial",10, "bold"))
        self.label_persona.grid(row=0, column=0,sticky="w")

        self.label_general = tk.Label(self, text="Seleccione el tema correspondiente")
        self.label_general.config(font = ("arial",10, "bold"))
        self.label_general.grid(row=1, column=0,sticky="w")

        self.label_especifico = tk.Label(self, text="Seleccione el subtema correspondiente")
        self.label_especifico.config(font = ("arial",10, "bold"))
        self.label_especifico.grid(row=2, column=0,sticky="w")

        # Botones de selección de tema y subtema
        self.opcion_seleccionada_persona = tk.StringVar(value=list(participantes.keys())[0])  # Valor inicial predeterminado
        self.opcion_persona = tk.OptionMenu(self, self.opcion_seleccionada_persona, *participantes.keys())
        self.opcion_persona.grid(row=0, column=1,padx=10, pady=10, sticky="ew")

        self.opcion_seleccionada = tk.StringVar(value=list(agenda.keys())[0])  # Valor inicial predeterminado
        self.opcion_general = tk.OptionMenu(self, self.opcion_seleccionada, *agenda.keys(), command=lambda _: self.actualizar_opcion_especifica())
        self.opcion_general.grid(row=1, column=1,padx=10, pady=10, sticky="ew")

        self.opcion_seleccionada_especifica = tk.StringVar(value=list(agenda[self.opcion_seleccionada.get()])[0])
        self.opcion_especifica = tk.OptionMenu(self, self.opcion_seleccionada_especifica, *agenda[self.opcion_seleccionada.get()])
        self.opcion_especifica.grid(row=2, column=1,padx=10, pady=10, sticky="ew")

        # Entry para mostrar el texto transcrito
        self.parrafo = parrafo
        self.texto_variable = tk.StringVar(value=self.parrafo)

        self.texto_entry = tk.Text(self, height=5, width=30)
        self.texto_entry.insert(tk.END, self.parrafo)
        self.texto_entry.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky="nsew")

        # Botón para guardar los cambios
        self.boton_agregar = tk.Button(self, text="Agregar", command=self.guardar_cambios)
        self.boton_agregar.grid(row=5, column=0, padx=5, pady=5)
        self.boton_agregar.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

    def actualizar_opcion_especifica(self):
        """
        Actualiza la opción específica de acuerdo a la opción general seleccionada.
        """
        # Eliminar el menú de opciones específicas actual.
        self.opcion_especifica.grid_forget()

        # Crear el nuevo menú de opciones específicas nuevo y asigna el valor predeterminado.
        self.opcion_seleccionada_especifica = tk.StringVar(value=list(agenda[self.opcion_seleccionada.get()])[0])
        self.opcion_especifica = tk.OptionMenu(self, self.opcion_seleccionada_especifica, *agenda[self.opcion_seleccionada.get()])
        self.opcion_especifica.grid(row=1, column=1, padx=2, pady=5)

    def guardar_cambios(self):
        """
        Guarda la información de la transcripción en un diccionario.
        """
        punto_general = self.opcion_seleccionada.get()
        punto_especifico = self.opcion_seleccionada_especifica.get()
        carnet = self.opcion_seleccionada_persona.get()
        texto = self.texto_entry.get("1.0", tk.END)
        modificar_participante(punto_general, punto_especifico, carnet, texto) # Agregar información a la base de datos
        self.actualizar_tabla_segmentos()# Actualizar tabla de segmentos

        # Terminar proceso de transcripción automáticamente
        if len(self.archivos) == 0:
            self.mostrar_reportes()   

    def actualizar_tabla_segmentos(self):
        """
        Actualiza la tabla de segmentos de la interfaz.
        """
        # Olvidar elementos de la interfaz
        for widget in self.winfo_children():
            widget.grid_forget()

        # Mostrar elementos de la interfaz
        self.tabla_segmentos(self.archivos)

    def mostar_tabla_segmentos(self):
        """
        Muestra la tabla de segmentos de la interfaz y elimina elementos de la interfaz.
        """
        archivos = seleccionar_carpeta_segmentos(self.ruta_texto)
        self.archivos = archivos # Guardar los archivos para usarlos en otros métodos.
        self.tabla_segmentos(self.archivos)

        # Olvidar botones y entry de la interfaz
        self.boton_seleccionar_archivo.grid_forget()
        self.ruta_texto.grid_forget()
        self.advertencia.grid_forget()

    def tabla_segmentos(self, archivos):
        """
        Crea la tabla de segmentos de la interfaz con sus respectivos botones.

        Args:
            archivos (list): Lista con las rutas de los archivos de audio.
        """
        #NOTA : Agregar label para la tabla

        contenedor_tabla = tk.Frame(self)
        contenedor_tabla.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        self.tabla = ttk.Treeview(contenedor_tabla, height=10)
        self.tabla["columns"] = ("Archivo")

        self.tabla.column("#0", width=0, stretch=tk.NO)
        self.tabla.column("Archivo", anchor=tk.W, width=400)

        # Encabezado de la tabla.
        self.tabla.heading("#0", text="")
        self.tabla.heading("Archivo", text="Segmentos de audio")

        # Insertar los segmentos en la tabla.
        for archivo in archivos:
            self.tabla.insert("", tk.END, text="", values=(archivo))

        self.tabla.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.tabla.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # Botón para iniciar la transcripción
        self.boton_transcribir = tk.Button(self, text="Transcribir", state=tk.DISABLED,
                                           command=self.transcribir_audio_seleccionado)
        self.boton_transcribir.grid(row=4, column=0, padx=10, pady=10)
        self.boton_transcribir.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")

        # Botón para finalizar la transcripción
        self.boton_ver_reportes = tk.Button(self, text="Finalizar",
                                           command=self.mostrar_reportes)
        self.boton_ver_reportes.grid(row=4, column=3, padx=10, pady=10)
        self.boton_ver_reportes.config(width=20, font=("arial", 12, "bold"), bg="#34495E", activebackground="#B0BEC5", fg="white", cursor="hand2")
    
    def on_item_selected(self, event = None):
        """
        Habilita el botón de transcribir cuando se selecciona un item de la tabla.
        """
        # Obtener el item seleccionado.
        item = self.tabla.selection()

        if item:
            self.boton_transcribir.config(state=tk.NORMAL)
        else:
            self.boton_transcribir.config(state=tk.DISABLED)

    def transcribir_audio_seleccionado(self):
        """
        Llama a las funciones necesarias para traducir el audio seleccionado.
        """
        # Segmento seleccionado.
        selected_item = self.tabla.focus()
        if selected_item:
            archivo_seleccionado = self.tabla.item(selected_item)["values"][0]
            ruta_corregida = corregir_ruta_archivo(archivo_seleccionado) # Corregir la ruta del archivo
            texto_transcrito = convertir_audio_a_texto(ruta_corregida) # Convertir el audio a texto
            self.almacenar_información(texto_transcrito) # Almacenar la información en la base de datos
            eliminar_segmento_usado(archivo_seleccionado,self.archivos) # Eliminar el segmento de la lista de segmentos

class VentanaListaParticipantes(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.participantes = set()

        # Crear tabla de participantes
        self.tabla = ttk.Treeview(self, columns=("Carnet"))
        self.tabla.heading("#0", text="Nombre")
        self.tabla.heading("#1", text="Carnet")
        self.tabla.column("#1", width=200)
        self.tabla.pack(expand=True, fill=tk.BOTH)

        # Agregar botones para editar y eliminar
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.editar_boton = ttk.Button(self, text="Editar", command=self.editar_participante)
        self.eliminar_boton = ttk.Button(self, text="Eliminar", command=self.eliminar_participante)

        # Agregar botón para agregar participante
        agregar_boton = ttk.Button(self, text="Agregar participante", command=self.agregar_participante)
        agregar_boton.pack(pady=10)

    def seleccionar_fila(self, event):
        # Habilitar botones de editar y eliminar cuando se selecciona una fila
        if self.tabla.selection():
            self.editar_boton.pack(side=tk.LEFT, padx=5)
            self.eliminar_boton.pack(side=tk.LEFT, padx=5)
        else:
            self.editar_boton.pack_forget()
            self.eliminar_boton.pack_forget()

class VentanaRegistroAgenda(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.apartados = {}

        # Crear tabla de apartados
        self.tabla = ttk.Treeview(self, columns=("Puntos"))
        self.tabla.heading("#0", text="Apartado")
        self.tabla.heading("#1", text="Puntos")
        self.tabla.column("#1", width=400)
        self.tabla.pack(expand=True, fill=tk.BOTH)

        # Agregar botones para editar y eliminar
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.editar_boton = ttk.Button(self, text="Editar", command=self.editar_apartado)
        self.eliminar_boton = ttk.Button(self, text="Eliminar", command=self.eliminar_apartado)

        # Agregar botón para agregar apartado y puntos
        agregar_boton = ttk.Button(self, text="Agregar apartado y punto", command=self.agregar_apartado_puntos)
        agregar_boton.pack(pady=10)

    def seleccionar_fila(self, event):
        # Habilitar botones de editar y eliminar cuando se selecciona una fila
        if self.tabla.selection():
            self.editar_boton.pack(side=tk.LEFT, padx=5)
            self.eliminar_boton.pack(side=tk.LEFT, padx=5)
        else:
            self.editar_boton.pack_forget()
            self.eliminar_boton.pack_forget()

if __name__ == '__main__':
    root = tk.Tk()
    ventana_principal = VentanaPrincipal(root)
    root.mainloop()