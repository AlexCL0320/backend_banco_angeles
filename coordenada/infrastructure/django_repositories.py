# coordenada/infrastructure/django_repositories.py

from typing import List, Optional
from django.db import IntegrityError

from coordenada.domain.entities import Coordenada as DomainCoordenada
from coordenada.domain.repositories import ICoordenadaRepository
from coordenada.models import Coordenada as DjangoCoordenada # Importa tu modelo de Django Coordenada

class DjangoCoordenadaRepository(ICoordenadaRepository):
    def _to_domain_coordenada(self, django_coordenada: DjangoCoordenada) -> DomainCoordenada:
        """Convierte un modelo DjangoCoordenada a una entidad de dominio Coordenada."""
        return DomainCoordenada(
            id=django_coordenada.id,
            latitud=django_coordenada.latitud, # Usar str directamente
            longitud=django_coordenada.longitud # Usar str directamente
        )

    def _to_django_coordenada_data(self, domain_coordenada: DomainCoordenada) -> dict:
        """Convierte una entidad de dominio Coordenada a un diccionario de datos para Django."""
        return {
            'latitud': domain_coordenada.latitud,
            'longitud': domain_coordenada.longitud,
        }

    def get_all(self) -> List[DomainCoordenada]:
        django_coordenadas = DjangoCoordenada.objects.all().order_by('id')
        return [self._to_domain_coordenada(c) for c in django_coordenadas]

    def get_by_id(self, coordenada_id: int) -> Optional[DomainCoordenada]:
        try:
            django_coordenada = DjangoCoordenada.objects.get(id=coordenada_id)
            return self._to_domain_coordenada(django_coordenada)
        except DjangoCoordenada.DoesNotExist:
            return None

    def get_by_lat_lon(self, latitud: str, longitud: str) -> Optional[DomainCoordenada]: # Modificado a str
        try:
            django_coordenada = DjangoCoordenada.objects.get(
                latitud=latitud, 
                longitud=longitud
            )
            return self._to_domain_coordenada(django_coordenada)
        except DjangoCoordenada.DoesNotExist:
            return None

    def save(self, coordenada: DomainCoordenada) -> DomainCoordenada:
        try:
            if coordenada.id: # Es una actualización
                django_coordenada = DjangoCoordenada.objects.get(id=coordenada.id)
                django_coordenada.latitud = coordenada.latitud
                django_coordenada.longitud = coordenada.longitud
                django_coordenada.save()
            else: # Es una creación
                django_coordenada = DjangoCoordenada.objects.create(
                    latitud=coordenada.latitud,
                    longitud=coordenada.longitud
                )
            return self._to_domain_coordenada(django_coordenada)
        except DjangoCoordenada.DoesNotExist:
            raise ValueError(f"Coordenada con ID {coordenada.id} no encontrada para actualizar.")
        except IntegrityError as e:
            # Si decides añadir unique_together en models.py, este error se capturará aquí
            raise ValueError(f"Error al guardar la coordenada: {e}. La latitud/longitud podría estar duplicada.")

    def delete(self, coordenada_id: int) -> None:
        try:
            django_coordenada = DjangoCoordenada.objects.get(id=coordenada_id)
            django_coordenada.delete()
        except DjangoCoordenada.DoesNotExist:
            raise ValueError(f"Coordenada con ID {coordenada_id} no encontrada para eliminar.")