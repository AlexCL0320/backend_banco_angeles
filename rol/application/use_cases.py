# rol/application/use_cases.py

from typing import List, Optional
from rol.domain.entities import Rol as DomainRol
from rol.domain.repositories import IRolRepository

class RolNotFoundException(Exception):
    pass

class RolAlreadyExistsException(Exception):
    pass

class ObtenerRolesUseCase:
    def __init__(self, rol_repo: IRolRepository):
        self.rol_repo = rol_repo

    def execute(self) -> List[DomainRol]:
        return self.rol_repo.get_all()

class ObtenerRolPorIdUseCase:
    def __init__(self, rol_repo: IRolRepository):
        self.rol_repo = rol_repo

    def execute(self, rol_id: int) -> DomainRol:
        rol = self.rol_repo.get_by_id(rol_id)
        if not rol:
            raise RolNotFoundException(f"Rol con ID {rol_id} no encontrado.")
        return rol

class CrearRolUseCase:
    def __init__(self, rol_repo: IRolRepository):
        self.rol_repo = rol_repo

    def execute(self, nombre: str, permisos: Optional[List[str]] = None) -> DomainRol:
        if self.rol_repo.get_by_nombre(nombre):
            raise RolAlreadyExistsException(f"Ya existe un rol con el nombre '{nombre}'.")
        new_rol = DomainRol(id=None, nombre=nombre, permisos=permisos) # ID será asignado por la DB
        return self.rol_repo.save(new_rol)

class ActualizarRolUseCase:
    def __init__(self, rol_repo: IRolRepository):
        self.rol_repo = rol_repo

    def execute(self, rol_id: int, nombre: Optional[str] = None, permisos: Optional[List[str]] = None) -> DomainRol:
        existing_rol = self.rol_repo.get_by_id(rol_id)
        if not existing_rol:
            raise RolNotFoundException(f"Rol con ID {rol_id} no encontrado para actualizar.")
        
        if nombre is not None:
            if self.rol_repo.get_by_nombre(nombre) and existing_rol.nombre != nombre:
                raise RolAlreadyExistsException(f"Ya existe un rol con el nombre '{nombre}'.")
            existing_rol.nombre = nombre
        
        if permisos is not None:
            existing_rol.permisos = permisos
            
        return self.rol_repo.save(existing_rol)

class EliminarRolUseCase:
    def __init__(self, rol_repo: IRolRepository):
        self.rol_repo = rol_repo

    def execute(self, rol_id: int) -> None:
        # Aquí puedes añadir lógica para verificar si el rol está en uso antes de eliminarlo
        # Por ejemplo, verificar si hay usuarios asignados a este rol.
        existing_rol = self.rol_repo.get_by_id(rol_id)
        if not existing_rol:
            raise RolNotFoundException(f"Rol con ID {rol_id} no encontrado para eliminar.")
        self.rol_repo.delete(rol_id)