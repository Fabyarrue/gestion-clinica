import tkinter as tk
from tkinter import ttk, messagebox


class InventarioFrame(tk.Frame):
    def __init__(self, parent, gestor_principal):
        super().__init__(parent)
        self.gestor = gestor_principal
        self.crear_widgets()

    def crear_widgets(self):
        # Etiquetas y campos de entrada
        tk.Label(self, text="Medicamento:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_medicamento = tk.Entry(self)
        self.entry_medicamento.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(self, text="Cantidad:").grid(row=1, column=0, sticky="e", padx=5, pady=5)  # Se modifico label
        self.entry_cantidad = tk.Entry(self)
        self.entry_cantidad.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Botones separados para Agregar y Usar
        tk.Button(self, text="Agregar", command=self.agregar_medicamento).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self, text="Usar", command=self.usar_medicamento).grid(row=2, column=1, padx=5, pady=5)

        # Tabla (Treeview)
        self.lista_medicamentos = ttk.Treeview(self, columns=("Medicamento", "Cantidad"), show='headings', height=5)
        self.lista_medicamentos.heading("Medicamento", text="Medicamento")
        self.lista_medicamentos.heading("Cantidad", text="Cantidad")
        self.lista_medicamentos.grid(row=3, column=0, columnspan=2, pady=5, sticky="nsew")

        # Configuración de pesos para expansión
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

    def agregar_medicamento(self):
        nombre = self.entry_medicamento.get().strip()
        cantidad_str = self.entry_cantidad.get().strip()

        if not nombre or not cantidad_str:
            messagebox.showwarning("Advertencia", "Por favor, ingresa el nombre y la cantidad del medicamento.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
            self.gestor.agregar_medicamento(nombre, cantidad)
            self.actualizar_lista_medicamentos()
            messagebox.showinfo("Éxito", f"{cantidad} unidades de {nombre} agregadas al inventario.")
            self.limpiar_campos()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def usar_medicamento(self):
        nombre = self.entry_medicamento.get().strip()
        cantidad_str = self.entry_cantidad.get().strip()

        if not nombre or not cantidad_str:
            messagebox.showwarning("Advertencia", "Por favor, ingresa el nombre y la cantidad del medicamento.")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")

            if self.gestor.usar_medicamento(nombre, cantidad):
                self.actualizar_lista_medicamentos()
                messagebox.showinfo("Éxito", f"{cantidad} unidades de {nombre} usadas del inventario.")
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", f"No hay suficiente cantidad de {nombre} en el inventario.")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_lista_medicamentos(self):
        # Limpiar la lista actual
        self.lista_medicamentos.delete(*self.lista_medicamentos.get_children())

        # Volver a poblar la lista
        for medicamento in self.gestor.obtener_inventario():
            self.lista_medicamentos.insert("", tk.END, values=(medicamento.nombre, medicamento.cantidad))

    def limpiar_campos(self):
        self.entry_medicamento.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)