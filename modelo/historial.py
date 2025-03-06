class NodoHistorial:
    def __init__(self, fecha, diagnostico, tratamiento, examenes=None):
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.examenes = examenes if examenes is not None else []
        self.siguiente = None

    def to_dict(self):
        return {
            "fecha": self.fecha,
            "diagnostico": self.diagnostico,
            "tratamiento": self.tratamiento,
            "examenes": self.examenes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['fecha'], data['diagnostico'], data['tratamiento'], data['examenes'])


class HistorialMedico:  # Lista enlazada
    def __init__(self):
        self.cabeza = None

    def agregar_consulta(self, fecha, diagnostico, tratamiento, examenes=None):
        nuevo_nodo = NodoHistorial(fecha, diagnostico, tratamiento, examenes)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_historial(self):
        historial = []
        actual = self.cabeza
        while actual:
            historial.append(actual)
            actual = actual.siguiente
        return historial

    def to_list_of_dicts(self):
        return [nodo.to_dict() for nodo in self.obtener_historial()]

    @classmethod
    def from_list_of_dicts(cls, data):
        historial = cls()
        for nodo_data in data:
            nodo = NodoHistorial.from_dict(nodo_data)
            historial.agregar_consulta(nodo.fecha, nodo.diagnostico, nodo.tratamiento, nodo.examenes)
        return historial


class NodoArbol:
    def __init__(self, data):
        self.data = data
        self.children = []


class ArbolHistorial:  # Arbol de historial
    def __init__(self, paciente):
        self.paciente = paciente  # Nodo raiz
        self.raiz = NodoArbol(f"Historial de {paciente.nombre_completo}") # <-- MODIFICACIÓN AQUÍ

    def agregar_consulta(self, fecha, diagnostico, tratamiento, examenes=None):
        consulta_nodo = NodoArbol(f"Consulta: {fecha}")
        consulta_nodo.children.append(NodoArbol(f"Diagnóstico: {diagnostico}"))
        consulta_nodo.children.append(NodoArbol(f"Tratamiento: {tratamiento}"))
        if examenes:
            examenes_nodo = NodoArbol("Exámenes")
            for examen in examenes:
                examenes_nodo.children.append(NodoArbol(examen))
            consulta_nodo.children.append(examenes_nodo)
        self.raiz.children.append(consulta_nodo)

    def generar_grafo(self, filename="historial"):
        try:
            from graphviz import Digraph
            dot = Digraph(comment=f'Historial Médico de {self.paciente.nombre_completo}') # <-- Y AQUÍ
            dot.node(self.paciente.nombre_completo, self.raiz.data) # <-- Y AQUÍ

            def agregar_nodos(nodo, parent_name):
                for child in nodo.children:
                    child_name = f"{parent_name}_{child.data}"  # Nombres únicos
                    dot.node(child_name, child.data)
                    dot.edge(parent_name, child_name)
                    agregar_nodos(child, child_name)

            agregar_nodos(self.raiz, self.paciente.nombre_completo) # <-- Y AQUÍ
            dot.render(filename, view=False, format='png')  # Guarda en formato png
            return f"{filename}.png"
        except ImportError:
            print("Graphviz no está instalado. No se generará el gráfico.")
            return None
        except Exception as e:
            print(f"Error al generar el grafo: {e}")
            return None