# rol/domain/repositories.py

from abc import ABC, abstractmethod
from typing import List, Optional
from rol.domain.entities import Rol as DomainRol

class IRolRepository(ABC):
    @abstractmethod
    def get_by_id(self, rol_id: int) -> Optional[DomainRol]:
        pass

    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[DomainRol]:
        pass

    @abstractmethod
    def get_all(self) -> List[DomainRol]:
        pass

    @abstractmethod
    def save(self, rol: DomainRol) -> DomainRol:
        pass

    @abstractmethod
    def delete(self, rol_id: int) -> None:
        pass

    @abstractmethod
    def get_default_rol(self) -> Optional[DomainRol]:
        """
        Retorna el rol por defecto si existe (ej. 'donador').
        La implementación concreta decidirá qué es el rol por defecto.
        """
        pass