import tkinter as tk
from tkinter import ttk, messagebox
from Avance_Proyecto import registro_agenda, lista_participantes, speech, seleccionar_espacio_agenda, seleccionar_participante
agenda = set()
participantes = set()

class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        master.title("App")

        # creación de pestañas
        self.notebook = tk.ttk.Notebook(master)
        self.tab_registro = tk.Frame(self.notebook)
        self.tab_lista = tk.Frame(self.notebook)
        self.tab_speech = tk.Frame(self.notebook)

        # agregando pestañas al notebook
        self.notebook.add(self.tab_registro, text="Registro de agenda")
        self.notebook.add(self.tab_lista, text="Lista de participantes")
        self.notebook.add(self.tab_speech, text="Reconocimiento de voz")
        self.notebook.pack(expand=True, fill='both')

        # agregando VentanaRegistroAgenda a la pestaña "Registro de agenda"
        self.ventana_registro = VentanaRegistroAgenda(self.tab_registro)
        self.ventana_registro.pack(fill=tk.BOTH, expand=True)

        # agregando VentanaListaParticipantes a la pestaña "Lista de participantes"
        self.ventana_lista = VentanaListaParticipantes(self.tab_lista)
        self.ventana_lista.pack(fill=tk.BOTH, expand=True)

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

if __name__ == '__main__':
    root = tk.Tk()
    ventana_principal = VentanaPrincipal(root)
    root.mainloop()