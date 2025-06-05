# colonia/domain/entities.py

from typing import Optional

class Colonia:
    def __init__(self, id: Optional[int], nombre: str, municipio: int):
        self.id = id
        self.nombre = nombre
        self.municipio = municipio
        # Puedes añadir municipio_nombre si es útil para la entidad,
        # pero para el dominio puro, el ID es suficiente para la relación.
        # self.municipio_nombre: Optional[str] = None 

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "municipio": self.municipio,
        }

    def __eq__(self, other):
        if not isinstance(other, Colonia):
            return NotImplemented
        return self.id == other.id and \
               self.nombre == other.nombre and \
               self.municipio == other.municipio

    def __hash__(self):
        return hash((self.id, self.nombre, self.municipio))

    def __repr__(self):
        return f"Colonia(id={self.id}, nombre='{self.nombre}', municipio={self.municipio})"