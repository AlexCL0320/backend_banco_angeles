# municipio/domain/entities.py

from typing import Optional

class Municipio:
    def __init__(self, id: Optional[int], nombre: str):
        self.id = id
        self.nombre = nombre

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }

    def __eq__(self, other):
        if not isinstance(other, Municipio):
            return NotImplemented
        return self.id == other.id and self.nombre == other.nombre

    def __hash__(self):
        return hash((self.id, self.nombre))

    def __repr__(self):
        return f"Municipio(id={self.id}, nombre='{self.nombre}')"