# usuario/infrastructure/django_repositories.py

from typing import List, Optional
from django.db import IntegrityError
from usuario.domain.entities import Usuario as DomainUsuario, Rol as DomainRol
from usuario.domain.repositories import IUsuarioRepository, IRolRepository
from usuario.models import Usuario as DjangoUsuario, Rol as DjangoRol # Importa tus modelos de Django

class DjangoRolRepository(IRolRepository):
    def get_by_id(self, rol_id: int) -> Optional[DomainRol]:
        try:
            django_rol = DjangoRol.objects.get(id=rol_id)
            return DomainRol(id=django_rol.id, nombre=django_rol.nombre)
        except DjangoRol.DoesNotExist:
            return None

    def get_by_nombre(self, nombre: str) -> Optional[DomainRol]:
        try:
            django_rol = DjangoRol.objects.get(nombre=nombre)
            return DomainRol(id=django_rol.id, nombre=django_rol.nombre)
        except DjangoRol.DoesNotExist:
            return None

    def get_default_rol(self) -> Optional[DomainRol]:
        """
        Retorna el rol por defecto.
        Asumimos que el rol con ID 2 es 'donador' (o el que consideres por defecto).
        Es crucial que este ID exista en tu tabla de Roles.
        """
        try:
            # Aquí podrías usar un ID específico, o buscar por nombre si prefieres.
            # Por ejemplo, si siempre quieres que el rol por defecto sea 'donador':
            # django_rol = DjangoRol.objects.get(nombre='donador')
            
            # Usando ID 2 como 'donador' por defecto (ajusta si es diferente en tu DB)
            django_rol = DjangoRol.objects.get(id=2) 
            return DomainRol(id=django_rol.id, nombre=django_rol.nombre)
        except DjangoRol.DoesNotExist:
            # Puedes registrar un error o simplemente retornar None si no se encuentra
            print("ADVERTENCIA: No se encontró el rol por defecto (ID 2 o 'donador'). Asegúrate de que exista en la DB.")
            return None
        except Exception as e:
            print(f"Error inesperado al obtener el rol por defecto: {e}")
            return None

