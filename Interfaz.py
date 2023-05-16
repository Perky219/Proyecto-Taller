import tkinter as tk
from tkinter import ttk, messagebox
from Avance_Proyecto import registro_agenda, lista_participantes, speech, seleccionar_espacio_agenda, seleccionar_participante
agenda = set()

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

        # agregando VentanaRegistro a la pestaña "Registro de agenda"
        self.ventana_registro = VentanaRegistro(self.tab_registro)
        self.ventana_registro.pack(fill=tk.BOTH, expand=True)

class VentanaRegistro(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.apartados={}

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

    def guardar_apartado_puntos(self, apartado, puntos):
        if apartado not in self.apartados:
            self.apartados[apartado] = [puntos]
        elif puntos in self.apartados[apartado]:
            messagebox.showerror("Error", f"El punto '{puntos}' ya existe en el apartado '{apartado}'")
            return
        else:
            self.apartados[apartado].append(puntos)
        self.tabla.insert("", tk.END, text=apartado, values=(puntos))

    def eliminar_apartado(self):
        # Eliminar fila seleccionada de la tabla
        fila = self.tabla.selection()[0]
        self.tabla.delete(fila)

    def editar_apartado(self):
        # Obtener fila seleccionada
        fila = self.tabla.selection()[0]

        # Obtener valores de la fila seleccionada
        apartado = self.tabla.item(fila, "text")
        puntos = self.tabla.item(fila, "values")[0]

        # Ventana para editar apartado y puntos
        ventana_editar = tk.Toplevel(self.master)
        ventana_editar.title("Editar Apartado y Punto")

        # Crear campos para editar apartado y puntos
        label_ap = tk.Label(ventana_editar, text="Apartado:")
        label_ap.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        campo_ap = tk.Entry(ventana_editar)
        campo_ap.grid(row=0, column=1, padx=5, pady=5)
        campo_ap.insert(0, apartado)

        label_pt = tk.Label(ventana_editar, text="Puntos:")
        label_pt.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        campo_pt = tk.Entry(ventana_editar)
        campo_pt.grid(row=1, column=1, padx=5, pady=5)
        campo_pt.insert(0, puntos)

        # Función para guardar cambios y cerrar la ventana
        def guardar_cambios():
            apartado_nuevo = campo_ap.get()
            puntos_nuevos = campo_pt.get()
            self.tabla.item(fila, text=apartado_nuevo, values=(puntos_nuevos,))
            ventana_editar.destroy()

        # Botón para guardar cambios
        boton_guardar = tk.Button(ventana_editar, text="Guardar", command=guardar_cambios)
        boton_guardar.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

        # Mostrar ventana
        ventana_editar.grab_set()
        ventana_editar.wait_window()

    def guardar_edicion(self, fila, apartado, puntos):
        # Actualizar valores de la fila seleccionada
        self.tabla.item(fila, text=apartado, values=(puntos))

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