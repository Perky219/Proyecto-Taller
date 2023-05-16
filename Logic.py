import tkinter as tk # Importamos la librería tkinter para crear la interfaz gráfica
from tkinter import filedialog # Importamos el módulo filedialog para abrir el explorador de archivos
from tkinter import messagebox # Importamos el módulo messagebox para mostrar mensajes de error
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import os
agenda = set()
participantes = set()
reporte = []

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

def eliminar_apartado(self):
    # Eliminar fila seleccionada de la tabla
    fila = self.tabla.selection()[0]
    self.tabla.delete(fila)

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

def modificar_participante(punto_general,punto_especifico,carne:str,texto:str):
    """
    Función que permite agregar los datos a la base de datos.

    Args:
        punto_general (str: Punto general de la agenda.
        punto_especifico (str): Punto específico de la agenda.
        carne (str): Carnet de la persona que participó.
        texto (str): Texto reconocido por el speech recognition.
    """
    #Total de palabras por persona en la reunión.
    total_palabras = len(texto.split())
    participantes[carne]["t_palabras"] += total_palabras
    #Participaciones por subtema.
    nombre =  participantes[carne]["nombre"]
    reporte.append([f"{punto_general} - {punto_especifico} - {nombre} - {texto}"])

    #Participaciones por subtema.
    if punto_general in participantes[carne]:
        if punto_especifico in participantes[carne][punto_general]:
            participantes[carne][punto_general][punto_especifico] += 1
        else:
            participantes[carne][punto_general][punto_especifico] = 1
    else:
        participantes[carne][punto_general] = {punto_especifico: 1}

def seleccionar_carpeta_segmentos(ruta_carpeta_texto):
    """
    Función que permite seleccionar la carpeta que contiene los archivos de audio.

    Args:
        ruta_carpeta_texto (str): Ruta de la carpeta que contiene los archivos de audio.

    Returns:
        str: Dirección de la carpeta que contiene los archivos de audio.
    """
    carpeta_segmentos = filedialog.askdirectory()
    ruta_carpeta_texto.delete("1.0", tk.END)
    ruta_carpeta_texto.insert(tk.END, carpeta_segmentos)
    return obtener_archivos_audio(carpeta_segmentos)

def obtener_archivos_audio(carpeta):
    """
    Función que permite obtener los archivos de audio de una carpeta.

    Args:
        carpeta (str): Dirección de la carpeta que contiene los archivos de audio.

    Returns:
        list: Lista con las rutas de los archivos de audio.
    """
    archivos = [] # Lista que contiene las rutas de los archivos de audio.
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".mp3") or archivo.endswith(".wav"):
            ruta_archivo = carpeta+"/"+archivo # Obtiene la ruta completa del archivo
            #ruta_archivo.replace("\\", "/")   Reemplazar barras invertidas con barras inclinadas hacia adelante
            archivos.append(ruta_archivo)
    return archivos

def corregir_ruta_archivo(ruta_archivo):
    """
    Función que permite corregir la ruta de un archivo al formato correcto para el speech recognition.

    Args:
        ruta_archivo (str): Str qur contiene la ruta del archivo.

    Returns:
        str: Ruta del archivo corregida.
    """
    # Corregir la ruta del archivo al formato correcto para el speech recognition.
    ruta_absoluta = os.path.abspath(ruta_archivo)
    ruta_carpeta = os.path.dirname(ruta_absoluta)
    nombre_archivo = os.path.basename(ruta_absoluta)
    ruta_corregida = os.path.join(ruta_carpeta, nombre_archivo)
    return ruta_corregida

def convertir_audio_a_texto(archivo_audio):
    """
    Función que permite convertir un archivo de audio a texto.

    Args:
        archivo_audio (str): Ruta del archivo de audio.

    Returns:
        str: Transcripción del archivo de audio.
    """

    r = sr.Recognizer()
    with sr.AudioFile(archivo_audio) as fuente:
        audio = r.record(fuente)

    try:
        texto = r.recognize_google(audio, language="es-ES")
        return texto
    except sr.UnknownValueError:
        tk.messagebox.showwarning("No se pudo reconocer el audio.")
    except sr.RequestError as e:
        tk.messagebox.showwarning(f"Error al realizar la solicitud al servicio de reconocimiento de voz de Google: {e}")


def seleccionar_archivo(ruta_texto):
    """
    Función que permite seleccionar un archivo de audio.

    Args:
        ruta_texto (str): Ruta del archivo de audio.
    """
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.wav")])
    ruta_texto.delete("1.0", tk.END)
    ruta_texto.insert(tk.END, archivo)

def seleccionar_carpeta_destino(ruta_carpeta_texto):
    """
    Función que permite seleccionar la carpeta de destino de los archivos de audio.

    Args:
        ruta_carpeta_texto (str): Ruta de la carpeta de destino de los archivos de audio.

    Returns:
        str: Dirección de la carpeta de destino de los archivos de audio.
    """
    carpeta_destino = filedialog.askdirectory()
    ruta_carpeta_texto.delete("1.0", tk.END)
    ruta_carpeta_texto.insert(tk.END, carpeta_destino)
    return carpeta_destino

def dividir_audio(ruta_carpeta_texto, ruta_texto):
    """
    Función que permite dividir un archivo de audio en segmentos.

    Args:
        ruta_carpeta_texto (_type_): _description_
        ruta_texto (_type_): _description_
    """
    archivo = ruta_texto.get("1.0", tk.END).strip()
    carpeta_destino = ruta_carpeta_texto.get("1.0", tk.END).strip()

    if archivo == "" or carpeta_destino == "":
        tk.messagebox.showwarning("Advertencia", "Por favor, seleccione el archivo de audio y la carpeta de destino.")
        return

    duracion_pausa_ms = 3000

    audio = AudioSegment.from_file(archivo, format="wav")
    segmentos = split_on_silence(audio, min_silence_len=duracion_pausa_ms, silence_thresh=-50)

    for i, segmento in enumerate(segmentos):
        segmento.export(f"{carpeta_destino}/segmento_{i}.wav", format="wav")

    tk.messagebox.showinfo("Fin del proceso", "Se ha dividido el audio en segmentos correctamente.")

def eliminar_segmento_usado(elemento,archivo):
    """
    Función que permite eliminar un elemento de una lista.

    Args:
        elemento (str): Elemento a eliminar.
        archivo (str): Lista con elementos.

    Returns:
        list: Lista sin el elemento eliminado.
    """
    if elemento in archivo:
        archivo.remove(elemento)
    return archivo