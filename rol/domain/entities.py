# rol/domain/entities.py

from typing import List, Optional

class Rol:
    def __init__(self, id: Optional[int], nombre: str, permisos: Optional[List[str]] = None):
        self.id = id
        self.nombre = nombre
        self.permisos = permisos if permisos is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "permisos": self.permisos,
        }

    def __eq__(self, other):
        if not isinstance(other, Rol):
            return NotImplemented
        return self.id == other.id and self.nombre == other.nombre and self.permisos == other.permisos

    def __hash__(self):
        return hash((self.id, self.nombre, tuple(self.permisos)))

    def __repr__(self):
        return f"Rol(id={self.id}, nombre='{self.nombre}', permisos={self.permisos})"