class DjangoUsuarioRepository(IUsuarioRepository):
    def __init__(self, rol_repo: IRolRepository):
        self.rol_repo = rol_repo

    def _to_domain_user(self, django_user: DjangoUsuario) -> DomainUsuario:
        """Convierte un modelo DjangoUsuario a una entidad de dominio Usuario."""
        # Asegúrate de que django_user.rol no sea None antes de acceder a sus atributos
        domain_rol = None
        if django_user.rol:
            domain_rol = DomainRol(id=django_user.rol.id, nombre=django_user.rol.nombre)
        
        return DomainUsuario(
            id=django_user.id,
            nombre_usuario=django_user.nombre_usuario,
            correo=django_user.correo,
            sexo=django_user.sexo,
            rol=domain_rol, # Asegurarse de que el rol es un objeto DomainRol o None
            is_active=django_user.is_active,
            is_staff=django_user.is_staff
        )

    # El método _to_django_user_data ya no es estrictamente necesario si mapeas directamente
    # en el método save, pero si lo conservas, no debería incluir 'rol' directamente.
    def _to_django_user_data(self, domain_user: DomainUsuario) -> dict:
        """Convierte una entidad de dominio Usuario a un diccionario de datos para Django."""
        data = {
            'nombre_usuario': domain_user.nombre_usuario,
            'correo': domain_user.correo,
            'sexo': domain_user.sexo,
            'is_active': domain_user.is_active,
            'is_staff': domain_user.is_staff,
        }
        return data

    def get_all(self) -> List[DomainUsuario]:
        django_users = DjangoUsuario.objects.all()
        return [self._to_domain_user(u) for u in django_users]

    def get_by_id(self, user_id: int) -> Optional[DomainUsuario]:
        try:
            django_user = DjangoUsuario.objects.get(id=user_id)
            return self._to_domain_user(django_user)
        except DjangoUsuario.DoesNotExist:
            return None

    def get_by_correo(self, correo: str) -> Optional[DomainUsuario]:
        try:
            django_user = DjangoUsuario.objects.get(correo=correo)
            return self._to_domain_user(django_user)
        except DjangoUsuario.DoesNotExist:
            return None

    def save(self, user: DomainUsuario) -> DomainUsuario:
        # Obtener el objeto Rol de Django. Esto es CRUCIAL.
        django_rol = None
        if user.rol and user.rol.id:
            try:
                django_rol = DjangoRol.objects.get(id=user.rol.id)
            except DjangoRol.DoesNotExist:
                raise ValueError(f"Rol con ID {user.rol.id} no encontrado en la base de datos.")
        else:
            # Si el usuario de dominio no tiene un rol o un rol.id,
            # esto indica un problema en el caso de uso si no se manejó el rol por defecto.
            # Puedes lanzar un error aquí para ser estricto, o permitir que el modelo Django
            # use su default si es lo que quieres (aunque Clean Arch prefiere control explícito).
            raise ValueError("La entidad de usuario de dominio debe tener un rol válido asignado.")


        if user.id: # Es una actualización
            try:
                django_user = DjangoUsuario.objects.get(id=user.id)
                
                # Actualizar campos
                django_user.nombre_usuario = user.nombre_usuario
                django_user.correo = user.correo
                django_user.sexo = user.sexo
                django_user.is_active = user.is_active
                django_user.is_staff = user.is_staff
                
                # Asignar el objeto Rol de Django
                # Solo actualizar el rol si se ha proporcionado un nuevo rol válido
                if django_rol:
                    django_user.rol = django_rol 

                # SOLO HASHEAR Y ESTABLECER LA CONTRASEÑA SI SE PROPORCIONA UNA NUEVA EN LA ENTIDAD
                if user.password:
                    django_user.set_password(user.password)
                
                django_user.save()
                return self._to_domain_user(django_user)
            except DjangoUsuario.DoesNotExist:
                raise ValueError(f"Usuario con ID {user.id} no encontrado para actualizar.")
            except IntegrityError as e:
                # Captura de errores de unicidad (ej. correo duplicado)
                if 'correo' in str(e).lower(): # Intenta ser específico para el correo
                    raise ValueError("El correo electrónico ya está registrado.")
                raise ValueError(f"Error al actualizar usuario: {e}.")

        else: # Es una creación
            try:
                # Crear la instancia del modelo Django
                django_user = DjangoUsuario(
                    nombre_usuario=user.nombre_usuario,
                    correo=user.correo,
                    sexo=user.sexo,
                    rol=django_rol, # Asignar el objeto Rol de Django
                    is_active=user.is_active,
                    is_staff=user.is_staff
                )
                
                # Establecer y hashear la contraseña si se proporciona
                if user.password:
                    django_user.set_password(user.password)
                else:
                    # Si no se proporciona contraseña en la creación, es un error
                    raise ValueError("La contraseña es requerida para crear un nuevo usuario.")
                
                django_user.save() # Guardar el usuario con la contraseña hasheada y rol correcto
                return self._to_domain_user(django_user)
            except IntegrityError as e:
                # Captura de errores de unicidad
                if 'correo' in str(e).lower():
                    raise ValueError("El correo electrónico ya está registrado.")
                if 'nombre_usuario' in str(e).lower():
                    raise ValueError("El nombre de usuario ya está en uso.")
                raise ValueError(f"Error al crear usuario: {e}.")


    def delete(self, user_id: int) -> None:
        try:
            django_user = DjangoUsuario.objects.get(id=user_id)
            django_user.delete()
        except DjangoUsuario.DoesNotExist:
            raise ValueError(f"Usuario con ID {user_id} no encontrado para eliminar.")