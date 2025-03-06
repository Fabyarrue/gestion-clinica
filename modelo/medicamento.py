class Medicamento:
    def __init__(self, nombre, cantidad_inicial=0):
        self.nombre = self.validar_nombre(nombre)
        self.cantidad = cantidad_inicial

    def agregar(self, cantidad):
        if cantidad > 0:
            self.cantidad += cantidad
        else:
            raise ValueError("La cantidad a agregar debe ser mayor que cero.")

    def usar(self, cantidad):
        if cantidad > 0:
            if self.cantidad >= cantidad:
                self.cantidad -= cantidad
                return True  # Se usó el medicamento
            else:
                return False  # No hay suficiente cantidad
        else:
            raise ValueError("La cantidad a usar debe ser mayor que cero.")

    def to_dict(self):
        return {"nombre": self.nombre, "cantidad": self.cantidad}

    @classmethod
    def from_dict(cls, data):
        return cls(data['nombre'], int(data['cantidad']))  # Asegurar que cantidad sea int

    def validar_nombre(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del medicamento no puede estar vacío.")
        return nombre.strip()

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"