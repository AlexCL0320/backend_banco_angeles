# municipio/domain/repositories.py

from abc import ABC, abstractmethod
from typing import List, Optional
from municipio.domain.entities import Municipio as DomainMunicipio

class IMunicipioRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[DomainMunicipio]:
        pass

    @abstractmethod
    def get_by_id(self, municipio_id: int) -> Optional[DomainMunicipio]:
        pass

    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[DomainMunicipio]:
        pass

    @abstractmethod
    def save(self, municipio: DomainMunicipio) -> DomainMunicipio:
        pass

    @abstractmethod
    def delete(self, municipio_id: int) -> None:
        pass