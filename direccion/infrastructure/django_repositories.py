# direccion/infrastructure/django_repositories.py

from typing import List, Optional
from django.db import IntegrityError

from direccion.domain.entities import Direccion as DomainDireccion
from direccion.domain.repositories import IDireccionRepository
from direccion.models import Direccion as DjangoDireccion # Importa tu modelo de Django Direccion

# Importar modelos de las relaciones
from colonia.models import Colonia as DjangoColonia
from coordenada.models import Coordenada as DjangoCoordenada

# Importar interfaces y entidades de dominio de las relaciones
from colonia.domain.repositories import IColoniaRepository
from colonia.domain.entities import Colonia as DomainColonia
from coordenada.domain.repositories import ICoordenadaRepository
from coordenada.domain.entities import Coordenada as DomainCoordenada


# Repositorio simplificado para Colonia para ser usado en la inyección de dependencias
class DjangoColoniaRepositoryForDireccion(IColoniaRepository):
    def get_by_id(self, colonia_id: int) -> Optional[DomainColonia]:
        try:
            django_colonia = DjangoColonia.objects.get(id=colonia_id)
            return DomainColonia(id=django_colonia.id, nombre=django_colonia.nombre, municipio=django_colonia.municipio)
        except DjangoColonia.DoesNotExist:
            return None
    
    # Métodos placeholder para el resto de la interfaz, ya que no se usarán aquí directamente
    def get_all(self) -> List[DomainColonia]: return []
    def get_by_nombre_and_municipio(self, nombre: str, municipio: int) -> Optional[DomainColonia]: return None
    def get_by_municipio(self, municipio: int) -> List[DomainColonia]: return []
    def save(self, colonia: DomainColonia) -> DomainColonia: raise NotImplementedError
    def delete(self, colonia_id: int) -> None: raise NotImplementedError

# Repositorio simplificado para Coordenada para ser usado en la inyección de dependencias
class DjangoCoordenadaRepositoryForDireccion(ICoordenadaRepository):
    def get_by_id(self, coordenada_id: int) -> Optional[DomainCoordenada]:
        try:
            django_coordenada = DjangoCoordenada.objects.get(id=coordenada_id)
            # Asegúrate de que los campos coincidan con tu models.py de Coordenada
            return DomainCoordenada(id=django_coordenada.id, latitud=django_coordenada.latitud, longitud=django_coordenada.longitud)
        except DjangoCoordenada.DoesNotExist:
            return None
    
    # Métodos placeholder para el resto de la interfaz, ya que no se usarán aquí directamente
    def get_all(self) -> List[DomainCoordenada]: return []
    def get_by_lat_lon(self, latitud: str, longitud: str) -> Optional[DomainCoordenada]: return None
    def save(self, coordenada: DomainCoordenada) -> DomainCoordenada: raise NotImplementedError
    def delete(self, coordenada_id: int) -> None: raise NotImplementedError


class DjangoDireccionRepository(IDireccionRepository):
    def _to_domain_direccion(self, django_direccion: DjangoDireccion) -> DomainDireccion:
        """Convierte un modelo DjangoDireccion a una entidad de dominio Direccion."""
        return DomainDireccion(
            id=django_direccion.id,
            calle=django_direccion.calle,
            numInterior=django_direccion.numInterior,
            numExterior=django_direccion.numExterior,
            colonia_id=django_direccion.colonia_id, # Accede al ID directamente
            coordenada_id=django_direccion.coordenadas_id # Accede al ID directamente, nota "coordenadas_id"
        )

    def _to_django_direccion_data(self, domain_direccion: DomainDireccion) -> dict:
        """Convierte una entidad de dominio Direccion a un diccionario de datos para Django."""
        return {
            'calle': domain_direccion.calle,
            'numInterior': domain_direccion.numInterior,
            'numExterior': domain_direccion.numExterior,
            'colonia_id': domain_direccion.colonia_id,
            'coordenadas_id': domain_direccion.coordenada_id, # Nota "coordenadas_id"
        }

    def get_all(self) -> List[DomainDireccion]:
        django_direcciones = DjangoDireccion.objects.all().order_by('calle')
        return [self._to_domain_direccion(d) for d in django_direcciones]

    def get_by_id(self, direccion_id: int) -> Optional[DomainDireccion]:
        try:
            django_direccion = DjangoDireccion.objects.get(id=direccion_id)
            return self._to_domain_direccion(django_direccion)
        except DjangoDireccion.DoesNotExist:
            return None

    def get_by_full_address(self, calle: str, numInterior: str, numExterior: str, colonia_id: int) -> Optional[DomainDireccion]:
        try:
            django_direccion = DjangoDireccion.objects.get(
                calle__iexact=calle, # Búsqueda insensible a mayúsculas/minúsculas
                numInterior=numInterior,
                numExterior=numExterior,
                colonia_id=colonia_id
            )
            return self._to_domain_direccion(django_direccion)
        except DjangoDireccion.DoesNotExist:
            return None
            
    def get_by_colonia(self, colonia_id: int) -> List[DomainDireccion]:
        django_direcciones = DjangoDireccion.objects.filter(colonia_id=colonia_id).order_by('calle')
        return [self._to_domain_direccion(d) for d in django_direcciones]

    def save(self, direccion: DomainDireccion) -> DomainDireccion:
        try:
            if direccion.id: # Es una actualización
                django_direccion = DjangoDireccion.objects.get(id=direccion.id)
                django_direccion.calle = direccion.calle
                django_direccion.numInterior = direccion.numInterior
                django_direccion.numExterior = direccion.numExterior
                django_direccion.colonia_id = direccion.colonia_id
                django_direccion.coordenadas_id = direccion.coordenada_id # Nota "coordenadas_id"
                django_direccion.save()
            else: # Es una creación
                django_direccion = DjangoDireccion.objects.create(
                    calle=direccion.calle,
                    numInterior=direccion.numInterior,
                    numExterior=direccion.numExterior,
                    colonia_id=direccion.colonia_id,
                    coordenadas_id=direccion.coordenada_id # Nota "coordenadas_id"
                )
            return self._to_domain_direccion(django_direccion)
        except DjangoDireccion.DoesNotExist:
            raise ValueError(f"Dirección con ID {direccion.id} no encontrada para actualizar.")
        except IntegrityError as e:
            # Captura errores de duplicados si hay restricciones UNIQUE a nivel de DB
            raise ValueError(f"Error al guardar la dirección: {e}. Podría haber una dirección duplicada.")
        except Exception as e:
            # Captura otros errores, como si los IDs de las FK no existen
            if "ForeignKey" in str(e): 
                 raise ValueError(f"Una de las referencias (colonia o coordenada) no existe. Detalles: {e}")
            raise e

    def delete(self, direccion_id: int) -> None:
        try:
            django_direccion = DjangoDireccion.objects.get(id=direccion_id)
            django_direccion.delete()
        except DjangoDireccion.DoesNotExist:
            raise ValueError(f"Dirección con ID {direccion_id} no encontrada para eliminar.")