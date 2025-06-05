# usuario/domain/entities.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Rol:
    id: int
    nombre: str

@dataclass
class Usuario:
    id: Optional[int]
    nombre_usuario: str
    correo: str
    sexo: str
    rol: Rol
    password: Optional[str] = None # No almacenamos contraseñas aquí, es para el proceso de creación/actualización
    is_active: bool = True
    is_staff: bool = False

    # Aquí podríamos añadir métodos de lógica de negocio pura del Usuario,
    # por ejemplo, si un usuario puede hacer algo específico basado en su rol.
    def es_administrador(self) -> bool:
        return self.is_staff
    
    def actualizar_datos(self, new_data: dict):
        # Lógica para actualizar los datos de la entidad, si es necesario
        # Esto es un ejemplo, la validación principal de los datos de entrada
        # se hará en los serializers/casos de uso.
        if 'nombre_usuario' in new_data:
            self.nombre_usuario = new_data['nombre_usuario']
        if 'correo' in new_data:
            self.correo = new_data['correo']
        if 'sexo' in new_data:
            self.sexo = new_data['sexo']
        if 'rol' in new_data:
            self.rol = new_data['rol'] # Asumimos que Rol ya es una entidad Rol
        if 'is_active' in new_data:
            self.is_active = new_data['is_active']
        if 'is_staff' in new_data:
            self.is_staff = new_data['is_staff']
        # No actualizamos password directamente aquí, se hace con un método específico si es necesario