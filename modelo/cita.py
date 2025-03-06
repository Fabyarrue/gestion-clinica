import datetime  # Importante: importar el módulo datetime

class Cita:
    def __init__(self, paciente, fecha_hora):
        self.paciente = paciente
        self.fecha_hora = self.validar_fecha_hora(fecha_hora)

    def __str__(self):
        return f"Cita(paciente={self.paciente.nombre_completo}, fecha={self.fecha_hora.strftime('%Y-%m-%d %H:%M')})"

    def to_dict(self):
        return {
            "paciente": self.paciente.nombre_completo,
            "fecha_hora": self.fecha_hora.strftime('%Y-%m-%d %H:%M')  # Formato ISO
        }

    @classmethod
    def from_dict(cls, data, pacientes):
        paciente = next((p for p in pacientes if p.nombre_completo == data['paciente']), None)
        if paciente:
          fecha_hora = datetime.datetime.strptime(data['fecha_hora'], '%Y-%m-%d %H:%M')
          return cls(paciente, fecha_hora)
        return None

    def validar_fecha_hora(self, fecha_hora_str):
        try:
            # Intentar convertir la cadena a un objeto datetime
            fecha_hora = datetime.datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
            return fecha_hora
        except ValueError:
            raise ValueError("Formato de fecha y hora inválido. Use YYYY-MM-DD HH:MM")