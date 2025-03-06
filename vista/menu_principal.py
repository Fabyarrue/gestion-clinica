import tkinter as tk
from tkinter import ttk, messagebox
from vista.pacientes_frame import PacientesFrame  # Importa los Frames
from vista.citas_frame import CitasFrame
from vista.inventario_frame import InventarioFrame
#Los import de modelo ya no son necesarios aquí

class MenuPrincipal:
    def __init__(self, root, gestor_principal):
        self.root = root
        self.root.title("Gestión Clínica")
        self.root.geometry("800x600")
        self.gestor = gestor_principal

        # Crear los frames de cada sección
        self.frame_pacientes = PacientesFrame(self.root, self.gestor)
        self.frame_pacientes.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.frame_citas = CitasFrame(self.root, self.gestor)
        self.frame_citas.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        self.frame_inventario = InventarioFrame(self.root, self.gestor)
        self.frame_inventario.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Configurar el sistema de grid para que se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

    def mostrar_historial(self, paciente):
        #Mostrar el historial del paciente
        historial = self.gestor.obtener_historial(paciente)

        # Crear una nueva ventana para mostrar el historial
        ventana_historial = tk.Toplevel(self.root)
        ventana_historial.title(f"Historial de {paciente.nombre_completo}") # Nombre completo
        ventana_historial.geometry("600x400")

        # Crear un Treeview para mostrar el historial
        tree = ttk.Treeview(ventana_historial, columns=("Fecha", "Diagnóstico", "Tratamiento", "Exámenes"), show="headings")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Diagnóstico", text="Diagnóstico")
        tree.heading("Tratamiento", text="Tratamiento")
        tree.heading("Exámenes", text="Exámenes")
        tree.pack(expand=True, fill='both')

        for nodo in historial.obtener_historial():
            examenes_str = ", ".join(nodo.examenes)  # Convertir lista a string
            tree.insert("", tk.END, values=(nodo.fecha, nodo.diagnostico, nodo.tratamiento, examenes_str))
        # Botón para generar el árbol de historial
        btn_generar_arbol = tk.Button(ventana_historial, text="Generar Árbol de Historial", command=lambda: self.generar_y_mostrar_arbol(paciente))
        btn_generar_arbol.pack(pady=10)
    def generar_y_mostrar_arbol(self, paciente):
        historial = self.gestor.obtener_historial(paciente)
        arbol = ArbolHistorial(paciente)
        for nodo in historial.obtener_historial():
          arbol.agregar_consulta(nodo.fecha, nodo.diagnostico, nodo.tratamiento, nodo.examenes)

        ruta_archivo = arbol.generar_grafo()
        if ruta_archivo:
            try:
                # Intenta abrir la imagen con el visor predeterminado del sistema
                import subprocess
                if os.name == 'nt':  # Windows
                    subprocess.Popen(['start', ruta_archivo], shell=True)
                elif os.name == 'posix':  # macOS y Linux
                    subprocess.Popen(['open', ruta_archivo])  # macOS
                else:
                    messagebox.showinfo("Información", f"Gráfico generado en: {ruta_archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el visor de imágenes: {e}")
        else:
          messagebox.showerror("Error",f"No se pudo generar el arbol de historial de {paciente.nombre_completo}")