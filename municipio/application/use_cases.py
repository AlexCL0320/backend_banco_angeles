# municipio/application/use_cases.py

from typing import List, Optional
from municipio.domain.entities import Municipio as DomainMunicipio
from municipio.domain.repositories import IMunicipioRepository

class MunicipioNotFoundException(Exception):
    pass

class MunicipioAlreadyExistsException(Exception):
    pass

class ObtenerMunicipiosUseCase:
    def __init__(self, municipio_repo: IMunicipioRepository):
        self.municipio_repo = municipio_repo

    def execute(self) -> List[DomainMunicipio]:
        return self.municipio_repo.get_all()

class ObtenerMunicipioPorIdUseCase:
    def __init__(self, municipio_repo: IMunicipioRepository):
        self.municipio_repo = municipio_repo

    def execute(self, municipio_id: int) -> DomainMunicipio:
        municipio = self.municipio_repo.get_by_id(municipio_id)
        if not municipio:
            raise MunicipioNotFoundException(f"Municipio con ID {municipio_id} no encontrado.")
        return municipio

class CrearMunicipioUseCase:
    def __init__(self, municipio_repo: IMunicipioRepository):
        self.municipio_repo = municipio_repo

    def execute(self, nombre: str) -> DomainMunicipio:
        if self.municipio_repo.get_by_nombre(nombre):
            raise MunicipioAlreadyExistsException(f"Ya existe un municipio con el nombre '{nombre}'.")
        new_municipio = DomainMunicipio(id=None, nombre=nombre) # ID será asignado por la DB
        return self.municipio_repo.save(new_municipio)

class ActualizarMunicipioUseCase:
    def __init__(self, municipio_repo: IMunicipioRepository):
        self.municipio_repo = municipio_repo

    def execute(self, municipio_id: int, nombre: Optional[str] = None) -> DomainMunicipio:
        existing_municipio = self.municipio_repo.get_by_id(municipio_id)
        if not existing_municipio:
            raise MunicipioNotFoundException(f"Municipio con ID {municipio_id} no encontrado para actualizar.")
        
        if nombre is not None:
            if self.municipio_repo.get_by_nombre(nombre) and existing_municipio.nombre != nombre:
                raise MunicipioAlreadyExistsException(f"Ya existe un municipio con el nombre '{nombre}'.")
            existing_municipio.nombre = nombre
            
        return self.municipio_repo.save(existing_municipio)

class EliminarMunicipioUseCase:
    def __init__(self, municipio_repo: IMunicipioRepository):
        self.municipio_repo = municipio_repo

    def execute(self, municipio_id: int) -> None:
        existing_municipio = self.municipio_repo.get_by_id(municipio_id)
        if not existing_municipio:
            raise MunicipioNotFoundException(f"Municipio con ID {municipio_id} no encontrado para eliminar.")
        self.municipio_repo.delete(municipio_id)