# donador/domain/entities.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

# Importa entidades de otros dominios si son parte de la entidad Donador
# Asegúrate de que estas también sean entidades puras si se usan aquí
# Por ejemplo, si Usuario es una entidad de dominio en su propia capa
from usuario.domain.entities import Usuario as UsuarioDomainEntity
from direccion.domain.entities import Direccion as DireccionDomainEntity
from coordenada.domain.entities import Coordenada as CoordenadaDomainEntity
from colonia.domain.entities import Colonia as ColoniaDomainEntity


@dataclass
class Donador:
    id: Optional[int] = None
    usuario: UsuarioDomainEntity  # La entidad de Usuario, no el ID de Django
    nombre: str
    apellidoP: str
    apellidoM: Optional[str]
    edad: int
    tipoSangre: str
    peso: float
    telefonoUno: str
    telefonoDos: Optional[str]
    estado: bool
    primeraDonacion: date
    ultimaDonacion: date
    direccion: DireccionDomainEntity # La entidad de Direccion, no el modelo Django

    # Métodos de lógica de negocio intrínseca al donador
    def puede_donar_basado_en_tiempo(self) -> bool:
        """
        Verifica si el donador puede donar basado en el tiempo transcurrido
        desde su última donación.
        """
        dias_desde_ultima_donacion = (date.today() - self.ultimaDonacion).days
        return dias_desde_ultima_donacion >= 90 # Ejemplo: 90 días de espera

    def es_mayor_de_edad(self) -> bool:
        """Verifica si el donador tiene la edad legal para donar."""
        return self.edad >= 18 # Ejemplo: Mayor de 18 años

    # Puedes añadir más validaciones de negocio aquí, aunque algunas validaciones
    # de formato ya se manejan en el serializador o en el caso de uso.
    def validate_donador_data(self):
        if self.edad < 18 or self.edad > 65: # Ejemplo de regla de negocio
            raise ValueError("La edad del donador debe estar entre 18 y 65 años.")
        # Más reglas de negocio aquí

# Podrías definir tus propias excepciones de dominio aquí
class DonadorNotFoundError(Exception):
    pass

class DonadorInvalidDataError(Exception):
    pass