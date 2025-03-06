import tkinter as tk
from tkinter import ttk, messagebox
from modelo.cita import Cita
from tkcalendar import DateEntry
from datetime import datetime

class CitasFrame(tk.Frame):
    def __init__(self, parent, gestor_principal):
        super().__init__(parent)
        self.gestor = gestor_principal
        self.crear_widgets()

    def crear_widgets(self):
        tk.Button(self, text="Agendar Cita", command=self.agendar_cita).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self, text="Atender Cita", command=self.atender_cita).grid(row=0, column=1, padx=5, pady=5)

        self.lista_citas = ttk.Treeview(self, columns=("Paciente", "Fecha y Hora"), show='headings', height=3)
        self.lista_citas.heading("Paciente", text="Paciente")
        self.lista_citas.heading("Fecha y Hora", text="Fecha y Hora")
        self.lista_citas.grid(row=1, column=0, columnspan=2, pady=5, sticky="nsew")

        tk.Button(self, text="Agregar Consulta a Historial", command=self.agregar_consulta_a_historial).grid(row=2, column=0, columnspan=2, pady=5)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def agendar_cita(self):
        paciente = self.gestor.menu.frame_pacientes.paciente_seleccionado

        if not paciente:
            messagebox.showwarning("Advertencia", "Selecciona un paciente en la lista de pacientes.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Agendar Cita")
        dialog.geometry("400x350")

        tk.Label(dialog, text=f"Paciente: {paciente.nombre_completo}").pack(pady=5)

        tk.Label(dialog, text="Selecciona una fecha:").pack()
        self.cal = DateEntry(dialog, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
        self.cal.pack(pady=5)

        tk.Label(dialog, text="Hora (HH:MM):").pack()
        self.hora_var = tk.StringVar(value="10")  # Valor por defecto sin los minutos
        hora_spinbox = ttk.Spinbox(dialog, from_=0, to=23, width=3, format="%02.0f", textvariable=self.hora_var, command=self.validar_hora)
        hora_spinbox.pack(side=tk.LEFT, padx=5)
        tk.Label(dialog, text=":").pack(side=tk.LEFT)
        self.minuto_var = tk.StringVar(value="00")
        minuto_spinbox = ttk.Spinbox(dialog, from_=0, to=59, width=3, format="%02.0f", textvariable=self.minuto_var, command=self.validar_minutos)  # Función de validación separada
        minuto_spinbox.pack(side=tk.LEFT, padx=5)

        def confirmar_fecha_hora():
            fecha = self.cal.get_date()
            try:
                hora = int(self.hora_var.get())
                minuto = int(self.minuto_var.get())
            except ValueError:
                messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM")
                return

            fecha_hora = datetime(fecha.year, fecha.month, fecha.day, hora, minuto)
            fecha_hora_str = fecha_hora.strftime("%Y-%m-%d %H:%M")

            try:
                self.gestor.agendar_cita(paciente, fecha_hora_str)
                self.actualizar_lista_citas()
                messagebox.showinfo("Éxito", f"Cita agendada para {paciente.nombre_completo} a las {fecha_hora_str}")
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        btn_confirmar = tk.Button(dialog, text="Confirmar", command=confirmar_fecha_hora)
        btn_confirmar.pack(pady=10)
        dialog.grab_set()
        dialog.wait_window(dialog)

    def validar_hora(self):
        """Valida y corrige la hora."""
        try:
            hora = int(self.hora_var.get())
            if hora < 0:
                self.hora_var.set("00")
            elif hora > 23:
                self.hora_var.set("23")
            else:
                self.hora_var.set(f"{hora:02}") #Se establece el formato
        except ValueError:
            self.hora_var.set("00") #En caso de error

    def validar_minutos(self):  # <-- Función de validación separada
        """Valida y corrige los minutos."""
        try:
            minuto = int(self.minuto_var.get())
            if minuto < 0:
                self.minuto_var.set("00")
            elif minuto > 59:
                self.minuto_var.set("59")
            else:
                self.minuto_var.set(f"{minuto:02}") #Se establece el formato
        except ValueError:
            self.minuto_var.set("00") #En caso de error


    def atender_cita(self):
        if self.gestor.atender_cita():
            self.actualizar_lista_citas()
            messagebox.showinfo("Éxito", "Cita atendida.")
        else:
            messagebox.showerror("Error", "No hay citas pendientes.")

    def actualizar_lista_citas(self):
        self.lista_citas.delete(*self.lista_citas.get_children())
        for cita in self.gestor.obtener_citas():
            fecha_hora_mostrada = cita.fecha_hora.strftime('%d-%m-%Y %H:%M')
            self.lista_citas.insert("", tk.END, values=(cita.paciente.nombre_completo, fecha_hora_mostrada))

    def agregar_consulta_a_historial(self):
        seleccionado = self.lista_citas.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona una cita primero.")
            return

        item = self.lista_citas.item(seleccionado[0])
        nombre_paciente = item['values'][0]
        paciente = self.gestor.obtener_paciente(nombre_paciente)

        if not paciente:
            messagebox.showerror("Error", "Paciente no encontrado.")
            return

        dialog = tk.Toplevel(self)
        dialog.title(f"Agregar Consulta a Historial de {paciente.nombre_completo}")
        dialog.geometry("400x350")

        tk.Label(dialog, text="Fecha (DD-MM-YYYY):").grid(row=0, column=0, sticky="e")
        entry_fecha = tk.Entry(dialog)
        entry_fecha.grid(row=0, column=1, sticky="ew")

        tk.Label(dialog, text="Diagnóstico:").grid(row=1, column=0, sticky="e")
        entry_diagnostico = tk.Entry(dialog)
        entry_diagnostico.grid(row=1, column=1, sticky="ew")

        tk.Label(dialog, text="Tratamiento:").grid(row=2, column=0, sticky="e")
        entry_tratamiento = tk.Entry(dialog)
        entry_tratamiento.grid(row=2, column=1, sticky="ew")

        tk.Label(dialog, text="Exámenes (separados por comas):").grid(row=3, column=0, sticky="e")
        entry_examenes = tk.Entry(dialog)
        entry_examenes.grid(row=3, column=1, sticky="ew")

        def validar_fecha(fecha):
            try:
                datetime.strptime(fecha, '%d-%m-%Y')
                return True
            except ValueError:
                return False

        # --- AÑADIDO: Función confirmar_consulta y botón ---
        def confirmar_consulta():
            fecha = entry_fecha.get().strip()
            diagnostico = entry_diagnostico.get().strip()
            tratamiento = entry_tratamiento.get().strip()
            examenes = [e.strip() for e in entry_examenes.get().split(",") if e.strip()]

            if not validar_fecha(fecha):
                messagebox.showerror("Error", "Formato de fecha inválido. Use DD-MM-YYYY.")
                return

            self.gestor.agregar_consulta_a_historial(paciente, fecha, diagnostico, tratamiento, examenes)
            messagebox.showinfo("Éxito", "Consulta agregada al historial.")
            dialog.destroy()

        btn_confirmar = tk.Button(dialog, text="Confirmar", command=confirmar_consulta)
        btn_confirmar.pack(pady=10)
        # --- FIN DEL AÑADIDO ---

        dialog.grab_set()
        dialog.wait_window(dialog)