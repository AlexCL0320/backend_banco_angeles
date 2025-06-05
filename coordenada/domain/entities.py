# coordenada/domain/entities.py

from typing import Optional

class Coordenada:
    def __init__(self, id: Optional[int], latitud: str, longitud: str):
        self.id = id
        self.latitud = latitud
        self.longitud = longitud

    def to_dict(self):
        return {
            "id": self.id,
            "latitud": self.latitud,
            "longitud": self.longitud,
        }

    def __eq__(self, other):
        if not isinstance(other, Coordenada):
            return NotImplemented
        # La comparación de strings es directa
        return self.id == other.id and \
               self.latitud == other.latitud and \
               self.longitud == other.longitud

    def __hash__(self):
        return hash((self.id, self.latitud, self.longitud))

    def __repr__(self):
        return f"Coordenada(id={self.id}, latitud='{self.latitud}', longitud='{self.longitud}')"