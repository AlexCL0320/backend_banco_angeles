# coordenada/application/use_cases.py

from typing import List, Optional
from coordenada.domain.entities import Coordenada as DomainCoordenada
from coordenada.domain.repositories import ICoordenadaRepository

class CoordenadaNotFoundException(Exception):
    pass

class CoordenadaAlreadyExistsException(Exception):
    pass

class ObtenerCoordenadasUseCase:
    def __init__(self, coordenada_repo: ICoordenadaRepository):
        self.coordenada_repo = coordenada_repo

    def execute(self) -> List[DomainCoordenada]:
        return self.coordenada_repo.get_all()

class ObtenerCoordenadaPorIdUseCase:
    def __init__(self, coordenada_repo: ICoordenadaRepository):
        self.coordenada_repo = coordenada_repo

    def execute(self, coordenada_id: int) -> DomainCoordenada:
        coordenada = self.coordenada_repo.get_by_id(coordenada_id)
        if not coordenada:
            raise CoordenadaNotFoundException(f"Coordenada con ID {coordenada_id} no encontrada.")
        return coordenada

class CrearCoordenadaUseCase:
    def __init__(self, coordenada_repo: ICoordenadaRepository):
        self.coordenada_repo = coordenada_repo

    def execute(self, latitud: str, longitud: str) -> DomainCoordenada: # Modificado a str
        if self.coordenada_repo.get_by_lat_lon(latitud, longitud):
            raise CoordenadaAlreadyExistsException(f"Ya existe una coordenada en ({latitud}, {longitud}).")
        
        new_coordenada = DomainCoordenada(id=None, latitud=latitud, longitud=longitud)
        return self.coordenada_repo.save(new_coordenada)

class ActualizarCoordenadaUseCase:
    def __init__(self, coordenada_repo: ICoordenadaRepository):
        self.coordenada_repo = coordenada_repo

    def execute(self, coordenada_id: int, latitud: Optional[str] = None, longitud: Optional[str] = None) -> DomainCoordenada: # Modificado a str
        existing_coordenada = self.coordenada_repo.get_by_id(coordenada_id)
        if not existing_coordenada:
            raise CoordenadaNotFoundException(f"Coordenada con ID {coordenada_id} no encontrada para actualizar.")
        
        if latitud is not None:
            existing_coordenada.latitud = latitud
        if longitud is not None:
            existing_coordenada.longitud = longitud

        # Verifica si los nuevos valores ya existen en otra coordenada
        if latitud is not None or longitud is not None:
            duplicate_coordenada = self.coordenada_repo.get_by_lat_lon(existing_coordenada.latitud, existing_coordenada.longitud)
            if duplicate_coordenada and duplicate_coordenada.id != existing_coordenada.id:
                raise CoordenadaAlreadyExistsException(f"Ya existe una coordenada en ({existing_coordenada.latitud}, {existing_coordenada.longitud}).")
            
        return self.coordenada_repo.save(existing_coordenada)

class EliminarCoordenadaUseCase:
    def __init__(self, coordenada_repo: ICoordenadaRepository):
        self.coordenada_repo = coordenada_repo

    def execute(self, coordenada_id: int) -> None:
        existing_coordenada = self.coordenada_repo.get_by_id(coordenada_id)
        if not existing_coordenada:
            raise CoordenadaNotFoundException(f"Coordenada con ID {coordenada_id} no encontrada para eliminar.")
        self.coordenada_repo.delete(coordenada_id)