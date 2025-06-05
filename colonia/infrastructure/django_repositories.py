# colonia/infrastructure/django_repositories.py

from typing import List, Optional
from django.db import IntegrityError

from colonia.domain.entities import Colonia as DomainColonia
from colonia.domain.repositories import IColoniaRepository
from colonia.models import Colonia as DjangoColonia # Importa tu modelo de Django Colonia

# También necesitamos el modelo de Municipio para las relaciones
from municipio.models import Municipio as DjangoMunicipio 
from municipio.domain.entities import Municipio as DomainMunicipio
from municipio.domain.repositories import IMunicipioRepository

# Implementación del repositorio de Municipio para ser inyectado
class DjangoMunicipioRepositoryForColonia(IMunicipioRepository):
    def get_by_id(self, municipio: int) -> Optional[DomainMunicipio]:
        try:
            django_municipio = DjangoMunicipio.objects.get(id=municipio)
            return DomainMunicipio(id=django_municipio.id, nombre=django_municipio.nombre)
        except DjangoMunicipio.DoesNotExist:
            return None
    
    # Métodos placeholder para el resto de la interfaz, ya que no se usarán aquí directamente
    def get_all(self) -> List[DomainMunicipio]:
        return []
    def get_by_nombre(self, nombre: str) -> Optional[DomainMunicipio]:
        return None
    def save(self, municipio: DomainMunicipio) -> DomainMunicipio:
        raise NotImplementedError
    def delete(self, municipio: int) -> None:
        raise NotImplementedError


class DjangoColoniaRepository(IColoniaRepository):
    def _to_domain_colonia(self, django_colonia: DjangoColonia) -> DomainColonia:
        """Convierte un modelo DjangoColonia a una entidad de dominio Colonia."""
        return DomainColonia(
            id=django_colonia.id,
            nombre=django_colonia.nombre,
            municipio=django_colonia.municipio # Accede al ID directamente
        )

    def _to_django_colonia_data(self, domain_colonia: DomainColonia) -> dict:
        """Convierte una entidad de dominio Colonia a un diccionario de datos para Django."""
        return {
            'nombre': domain_colonia.nombre,
            'municipio': domain_colonia.municipio,
        }

    def get_all(self) -> List[DomainColonia]:
        django_colonias = DjangoColonia.objects.all().order_by('nombre')
        return [self._to_domain_colonia(c) for c in django_colonias]

    def get_by_id(self, colonia_id: int) -> Optional[DomainColonia]:
        try:
            django_colonia = DjangoColonia.objects.get(id=colonia_id)
            return self._to_domain_colonia(django_colonia)
        except DjangoColonia.DoesNotExist:
            return None

    def get_by_nombre_and_municipio(self, nombre: str, municipio: int) -> Optional[DomainColonia]:
        try:
            django_colonia = DjangoColonia.objects.get(
                nombre__iexact=nombre, # Búsqueda insensible a mayúsculas/minúsculas
                municipio=municipio
            )
            return self._to_domain_colonia(django_colonia)
        except DjangoColonia.DoesNotExist:
            return None
            
    def get_by_municipio(self, municipio: int) -> List[DomainColonia]:
        django_colonias = DjangoColonia.objects.filter(municipio=municipio).order_by('nombre')
        return [self._to_domain_colonia(c) for c in django_colonias]

    def save(self, colonia: DomainColonia) -> DomainColonia:
        try:
            if colonia.id: # Es una actualización
                django_colonia = DjangoColonia.objects.get(id=colonia.id)
                django_colonia.nombre = colonia.nombre
                # Para actualizar la relación, se asigna el ID directamente
                django_colonia.municipio = colonia.municipio 
                django_colonia.save()
            else: # Es una creación
                # Al crear, se asigna el ID del municipio
                django_colonia = DjangoColonia.objects.create(
                    nombre=colonia.nombre,
                    municipio=colonia.municipio
                )
            return self._to_domain_colonia(django_colonia)
        except DjangoColonia.DoesNotExist:
            raise ValueError(f"Colonia con ID {colonia.id} no encontrada para actualizar.")
        except IntegrityError as e:
            raise ValueError(f"Error al guardar la colonia: {e}. El nombre de la colonia en este municipio podría estar duplicado.")
        except Exception as e:
            # Captura otros errores, como si el municipio no existe en la DB
            if "ForeignKey" in str(e): # Esto es un ejemplo, podrías necesitar una verificación más robusta
                 raise ValueError(f"El municipio con ID {colonia.municipio} no existe.")
            raise e

    def delete(self, colonia_id: int) -> None:
        try:
            django_colonia = DjangoColonia.objects.get(id=colonia_id)
            django_colonia.delete()
        except DjangoColonia.DoesNotExist:
            raise ValueError(f"Colonia con ID {colonia_id} no encontrada para eliminar.")