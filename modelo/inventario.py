from collections import deque
from .medicamento import Medicamento  # <-- Importante


class InventarioMedicamentos:
    def __init__(self):
        self.medicamentos = deque()  # La pila de medicamentos

    def agregar_medicamento(self, medicamento):
        for med in self.medicamentos:
            if med.nombre == medicamento.nombre:
                med.agregar(medicamento.cantidad)
                return
        self.medicamentos.append(medicamento)

    def usar_medicamento(self, nombre_medicamento, cantidad):
        for med in reversed(self.medicamentos):
            if med.nombre == nombre_medicamento:
                if med.usar(cantidad):
                    return True
                else:
                    return False  # No hay suficiente stock
        return False

    def obtener_inventario(self):
        return list(self.medicamentos)

    def to_list_of_dicts(self):
        return [medicamento.to_dict() for medicamento in self.medicamentos]

    @classmethod
    def from_list_of_dicts(cls, data):
        inventario = cls()
        for medicamento_data in data:
            medicamento = Medicamento.from_dict(medicamento_data)
            inventario.agregar_medicamento(medicamento)
        return inventario