import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import speech_recognition as sr
from Logic import seleccionar_archivo, seleccionar_carpeta_destino, dividir_audio, participantes, agenda

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

        boton_seleccionar_archivo = tk.Button(self, text="Seleccionar archivo", command=lambda: seleccionar_archivo(self.ruta_texto))
        boton_seleccionar_archivo.grid(row=1, column=0, padx=10, pady=10)

        self.ruta_texto = tk.Text(self, height=1)
        self.ruta_texto.grid(row=2, column=0, padx=10, pady=10)

        # Etiqueta y campo de texto para especificar la carpeta de destino
        etiqueta_carpeta_destino = tk.Label(self, text="Carpeta de destino:")
        etiqueta_carpeta_destino.grid(row=3, column=0, padx=5, pady=5)

        boton_seleccionar_carpeta = tk.Button(self, text="Seleccionar carpeta", command=lambda: seleccionar_carpeta_destino(self.ruta_carpeta_texto))
        boton_seleccionar_carpeta.grid(row=4, column=0, padx=10, pady=10)

        self.ruta_carpeta_texto = tk.Text(self, height=1)
        self.ruta_carpeta_texto.grid(row=5, column=0, padx=10, pady=10)

        # Botón para iniciar la división del audio
        boton_dividir_audio = tk.Button(self, text="Dividir audio", command=lambda: dividir_audio(self.ruta_carpeta_texto, self.ruta_texto))
        boton_dividir_audio.grid(row=6, column=0, padx=10, pady=10)

class VentanaTranscripcion(ttk.Frame):
    def __init__(self, master, ventana_agenda, ventana_participantes):
        super().__init__(master)
        
        self.agenda = set()
        self.participantes = set()

        # Crear etiqueta y campo de texto para la lista de apartados
        self.label_agenda = ttk.Label(self, text="Lista de Apartados:")
        self.label_agenda.pack(pady=10)
        self.text_agenda = tk.Text(self, height=10, width=50)
        self.text_agenda.pack()

        # Crear etiqueta y campo de texto para la lista de participantes
        self.label_participantes = ttk.Label(self, text="Lista de Participantes:")
        self.label_participantes.pack(pady=10)
        self.text_participantes = tk.Text(self, height=10, width=50)
        self.text_participantes.pack()

        # Crear etiqueta y campo de texto para la transcripción
        self.label_transcripcion = ttk.Label(self, text="Transcripción:")
        self.label_transcripcion.pack(pady=10)
        self.entry_transcripcion = ttk.Entry(self, state="readonly")
        self.entry_transcripcion.pack()

        # Botón para seleccionar archivo de audio
        self.boton_seleccionar_audio = ttk.Button(self, text="Seleccionar archivo de audio", command=self.seleccionar_archivo_audio)
        self.boton_seleccionar_audio.pack(pady=10)

        # Instancias de las pestañas "Registro de agenda" y "Lista de participantes"
        self.ventana_agenda = ventana_agenda
        self.ventana_participantes = ventana_participantes

        # Mostrar los participantes en el campo de texto "Lista de participantes"
        self.actualizar_participantes()
        self.mostrar_participantes()

        # Mostrar los apartados en el campo de texto "Lista de apartados"
        self.actualizar_agenda()
        self.mostrar_agenda()

    def seleccionar_archivo_audio(self):
        # Abrir el explorador de archivos y permitir al usuario seleccionar un archivo de audio
        archivo_audio = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.mp3;*.wav")])

        # Verificar si se seleccionó un archivo de audio
        if archivo_audio:
            # Realizar la transcripción del audio
            transcripcion_texto = self.obtener_transcripcion(archivo_audio)

            # Actualizar el campo de texto de la transcripción
            self.entry_transcripcion.configure(state="normal")
            self.entry_transcripcion.delete(0, tk.END)
            self.entry_transcripcion.insert(0, transcripcion_texto)
            self.entry_transcripcion.configure(state="readonly")

            # Ajustar el ancho del Entry al tamaño del texto de la transcripción
            self.entry_transcripcion.configure(width=len(transcripcion_texto))

    def obtener_transcripcion(self, archivo):
        # Crear un reconocedor de voz
        reconocedor = sr.Recognizer()

        # Cargar el archivo de audio
        with sr.AudioFile(archivo) as fuente:
            # Leer el archivo de audio
            audio = reconocedor.record(fuente)

        try:
            # Realizar la transcripción del audio
            texto = reconocedor.recognize_google(audio, language="es-ES")
            return texto
        except sr.UnknownValueError:
            return "No se pudo transcribir el audio"
        except sr.RequestError as e:
            return f"Error al transcribir el audio: {e}"
        
    def obtener_agenda(self):
        return self.agenda

    def actualizar_agenda(self):
        self.agenda = self.ventana_agenda
        self.mostrar_agenda()

    def mostrar_agenda(self):
        self.text_agenda.delete(1.0, tk.END)
        for apartado, puntos in self.agenda:
            self.text_agenda.insert(tk.END, f"- {apartado}\n")
            for punto in puntos:
                self.text_agenda.insert(tk.END, f"  - {punto}\n")

    def obtener_participantes(self):
        return self.lista_participantes

    def actualizar_participantes(self):
        self.participantes = self.ventana_agenda
        self.mostrar_participantes()

    def mostrar_participantes(self):
        self.text_participantes.delete(1.0, tk.END)
        for participante in self.participantes:
            self.text_participantes.insert(tk.END, f"- {participante}\n")

