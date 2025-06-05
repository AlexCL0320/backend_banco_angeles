# municipio/infrastructure/django_repositories.py

from typing import List, Optional
from django.db import IntegrityError

from municipio.domain.entities import Municipio as DomainMunicipio
from municipio.domain.repositories import IMunicipioRepository
from municipio.models import Municipio as DjangoMunicipio # Importa tu modelo de Django Municipio

class DjangoMunicipioRepository(IMunicipioRepository):
    def _to_domain_municipio(self, django_municipio: DjangoMunicipio) -> DomainMunicipio:
        """Convierte un modelo DjangoMunicipio a una entidad de dominio Municipio."""
        return DomainMunicipio(id=django_municipio.id, nombre=django_municipio.nombre)

    def _to_django_municipio_data(self, domain_municipio: DomainMunicipio) -> dict:
        """Convierte una entidad de dominio Municipio a un diccionario de datos para Django."""
        return {
            'nombre': domain_municipio.nombre,
        }

    def get_all(self) -> List[DomainMunicipio]:
        django_municipios = DjangoMunicipio.objects.all().order_by('nombre')
        return [self._to_domain_municipio(m) for m in django_municipios]

    def get_by_id(self, municipio_id: int) -> Optional[DomainMunicipio]:
        try:
            django_municipio = DjangoMunicipio.objects.get(id=municipio_id)
            return self._to_domain_municipio(django_municipio)
        except DjangoMunicipio.DoesNotExist:
            return None

    def get_by_nombre(self, nombre: str) -> Optional[DomainMunicipio]:
        try:
            django_municipio = DjangoMunicipio.objects.get(nombre__iexact=nombre) # __iexact para búsqueda insensible a mayúsculas/minúsculas
            return self._to_domain_municipio(django_municipio)
        except DjangoMunicipio.DoesNotExist:
            return None

    def save(self, municipio: DomainMunicipio) -> DomainMunicipio:
        try:
            if municipio.id: # Es una actualización
                django_municipio = DjangoMunicipio.objects.get(id=municipio.id)
                django_municipio.nombre = municipio.nombre
                django_municipio.save()
            else: # Es una creación
                django_municipio = DjangoMunicipio.objects.create(nombre=municipio.nombre)
            return self._to_domain_municipio(django_municipio)
        except DjangoMunicipio.DoesNotExist:
            raise ValueError(f"Municipio con ID {municipio.id} no encontrado para actualizar.")
        except IntegrityError as e:
            raise ValueError(f"Error al guardar el municipio: {e}. El nombre del municipio podría estar duplicado.")

    def delete(self, municipio_id: int) -> None:
        try:
            django_municipio = DjangoMunicipio.objects.get(id=municipio_id)
            django_municipio.delete()
        except DjangoMunicipio.DoesNotExist:
            raise ValueError(f"Municipio con ID {municipio_id} no encontrado para eliminar.")