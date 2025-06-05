# usuario/application/use_cases.py

from typing import List, Optional
from usuario.domain.entities import Usuario as DomainUsuario, Rol as DomainRol
from usuario.domain.repositories import IUsuarioRepository, IRolRepository

class UsuarioNotFoundException(Exception):
    pass

class EmailAlreadyExistsException(Exception):
    pass

class RolNotFoundException(Exception):
    pass

# --- Obtener Usuarios ---
class ObtenerUsuariosUseCase: # <--- ¡Asegúrate de que el nombre esté exacto!
    def __init__(self, user_repo: IUsuarioRepository):
        self.user_repo = user_repo

    def execute(self) -> List[DomainUsuario]:
        return self.user_repo.get_all()

class ObtenerUsuarioPorIdUseCase:
    def __init__(self, user_repo: IUsuarioRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> DomainUsuario:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UsuarioNotFoundException(f"Usuario con ID {user_id} no encontrado.")
        return user

class ObtenerUsuarioPorCorreoUseCase:
    def __init__(self, user_repo: IUsuarioRepository):
        self.user_repo = user_repo

    def execute(self, correo: str) -> DomainUsuario:
        user = self.user_repo.get_by_correo(correo)
        if not user:
            raise UsuarioNotFoundException(f"Usuario con correo {correo} no encontrado.")
        return user

# --- Crear Usuario ---
class CrearUsuarioUseCase:
    def __init__(self, user_repo: IUsuarioRepository, rol_repo: IRolRepository):
        self.user_repo = user_repo
        self.rol_repo = rol_repo

    def execute(self, nombre_usuario: str, correo: str, sexo: str, password: str, rol_id: Optional[int] = None) -> DomainUsuario:
        if self.user_repo.get_by_correo(correo):
            raise EmailAlreadyExistsException("Ya existe un usuario con este correo.")

        # Manejo de rol por defecto:
        rol_domain = None
        if rol_id is not None: # Si se proporcionó un rol_id explícitamente
            rol_domain = self.rol_repo.get_by_id(rol_id)
            if not rol_domain:
                raise RolNotFoundException(f"Rol con ID {rol_id} no encontrado.")
        else: # Si no se proporcionó rol_id, intenta obtener el por defecto
            rol_domain = self.rol_repo.get_default_rol()
            if not rol_domain:
                # Si no se encuentra un rol por defecto, puedes lanzar una excepción
                # o asignarle un valor predeterminado duro si estás seguro.
                # Considerando tu problema de que siempre sea admin, vamos a forzar una excepción
                # si no hay rol por defecto, para que no caiga en el default=1 del modelo.
                raise RolNotFoundException("No se encontró un rol por defecto y no se proporcionó un rol_id válido.")
        
        # Validar que rol_domain no sea None antes de crear el usuario
        if rol_domain is None:
            raise ValueError("No se pudo determinar el rol para el nuevo usuario.")


        new_user = DomainUsuario(
            id=None,
            nombre_usuario=nombre_usuario,
            correo=correo,
            sexo=sexo,
            password=password,
            rol=rol_domain, # Asignamos el objeto de dominio Rol
            is_active=True,
            is_staff=False
        )
        return self.user_repo.save(new_user)

# --- Actualizar Usuario ---
class ActualizarUsuarioUseCase:
    def __init__(self, user_repo: IUsuarioRepository, rol_repo: IRolRepository):
        self.user_repo = user_repo
        self.rol_repo = rol_repo

    def execute(self, user_id: int, update_data: dict) -> DomainUsuario:
        existing_user = self.user_repo.get_by_id(user_id)
        if not existing_user:
            raise UsuarioNotFoundException(f"Usuario con ID {user_id} no encontrado para actualizar.")

        if 'correo' in update_data and update_data['correo'] != existing_user.correo:
            if self.user_repo.get_by_correo(update_data['correo']):
                raise EmailAlreadyExistsException("El nuevo correo ya está en uso por otro usuario.")
            existing_user.correo = update_data['correo']

        if 'rol_id' in update_data:
            rol_domain = self.rol_repo.get_by_id(update_data['rol_id'])
            if not rol_domain:
                raise RolNotFoundException(f"Rol con ID {update_data['rol_id']} no encontrado.")
            existing_user.rol = rol_domain
            
        # Actualizar otros campos que existen en la entidad DomainUsuario
        for key, value in update_data.items():
            # Excluir 'rol_id' ya que se maneja por separado
            if hasattr(existing_user, key) and key not in ['rol_id']: 
                setattr(existing_user, key, value)
        
        if 'password' in update_data:
            existing_user.password = update_data['password']

        return self.user_repo.save(existing_user)

# --- Eliminar Usuario ---
class EliminarUsuarioUseCase:
    def __init__(self, user_repo: IUsuarioRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> None:
        self.user_repo.delete(user_id)