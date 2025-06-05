# direccion/domain/repositories.py

from abc import ABC, abstractmethod
from typing import List, Optional
from direccion.domain.entities import Direccion as DomainDireccion

class IDireccionRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[DomainDireccion]:
        pass

    @abstractmethod
    def get_by_id(self, direccion_id: int) -> Optional[DomainDireccion]:
        pass

    @abstractmethod
    def get_by_full_address(self, calle: str, numInterior: str, numExterior: str, colonia_id: int) -> Optional[DomainDireccion]:
        """Obtiene una dirección por sus detalles completos y colonia."""
        pass
    
    @abstractmethod
    def get_by_colonia(self, colonia_id: int) -> List[DomainDireccion]:
        """Obtiene todas las direcciones en una colonia específica."""
        pass

    @abstractmethod
    def save(self, direccion: DomainDireccion) -> DomainDireccion:
        pass

    @abstractmethod
    def delete(self, direccion_id: int) -> None:
        pass