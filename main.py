import tkinter as tk
from tkinter import ttk, messagebox
from vista.menu_principal import MenuPrincipal
from modelo.paciente import Paciente
from modelo.cita import Cita
from modelo.medicamento import Medicamento
from modelo.historial import HistorialMedico, ArbolHistorial
from modelo.inventario import InventarioMedicamentos
from collections import deque
import csv
import os
from datetime import datetime  # Importamos datetime


class GestorPrincipal:
    def __init__(self):
        self.pacientes = []
        self.citas = deque()
        self.inventario = InventarioMedicamentos()
        self.historiales = {}  # Diccionario de historiales: clave=Paciente, valor=HistorialMedico
        # --- INICIO: Creación explícita de archivos CSV si no existen ---
        if not os.path.exists("datos/pacientes.csv"):
            with open("datos/pacientes.csv", mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["nombre_completo", "rut", "edad"])
                writer.writeheader()  # Crea el archivo con el encabezado
        if not os.path.exists("datos/citas.csv"):
            with open("datos/citas.csv", mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["paciente", "fecha_hora"])
                writer.writeheader() #Crea el archivo con su encabezado
        if not os.path.exists("datos/inventario.csv"):
            with open("datos/inventario.csv", mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["nombre", "cantidad"])
                writer.writeheader() #Crea el archivo con su encabezado
        # --- FIN: Creación explícita de archivos CSV ---
        self.cargar_datos()
        print("Pacientes después de cargar:", self.pacientes)
        self.agregar_datos_ejemplo()
        print("Pacientes después de ejemplos:", self.pacientes)
        print("Inventario después de ejemplos:", self.inventario.obtener_inventario())

    def registrar_paciente(self, nombre, rut, edad):
        print("Intentando registrar paciente:", nombre, rut, edad)
        # Verificar si ya existe un paciente con el mismo RUT
        for paciente in self.pacientes:
            print("  Paciente existente:", paciente)
            if paciente.rut == rut:
                raise ValueError(f"Ya existe un paciente registrado con el RUT {rut}.")

        paciente = Paciente(nombre, rut, edad)
        self.pacientes.append(paciente)
        self.historiales[paciente] = HistorialMedico()  # Crea historial vacío
        self.guardar_pacientes()
        return paciente

    def obtener_pacientes(self):
        return self.pacientes

    def obtener_paciente(self, nombre):
        return next((p for p in self.pacientes if p.nombre_completo == nombre), None)

    def agendar_cita(self, paciente, fecha_hora_str):
        cita = Cita(paciente, fecha_hora_str)
        self.citas.append(cita)
        self.guardar_citas()

    def atender_cita(self):
        if self.citas:
            cita = self.citas.popleft()
            paciente = cita.paciente
            fecha_consulta = datetime.now().strftime("%d-%m-%Y")
            diagnostico = ""
            tratamiento = ""
            examenes = []

            self.agregar_consulta_a_historial(paciente, fecha_consulta, diagnostico, tratamiento, examenes)
            self.guardar_citas()
            return cita
        else:
            return None

    def obtener_citas(self):
        return list(self.citas)

    def agregar_medicamento(self, nombre, cantidad):
        medicamento = Medicamento(nombre, cantidad)
        self.inventario.agregar_medicamento(medicamento)
        self.guardar_inventario()


    def usar_medicamento(self, nombre, cantidad):
        resultado = self.inventario.usar_medicamento(nombre, cantidad)
        self.guardar_inventario()
        return resultado

    def obtener_inventario(self):
        return self.inventario.obtener_inventario()

    def obtener_historial(self, paciente):
        return self.historiales.get(paciente, None)

    def agregar_consulta_a_historial(self, paciente, fecha, diagnostico, tratamiento, examenes=None):
        historial = self.obtener_historial(paciente)
        if historial:
            historial.agregar_consulta(fecha, diagnostico, tratamiento, examenes)
            self.guardar_historiales()
        else:
            print(f"Error: No se encontró el historial para el paciente {paciente.nombre_completo}")

    def mostrar_historial(self, paciente):
        if paciente in self.historiales:
            self.menu.mostrar_historial(paciente)
        else:
            messagebox.showwarning("Advertencia", f"No hay historial para {paciente.nombre_completo}.")

    # --- Métodos de Persistencia (CSV) ---

    def cargar_datos(self):
        self.cargar_pacientes()
        self.cargar_citas()
        self.cargar_inventario()
        self.cargar_historiales()

    def guardar_datos(self):
        self.guardar_pacientes()
        self.guardar_citas()
        self.guardar_inventario()
        self.guardar_historiales()


    def cargar_pacientes(self):
        try:
            with open("datos/pacientes.csv", mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # --- CORRECCIÓN AQUÍ ---
                    nombre_completo = row.get('nombre_completo')
                    if nombre_completo is None:
                        nombre_completo = row.get('nombre')
                    rut = row.get('rut', '')
                    edad = row['edad']
                    # --- FIN DE LA CORRECCIÓN ---
                    self.pacientes.append(Paciente(nombre_completo, rut, edad))


        except FileNotFoundError:
            pass  # El archivo no existe, se creará al guardar

    def guardar_pacientes(self):
        with open("datos/pacientes.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["nombre_completo", "rut", "edad"])  # Modificado
            writer.writeheader()
            for paciente in self.pacientes:
                writer.writerow(paciente.to_dict())

    def cargar_citas(self):
        try:
            with open("datos/citas.csv", mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    paciente = self.obtener_paciente(row['paciente'])  # Busca por nombre_completo
                    if paciente:
                        fecha_hora = row['fecha_hora'] #Ya viene lista
                        self.citas.append(Cita(paciente, fecha_hora)) #Pasamos la fecha y hora
        except FileNotFoundError:
            pass

    def guardar_citas(self):
        with open("datos/citas.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["paciente", "fecha_hora"])  # Incluye fecha_hora
            writer.writeheader()
            for cita in self.citas:
                writer.writerow(cita.to_dict())

    def cargar_inventario(self):
        try:
            with open("datos/inventario.csv", mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.inventario = InventarioMedicamentos.from_list_of_dicts(list(reader))
                print("Inventario cargado desde CSV:", self.inventario.obtener_inventario())
        except FileNotFoundError:
            print("Archivo inventario.csv no encontrado.")
            pass

    def guardar_inventario(self):
        with open("datos/inventario.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["nombre", "cantidad"])
            writer.writeheader()
            writer.writerows(self.inventario.to_list_of_dicts())

    def cargar_historiales(self):
        try:
            for paciente in self.pacientes:
                ruta_archivo = f"datos/historial_{paciente.nombre_completo}.csv" #nombre_completo
                if os.path.exists(ruta_archivo):
                    with open(ruta_archivo, mode='r', newline='', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        historial = HistorialMedico.from_list_of_dicts(list(reader))
                        self.historiales[paciente] = historial
        except Exception as e:
            print(f"Error al cargar historiales: {e}")

    def guardar_historiales(self):
        try:
            for paciente, historial in self.historiales.items():
                ruta_archivo = f"datos/historial_{paciente.nombre_completo}.csv" #nombre_completo
                with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as file:
                    nombres_campos = ["fecha", "diagnostico", "tratamiento", "examenes"]
                    writer = csv.DictWriter(file, fieldnames=nombres_campos)
                    writer.writeheader()
                    for nodo in historial.obtener_historial():
                        examenes_str = ", ".join(nodo.examenes)
                        writer.writerow({
                            'fecha': nodo.fecha,
                            'diagnostico': nodo.diagnostico,
                            'tratamiento': nodo.tratamiento,
                            'examenes': examenes_str
                        })
        except Exception as e:
            print(f"Error al guardar historiales: {e}")

    def agregar_datos_ejemplo(self):
        if not self.pacientes:  # Solo si no hay pacientes cargados
            pacientes_ejemplo = [
                ("Juan Perez Gonzalez", "12.345.678-9", 35),
                ("Maria Rodriguez Soto", "15.678.901-2", 28),
                ("Pedro Ramirez Silva", "10.111.222-3", 51),
                ("Ana Muñoz Ortega", "18.444.555-6", 42),
                ("Carlos Diaz Lopez", "14.777.888-K", 19)
            ]
            for nombre, rut, edad in pacientes_ejemplo:
                self.registrar_paciente(nombre, rut, edad)

        if not self.inventario.obtener_inventario():  # Solo si no hay medicamentos
            print("Agregando medicamentos de ejemplo...")
            medicamentos_ejemplo = [
                ("Paracetamol", 100),
                ("Ibuprofeno", 50),
                ("Viadil", 20),
                ("Tramadol", 30),
                ("Clorfenamina", 80),
                ("Prednisona", 60)
            ]
            for nombre, cantidad in medicamentos_ejemplo:
                self.agregar_medicamento(nombre, cantidad)
            print("Medicamentos de ejemplo agregados.")
        else:
            print("Ya existen medicamentos en el inventario")

    def set_menu(self, menu):
        self.menu = menu
        if self.menu and self.menu.frame_inventario:
            self.menu.frame_inventario.actualizar_lista_medicamentos()
        if self.menu and self.menu.frame_pacientes:
            self.menu.frame_pacientes.actualizar_lista_pacientes()

if __name__ == "__main__":
    root = tk.Tk()
    gestor = GestorPrincipal()
    menu = MenuPrincipal(root, gestor)
    gestor.set_menu(menu)  # Establece la referencia al menú en el gestor
    root.mainloop()