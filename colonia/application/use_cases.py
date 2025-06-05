# colonia/application/use_cases.py

from typing import List, Optional
from colonia.domain.entities import Colonia as DomainColonia
from colonia.domain.repositories import IColoniaRepository
from municipio.domain.repositories import IMunicipioRepository # Necesitamos el repositorio de municipio para validar

class ColoniaNotFoundException(Exception):
    pass

class ColoniaAlreadyExistsException(Exception):
    pass

class MunicipioNotValidException(Exception):
    pass

class ObtenerColoniasUseCase:
    def __init__(self, colonia_repo: IColoniaRepository):
        self.colonia_repo = colonia_repo

    def execute(self) -> List[DomainColonia]:
        return self.colonia_repo.get_all()

class ObtenerColoniaPorIdUseCase:
    def __init__(self, colonia_repo: IColoniaRepository):
        self.colonia_repo = colonia_repo

    def execute(self, colonia_id: int) -> DomainColonia:
        colonia = self.colonia_repo.get_by_id(colonia_id)
        if not colonia:
            raise ColoniaNotFoundException(f"Colonia con ID {colonia_id} no encontrada.")
        return colonia

class ObtenerColoniasPorMunicipioUseCase:
    def __init__(self, colonia_repo: IColoniaRepository):
        self.colonia_repo = colonia_repo

    def execute(self, municipio: int) -> List[DomainColonia]:
        return self.colonia_repo.get_by_municipio(municipio)


class CrearColoniaUseCase:
    def __init__(self, colonia_repo: IColoniaRepository, municipio_repo: IMunicipioRepository):
        self.colonia_repo = colonia_repo
        self.municipio_repo = municipio_repo

    def execute(self, nombre: str, municipio: int) -> DomainColonia:
        # Validar que el municipio existe
        municipio = self.municipio_repo.get_by_id(municipio)
        if not municipio:
            raise MunicipioNotValidException(f"El Municipio con ID {municipio} no es válido.")

        if self.colonia_repo.get_by_nombre_and_municipio(nombre, municipio):
            raise ColoniaAlreadyExistsException(f"Ya existe una colonia '{nombre}' en el municipio con ID {municipio}.")
        
        new_colonia = DomainColonia(id=None, nombre=nombre, municipio=municipio)
        return self.colonia_repo.save(new_colonia)

class ActualizarColoniaUseCase:
    def __init__(self, colonia_repo: IColoniaRepository, municipio_repo: IMunicipioRepository):
        self.colonia_repo = colonia_repo
        self.municipio_repo = municipio_repo

    def execute(self, colonia_id: int, nombre: Optional[str] = None, municipio: Optional[int] = None) -> DomainColonia:
        existing_colonia = self.colonia_repo.get_by_id(colonia_id)
        if not existing_colonia:
            raise ColoniaNotFoundException(f"Colonia con ID {colonia_id} no encontrada para actualizar.")
        
        current_nombre = existing_colonia.nombre
        current_municipio = existing_colonia.municipio

        # Actualizar los campos si se proporcionan nuevos valores
        if nombre is not None:
            existing_colonia.nombre = nombre
        if municipio is not None:
            # Validar que el nuevo municipio existe
            municipio = self.municipio_repo.get_by_id(municipio)
            if not municipio:
                raise MunicipioNotValidException(f"El Municipio con ID {municipio} no es válido.")
            existing_colonia.municipio = municipio
        
        # Verificar duplicados solo si los campos relevantes cambiaron
        if (nombre is not None and nombre != current_nombre) or \
           (municipio is not None and municipio != current_municipio):
            
            duplicate_colonia = self.colonia_repo.get_by_nombre_and_municipio(
                existing_colonia.nombre, 
                existing_colonia.municipio
            )
            if duplicate_colonia and duplicate_colonia.id != existing_colonia.id:
                raise ColoniaAlreadyExistsException(
                    f"Ya existe una colonia '{existing_colonia.nombre}' en el municipio con ID {existing_colonia.municipio}."
                )
            
        return self.colonia_repo.save(existing_colonia)

class EliminarColoniaUseCase:
    def __init__(self, colonia_repo: IColoniaRepository):
        self.colonia_repo = colonia_repo

    def execute(self, colonia_id: int) -> None:
        existing_colonia = self.colonia_repo.get_by_id(colonia_id)
        if not existing_colonia:
            raise ColoniaNotFoundException(f"Colonia con ID {colonia_id} no encontrada para eliminar.")
        self.colonia_repo.delete(colonia_id)