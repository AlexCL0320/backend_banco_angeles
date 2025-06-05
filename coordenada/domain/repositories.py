# coordenada/domain/repositories.py

from abc import ABC, abstractmethod
from typing import List, Optional
from coordenada.domain.entities import Coordenada as DomainCoordenada

class ICoordenadaRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[DomainCoordenada]:
        pass

    @abstractmethod
    def get_by_id(self, coordenada_id: int) -> Optional[DomainCoordenada]:
        pass

    @abstractmethod
    def get_by_lat_lon(self, latitud: str, longitud: str) -> Optional[DomainCoordenada]: # Modificado a str
        pass

    @abstractmethod
    def save(self, coordenada: DomainCoordenada) -> DomainCoordenada:
        pass

    @abstractmethod
    def delete(self, coordenada_id: int) -> None:
        pass