class VentanaListaParticipantes(ttk.Frame):
    def __init__(self, master, participantes):
        super().__init__(master)
        self.lista_participantes = participantes

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

    def actualizar_tabla_participantes(self):
        self.tabla.delete(*self.tabla.get_children())
        for participante in self.lista_participantes:
            self.tabla.insert("", tk.END, text=participante)

    def seleccionar_fila(self, event):
        # Habilitar botones de editar y eliminar cuando se selecciona una fila
        if self.tabla.selection():
            self.editar_boton.pack(side=tk.LEFT, padx=5)
            self.eliminar_boton.pack(side=tk.LEFT, padx=5)
        else:
            self.editar_boton.pack_forget()
            self.eliminar_boton.pack_forget()

    def editar_participante(self):
        # Obtener fila seleccionada
        fila = self.tabla.selection()[0]
        nombre = self.tabla.item(fila, "text")
        carnet = self.tabla.item(fila, "values")[0]

        # Ventana para editar el participante
        ventana_participante = tk.Toplevel(self.winfo_toplevel())
        ventana_participante.title("Editar Participante")

        label_nombre = tk.Label(ventana_participante, text="Nombre:")
        label_nombre.pack(pady=10)

        entry_nombre = tk.Entry(ventana_participante)
        entry_nombre.insert(tk.END, nombre)
        entry_nombre.pack(pady=10)

        label_carnet = tk.Label(ventana_participante, text="Carnet:")
        label_carnet.pack(pady=10)

        entry_carnet = tk.Entry(ventana_participante)
        entry_carnet.insert(tk.END, carnet)
        entry_carnet.pack(pady=10)

        button_guardar = tk.Button(ventana_participante, text="Guardar", command=lambda: [self.actualizar_participante(fila, entry_nombre.get(), entry_carnet.get()), ventana_participante.destroy()])
        button_guardar.pack(pady=10)

    def eliminar_participante(self):
        # Obtener la fila seleccionada de la tabla
        fila = self.tabla.selection()[0]
        nombre = self.tabla.item(fila, "text")
        
        # Eliminar el participante del conjunto global
        for participante in participantes:
            if nombre == participante[0]:
                participantes.remove(participante)
                break
        
        # Eliminar la fila de la tabla
        self.tabla.delete(fila)

    def agregar_participante(self):
        # Ventana para ingresar nombre y carnet del participante
        ventana_participante = tk.Toplevel(self.winfo_toplevel())
        ventana_participante.title("Agregar Participante")

        label_nombre = tk.Label(ventana_participante, text="Ingrese el nombre del participante:")
        label_nombre.pack(pady=10)

        entry_nombre = tk.Entry(ventana_participante)
        entry_nombre.pack(pady=10)

        label_carnet = tk.Label(ventana_participante, text="Ingrese el carnet del participante:")
        label_carnet.pack(pady=10)

        entry_carnet = tk.Entry(ventana_participante)
        entry_carnet.pack(pady=10)

        button_guardar = tk.Button(ventana_participante, text="Guardar", command=lambda: [self.guardar_participante(entry_nombre.get(), entry_carnet.get()), ventana_participante.destroy()])
        button_guardar.pack(pady=10)

    def guardar_participante(self, nombre, carnet):
        # Verificar si el carnet es un número entero
        try:
            carnet = int(carnet)
        except ValueError:
            messagebox.showerror("Error", "El carnet debe ser un número")
            return

        # Verificar si el carnet ya está en el conjunto de participantes
        for participante in participantes:
            if carnet == int(participante[1]):
                messagebox.showerror("Error", f"El carnet '{carnet}' ya está registrado para otro participante")
                return

        # Agregar el participante al conjunto global
        participantes.add((nombre, carnet))

        # Actualizar la tabla de participantes
        self.tabla.insert("", tk.END, text=nombre, values=(carnet,))

    def actualizar_participante(self, fila, nombre, carnet):
        # Verificar si el carnet es un número entero
        try:
            carnet = int(carnet)
        except ValueError:
            messagebox.showerror("Error", "El carnet debe ser un número")
            return

        # Verificar si el carnet ya está en el conjunto de participantes
        for participante in participantes:
            if carnet == int(participante[1]) and nombre != participante[0]:
                messagebox.showerror("Error", f"El carnet '{carnet}' ya está registrado para otro participante")
                return

        # Eliminar participante anterior
        self.eliminar_participante()

        # Agregar el participante actualizado al conjunto global
        participantes.add((nombre, carnet))

        # Actualizar la tabla de participantes
        self.tabla.insert("", tk.END, text=nombre, values=(carnet,))

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

    def editar_apartado(self):
    # Obtener fila seleccionada
        fila = self.tabla.selection()[0]
        apartado = self.tabla.item(fila, "text")
        punto = self.tabla.item(fila, "values")[0]

        # Ventana para editar el apartado y el punto
        ventana_editar = tk.Toplevel(self.winfo_toplevel())
        ventana_editar.title("Editar Apartado y Punto")

        label_apartado = tk.Label(ventana_editar, text="Apartado:")
        label_apartado.pack(pady=10)

        entry_apartado = tk.Entry(ventana_editar)
        entry_apartado.insert(tk.END, apartado)
        entry_apartado.pack(pady=10)

        label_punto = tk.Label(ventana_editar, text="Punto:")
        label_punto.pack(pady=10)

        entry_punto = tk.Entry(ventana_editar)
        entry_punto.insert(tk.END, punto)
        entry_punto.pack(pady=10)

        button_guardar = tk.Button(ventana_editar, text="Guardar", command=lambda: [self.actualizar_apartado(fila, entry_apartado.get(), entry_punto.get()), ventana_editar.destroy()])
        button_guardar.pack(pady=10)

    def eliminar_apartado(self):
        # Eliminar fila seleccionada de la tabla
        fila = self.tabla.selection()[0]
        self.tabla.delete(fila)
    
    def agregar_apartado_puntos(self):
        # Ventana para ingresar apartado y puntos
        ventana_ap = tk.Toplevel(self.winfo_toplevel())
        ventana_ap.title("Agregar Apartado y Punto")

        label_ap = tk.Label(ventana_ap, text="Ingrese el nombre del apartado:")
        label_ap.pack(pady=10)

        entry_ap = tk.Entry(ventana_ap)
        entry_ap.pack(pady=10)

        label_puntos = tk.Label(ventana_ap, text="Ingrese el punto correspondiente al apartado:")
        label_puntos.pack(pady=10)

        entry_puntos = tk.Entry(ventana_ap)
        entry_puntos.pack(pady=10)

        button_guardar = tk.Button(ventana_ap, text="Guardar", command=lambda: [self.guardar_apartado_puntos(entry_ap.get(), entry_puntos.get()), ventana_ap.destroy()])
        button_guardar.pack(pady=10)

    def guardar_apartado_puntos(self, apartado, punto):
        # Verificar si el apartado ya existe en la lista de apartados
        if apartado in self.apartados:
            # Verificar si el punto ya existe dentro del apartado
            if punto in self.apartados[apartado]:
                messagebox.showerror("Error", f"El punto '{punto}' ya existe en el apartado '{apartado}'")
                return
            else:
                # Agregar el punto al apartado existente
                self.apartados[apartado].append(punto)
        else:
            # Crear un nuevo apartado con el punto correspondiente
            self.apartados[apartado] = [punto]

        # Actualizar la tabla de apartados
        self.tabla.insert("", tk.END, text=apartado, values=(punto))

    def actualizar_apartado(self, fila, apartado, punto):
        # Verificar si el apartado ya existe en la lista de apartados
        if apartado in self.apartados:
            # Verificar si el punto ya existe dentro del apartado
            if punto in self.apartados[apartado]:
                messagebox.showerror("Error", f"El punto '{punto}' ya existe en el apartado '{apartado}'")
                return
            else:
                # Eliminar el punto anterior del apartado
                self.apartados[apartado].remove(self.tabla.item(fila, "values")[0])
                # Agregar el punto actualizado al apartado existente
                self.apartados[apartado].append(punto)
        else:
            # Crear un nuevo apartado con el punto correspondiente
            self.apartados[apartado] = [punto]

        # Actualizar la tabla de apartados
        self.guardar_edicion(fila, apartado, punto)

    def guardar_edicion(self, fila, apartado, punto):
        # Actualizar valores de la fila seleccionada
        self.tabla.item(fila, text=apartado, values=(punto))

    def agregar_apartado_y_punto(apartado, punto):
        # buscar si el apartado ya está en la agenda
        encontrado = False
        for a in agenda:
            if a[0] == apartado:
                # si el apartado existe, agregar el punto al conjunto de puntos del apartado
                a[1].add(punto)
                encontrado = True
                break
        # si el apartado no existe, agregarlo como un nuevo conjunto de puntos
        if not encontrado:
            agenda.add((apartado, {punto}))