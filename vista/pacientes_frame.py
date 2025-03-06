import tkinter as tk
from tkinter import ttk, messagebox
# Ya no es necesario importar validaciones desde aquí, se usa el modelo

class PacientesFrame(tk.Frame):
    def __init__(self, parent, gestor_principal):
        super().__init__(parent)
        self.gestor = gestor_principal
        self.crear_widgets()
        self.paciente_seleccionado = None  # <--  Para guardar la selección

    def crear_widgets(self):
        tk.Label(self, text="Nombre Completo:").grid(row=0, column=0, sticky="e")
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.grid(row=0, column=1, sticky="ew")

        tk.Label(self, text="RUT:").grid(row=1, column=0, sticky="e")  # Nuevo campo RUT
        self.entry_rut = tk.Entry(self)
        self.entry_rut.grid(row=1, column=1, sticky="ew")

        tk.Label(self, text="Edad:").grid(row=2, column=0, sticky="e")
        self.entry_edad = tk.Entry(self)
        self.entry_edad.grid(row=2, column=1, sticky="ew")

        tk.Button(self, text="Registrar Paciente", command=self.registrar_paciente).grid(row=3, column=0, columnspan=2, pady=5)

        self.lista_pacientes = ttk.Treeview(self, columns=("Nombre", "RUT", "Edad"), show='headings', height=5)
        self.lista_pacientes.heading("Nombre", text="Nombre Completo")
        self.lista_pacientes.heading("RUT", text="RUT")  # Encabezado para RUT
        self.lista_pacientes.heading("Edad", text="Edad")
        self.lista_pacientes.grid(row=4, column=0, columnspan=2, pady=5, sticky="nsew")
        self.lista_pacientes.bind("<<TreeviewSelect>>", self.seleccionar_paciente) # <--  Importante!

        tk.Button(self, text="Ver Historial", command=self.ver_historial).grid(row=5, column=0, columnspan=2, pady=5)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)  # Ajustar fila de la lista

    def ver_historial(self):
        if self.paciente_seleccionado: # <--  Usa paciente_seleccionado
            self.gestor.mostrar_historial(self.paciente_seleccionado)
        else: # <--  Muestra mensaje si no hay selección
            messagebox.showwarning("Advertencia", "Selecciona un paciente primero.")


    def registrar_paciente(self):
        nombre = self.entry_nombre.get().strip()
        rut = self.entry_rut.get().strip()  # Obtener el RUT
        edad = self.entry_edad.get().strip()

        try:
            paciente = self.gestor.registrar_paciente(nombre, rut, edad)  # Pasa el RUT
            messagebox.showinfo("Éxito", f"Paciente registrado: {nombre}, RUT: {rut}, Edad: {edad}")
            self.actualizar_lista_pacientes()
            self.limpiar_campos()
        except ValueError as e:
            messagebox.showerror("Error", str(e))  # Muestra el mensaje de error específico

    def actualizar_lista_pacientes(self):
        self.lista_pacientes.delete(*self.lista_pacientes.get_children())
        for paciente in self.gestor.obtener_pacientes():
            self.lista_pacientes.insert("", tk.END, values=(paciente.nombre_completo, paciente.rut, paciente.edad))

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_rut.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)

    def seleccionar_paciente(self, event): # <--  Método para manejar la selección
        seleccionado = self.lista_pacientes.selection()
        if seleccionado:
            item = self.lista_pacientes.item(seleccionado[0])
            nombre_paciente = item['values'][0]
            self.paciente_seleccionado = self.gestor.obtener_paciente(nombre_paciente)
        else:
            self.paciente_seleccionado = None