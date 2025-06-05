# usuario/domain/repositories.py

from abc import ABC, abstractmethod
from typing import List, Optional
from usuario.domain.entities import Usuario, Rol # Importa las entidades de dominio

class IUsuarioRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Usuario]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[Usuario]:
        pass

    @abstractmethod
    def get_by_correo(self, correo: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def save(self, user: Usuario) -> Usuario:
        # Save podría tanto crear como actualizar, dependiendo de si el ID está presente
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

class IRolRepository(ABC):
    @abstractmethod
    def get_by_id(self, rol_id: int) -> Optional[Rol]:
        pass

    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Rol]:
        pass

    @abstractmethod
    def get_default_rol(self) -> Optional[Rol]:
        pass # Método para obtener el rol por defecto si es necesario