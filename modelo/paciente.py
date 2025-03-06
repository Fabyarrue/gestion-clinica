import re  # Importamos el módulo de expresiones regulares

class Paciente:
    def __init__(self, nombre_completo, rut, edad):
        self.nombre_completo = self.validar_nombre(nombre_completo)
        self.rut = self.validar_rut(rut)  # Validación de RUT
        self.edad = edad

    def __str__(self):
        return f"Paciente(nombre={self.nombre_completo}, rut={self.rut}, edad={self.edad})"

    def to_dict(self):
        return {
            "nombre_completo": self.nombre_completo,
            "rut": self.rut,
            "edad": self.edad
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['nombre_completo'], data['rut'], data['edad'])

    def validar_nombre(self, nombre):
        # Permite letras (mayúsculas y minúsculas), espacios y acentos.
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            raise ValueError("El nombre debe contener solo letras y espacios.")
        return nombre

    def validar_rut(self, rut):
        #Validar rut con expresiones regulares.
        if not re.match(r"^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$", rut):
            raise ValueError("Formato de RUT incorrecto (ej: 12.345.678-9).")
        return rut