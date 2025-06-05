# direccion/application/use_cases.py

from typing import List, Optional
from direccion.domain.entities import Direccion as DomainDireccion
from direccion.domain.repositories import IDireccionRepository
from colonia.domain.repositories import IColoniaRepository # Para validar Colonia
from coordenada.domain.repositories import ICoordenadaRepository # Para validar Coordenada


class DireccionNotFoundException(Exception):
    pass

class DireccionAlreadyExistsException(Exception):
    pass

class ColoniaNotValidException(Exception):
    pass

class CoordenadaNotValidException(Exception):
    pass

class ObtenerDireccionesUseCase:
    def __init__(self, direccion_repo: IDireccionRepository):
        self.direccion_repo = direccion_repo

    def execute(self) -> List[DomainDireccion]:
        return self.direccion_repo.get_all()

class ObtenerDireccionPorIdUseCase:
    def __init__(self, direccion_repo: IDireccionRepository):
        self.direccion_repo = direccion_repo

    def execute(self, direccion_id: int) -> DomainDireccion:
        direccion = self.direccion_repo.get_by_id(direccion_id)
        if not direccion:
            raise DireccionNotFoundException(f"Dirección con ID {direccion_id} no encontrada.")
        return direccion

class ObtenerDireccionesPorColoniaUseCase:
    def __init__(self, direccion_repo: IDireccionRepository):
        self.direccion_repo = direccion_repo

    def execute(self, colonia_id: int) -> List[DomainDireccion]:
        return self.direccion_repo.get_by_colonia(colonia_id)

class CrearDireccionUseCase:
    def __init__(self, direccion_repo: IDireccionRepository, 
                 colonia_repo: IColoniaRepository, 
                 coordenada_repo: ICoordenadaRepository):
        self.direccion_repo = direccion_repo
        self.colonia_repo = colonia_repo
        self.coordenada_repo = coordenada_repo

    def execute(self, calle: str, numInterior: str, numExterior: str, colonia_id: int, coordenada_id: int) -> DomainDireccion:
        # Validar que Colonia existe
        colonia = self.colonia_repo.get_by_id(colonia_id)
        if not colonia:
            raise ColoniaNotValidException(f"La Colonia con ID {colonia_id} no es válida.")

        # Validar que Coordenada existe
        coordenada = self.coordenada_repo.get_by_id(coordenada_id)
        if not coordenada:
            raise CoordenadaNotValidException(f"La Coordenada con ID {coordenada_id} no es válida.")

        if self.direccion_repo.get_by_full_address(calle, numInterior, numExterior, colonia_id):
            raise DireccionAlreadyExistsException(f"Ya existe una dirección '{calle} {numExterior} {numInterior}' en esta colonia.")
        
        new_direccion = DomainDireccion(
            id=None, 
            calle=calle, 
            numInterior=numInterior, 
            numExterior=numExterior, 
            colonia_id=colonia_id, 
            coordenada_id=coordenada_id
        )
        return self.direccion_repo.save(new_direccion)

class ActualizarDireccionUseCase:
    def __init__(self, direccion_repo: IDireccionRepository, 
                 colonia_repo: IColoniaRepository, 
                 coordenada_repo: ICoordenadaRepository):
        self.direccion_repo = direccion_repo
        self.colonia_repo = colonia_repo
        self.coordenada_repo = coordenada_repo

    def execute(self, 
                direccion_id: int, 
                calle: Optional[str] = None, 
                numInterior: Optional[str] = None, 
                numExterior: Optional[str] = None, 
                colonia_id: Optional[int] = None, 
                coordenada_id: Optional[int] = None) -> DomainDireccion:
        
        existing_direccion = self.direccion_repo.get_by_id(direccion_id)
        if not existing_direccion:
            raise DireccionNotFoundException(f"Dirección con ID {direccion_id} no encontrada para actualizar.")
        
        # Guardar valores actuales para la validación de duplicados
        current_calle = existing_direccion.calle
        current_numInterior = existing_direccion.numInterior
        current_numExterior = existing_direccion.numExterior
        current_colonia_id = existing_direccion.colonia_id
        current_coordenada_id = existing_direccion.coordenada_id

        # Actualizar los campos si se proporcionan nuevos valores
        if calle is not None:
            existing_direccion.calle = calle
        if numInterior is not None:
            existing_direccion.numInterior = numInterior
        if numExterior is not None:
            existing_direccion.numExterior = numExterior
        
        if colonia_id is not None:
            colonia = self.colonia_repo.get_by_id(colonia_id)
            if not colonia:
                raise ColoniaNotValidException(f"La Colonia con ID {colonia_id} no es válida.")
            existing_direccion.colonia_id = colonia_id
        
        if coordenada_id is not None:
            coordenada = self.coordenada_repo.get_by_id(coordenada_id)
            if not coordenada:
                raise CoordenadaNotValidException(f"La Coordenada con ID {coordenada_id} no es válida.")
            existing_direccion.coordenada_id = coordenada_id
        
        # Verificar duplicados solo si los campos relevantes cambiaron
        if (calle is not None and calle != current_calle) or \
           (numInterior is not None and numInterior != current_numInterior) or \
           (numExterior is not None and numExterior != current_numExterior) or \
           (colonia_id is not None and colonia_id != current_colonia_id):
            
            duplicate_direccion = self.direccion_repo.get_by_full_address(
                existing_direccion.calle, 
                existing_direccion.numInterior, 
                existing_direccion.numExterior, 
                existing_direccion.colonia_id
            )
            if duplicate_direccion and duplicate_direccion.id != existing_direccion.id:
                raise DireccionAlreadyExistsException(
                    f"Ya existe una dirección '{existing_direccion.calle} {existing_direccion.numExterior} {existing_direccion.numInterior}' en esta colonia."
                )
            
        return self.direccion_repo.save(existing_direccion)

class EliminarDireccionUseCase:
    def __init__(self, direccion_repo: IDireccionRepository):
        self.direccion_repo = direccion_repo

    def execute(self, direccion_id: int) -> None:
        existing_direccion = self.direccion_repo.get_by_id(direccion_id)
        if not existing_direccion:
            raise DireccionNotFoundException(f"Dirección con ID {direccion_id} no encontrada para eliminar.")
        self.direccion_repo.delete(direccion_id)