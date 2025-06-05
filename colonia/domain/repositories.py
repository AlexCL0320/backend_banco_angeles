# colonia/domain/repositories.py

from abc import ABC, abstractmethod
from typing import List, Optional
from colonia.domain.entities import Colonia as DomainColonia

class IColoniaRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[DomainColonia]:
        pass

    @abstractmethod
    def get_by_id(self, colonia_id: int) -> Optional[DomainColonia]:
        pass

    @abstractmethod
    def get_by_nombre_and_municipio(self, nombre: str, municipio: int) -> Optional[DomainColonia]:
        pass
    
    @abstractmethod
    def get_by_municipio(self, municipio: int) -> List[DomainColonia]:
        """Obtiene todas las colonias de un municipio específico."""
        pass

    @abstractmethod
    def save(self, colonia: DomainColonia) -> DomainColonia:
        pass

    @abstractmethod
    def delete(self, colonia_id: int) -> None:
        pass