# rol/infrastructure/django_repositories.py

from typing import List, Optional
from django.db import IntegrityError

from rol.domain.entities import Rol as DomainRol
from rol.domain.repositories import IRolRepository
from rol.models import Rol as DjangoRol # Importa tu modelo de Django Rol

class DjangoRolRepository(IRolRepository):
    def _to_domain_rol(self, django_rol: DjangoRol) -> DomainRol:
        """Convierte un modelo DjangoRol a una entidad de dominio Rol."""
        return DomainRol(id=django_rol.id, nombre=django_rol.nombre, permisos=django_rol.permisos)

    def _to_django_rol_data(self, domain_rol: DomainRol) -> dict:
        """Convierte una entidad de dominio Rol a un diccionario de datos para Django."""
        return {
            'nombre': domain_rol.nombre,
            'permisos': domain_rol.permisos,
        }

    def get_by_id(self, rol_id: int) -> Optional[DomainRol]:
        try:
            django_rol = DjangoRol.objects.get(id=rol_id)
            return self._to_domain_rol(django_rol)
        except DjangoRol.DoesNotExist:
            return None

    def get_by_nombre(self, nombre: str) -> Optional[DomainRol]:
        try:
            django_rol = DjangoRol.objects.get(nombre__iexact=nombre) # __iexact para búsqueda insensible a mayúsculas/minúsculas
            return self._to_domain_rol(django_rol)
        except DjangoRol.DoesNotExist:
            return None

    def get_all(self) -> List[DomainRol]:
        django_roles = DjangoRol.objects.all().order_by('id')
        return [self._to_domain_rol(r) for r in django_roles]

    def save(self, rol: DomainRol) -> DomainRol:
        try:
            if rol.id: # Es una actualización
                django_rol = DjangoRol.objects.get(id=rol.id)
                django_rol.nombre = rol.nombre
                django_rol.permisos = rol.permisos
                django_rol.save()
            else: # Es una creación
                django_rol = DjangoRol.objects.create(
                    nombre=rol.nombre,
                    permisos=rol.permisos
                )
            return self._to_domain_rol(django_rol)
        except DjangoRol.DoesNotExist:
            raise ValueError(f"Rol con ID {rol.id} no encontrado para actualizar.")
        except IntegrityError as e:
            raise ValueError(f"Error al guardar el rol: {e}. El nombre del rol podría estar duplicado.")

    def delete(self, rol_id: int) -> None:
        try:
            django_rol = DjangoRol.objects.get(id=rol_id)
            django_rol.delete()
        except DjangoRol.DoesNotExist:
            raise ValueError(f"Rol con ID {rol_id} no encontrado para eliminar.")

    def get_default_rol(self) -> Optional[DomainRol]:
        """
        Retorna el rol por defecto (ej. 'donador').
        Ajusta el ID o el nombre según tu configuración.
        """
        try:
            # Aquí asumimos que el rol 'donador' tiene el ID 2.
            # Si quieres buscarlo por nombre, usa: DjangoRol.objects.get(nombre='donador')
            django_rol = DjangoRol.objects.get(id=2) 
            return self._to_domain_rol(django_rol)
        except DjangoRol.DoesNotExist:
            print("ADVERTENCIA: No se encontró el rol por defecto (ID 2 o 'donador').")
            return None
        except Exception as e:
            print(f"Error inesperado al obtener el rol por defecto: {e}")
            return None