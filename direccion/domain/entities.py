# direccion/domain/entities.py

from typing import Optional

class Direccion:
    def __init__(self, 
                 id: Optional[int], 
                 calle: str, 
                 numInterior: str, 
                 numExterior: str, 
                 colonia_id: int, 
                 coordenada_id: int):
        self.id = id
        self.calle = calle
        self.numInterior = numInterior
        self.numExterior = numExterior
        self.colonia_id = colonia_id
        self.coordenada_id = coordenada_id

    def to_dict(self):
        return {
            "id": self.id,
            "calle": self.calle,
            "numInterior": self.numInterior,
            "numExterior": self.numExterior,
            "colonia_id": self.colonia_id,
            "coordenada_id": self.coordenada_id,
        }

    def __eq__(self, other):
        if not isinstance(other, Direccion):
            return NotImplemented
        return self.id == other.id and \
               self.calle == other.calle and \
               self.numInterior == other.numInterior and \
               self.numExterior == other.numExterior and \
               self.colonia_id == other.colonia_id and \
               self.coordenada_id == other.coordenada_id

    def __hash__(self):
        return hash((self.id, self.calle, self.numInterior, self.numExterior, self.colonia_id, self.coordenada_id))

    def __repr__(self):
        return (f"Direccion(id={self.id}, calle='{self.calle}', numInterior='{self.numInterior}', "
                f"numExterior='{self.numExterior}', colonia_id={self.colonia_id}, coordenada_id={self.coordenada_id})")