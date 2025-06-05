# donador/domain/repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Donador

class IDonadorRepository(ABC):
    @abstractmethod
    def get_by_id(self, donador_id: int) -> Optional[Donador]:
        """Obtiene un Donador por su ID. Retorna None si no existe."""
        pass

    @abstractmethod
    def get_by_usuario_id(self, usuario_id: int) -> Optional[Donador]:
        """Obtiene un Donador asociado a un Usuario por su ID."""
        pass

    @abstractmethod
    def save(self, donador: Donador) -> Donador:
        """Guarda (crea o actualiza) un Donador. Retorna el Donador guardado."""
        pass

    @abstractmethod
    def delete(self, donador_id: int) -> None:
        """Elimina un Donador por su ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[Donador]:
        """Obtiene todos los Donadores."""
        pass

    @abstractmethod
    def get_donadores_for_map_entities(self) -> List[Donador]:
        """Obtiene una lista de entidades Donador optimizadas para la vista de mapa."""
        pass

    # Métodos específicos para la integración con el ORM de Django en la capa de infraestructura
    # que no son puramente de dominio, pero son útiles para la orquestación.
    @abstractmethod
    def get_all_donadores_for_drf(self):
        """
        Retorna un queryset de Django Model directamente para que Django REST Framework
        pueda aplicar filtros y ordenamientos nativos.
        """
        pass

    @abstractmethod
    def map_domain_entities_to_django_queryset(self, entities: List[Donador]):
        """
        Mapea una lista de entidades de dominio a un queryset de Django Model.
        Esto es un "hack" para permitir que DjangoFilterBackend opere.
        """
        pass

    @abstractmethod
    def get_donador_model_by_id(self, donador_id: int):
        """
        Obtiene el modelo Django Donador por su ID, para uso directo de la API
        (ej. para serialización).
        """
        pass

    @abstractmethod
    def get_donador_model_by_user_id(self, usuario_id: int):
        """
        Obtiene el modelo Django Donador por ID de usuario, para uso directo de la API.
        """
        pass

    @abstractmethod
    def get_donadores_for_map(self):
        """
        Obtiene los modelos Django Donador con las relaciones necesarias para el serializador del mapa.
        """
        pass