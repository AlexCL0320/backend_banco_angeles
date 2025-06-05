# citas/domain/repositories.py

from abc import ABC, abstractmethod
from typing import List, Optional
from cita.domain.entities import Cita # Asegúrate de la importación correcta

class CitaRepository(ABC):
    @abstractmethod
    def get_by_id(self, cita_id: str) -> Optional[Cita]:
        pass

    @abstractmethod
    def get_all(self) -> List[Cita]:
        pass

    @abstractmethod
    def get_by_donador_id(self, donador_id: str) -> List[Cita]:
        pass

    @abstractmethod
    def save(self, cita: Cita) -> None:
        pass

    @abstractmethod
    def delete(self, cita_id: str) -> None:
        pass