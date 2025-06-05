# donador/application/use_cases.py
from ..domain.entities import Donador # Importa tu entidad de dominio
from ..domain.repositories import IDonadorRepository # Importa la interfaz del repositorio
from ..domain.entities import ( # Importa las entidades de otros dominios
    UsuarioDomainEntity, 
    DireccionDomainEntity, 
    CoordenadaDomainEntity, 
    ColoniaDomainEntity
)
from datetime import date # Para usar date.today() en lógica de negocio

# Puedes definir tus propias excepciones de aplicación si son distintas de las de dominio
class DonadorCreationError(Exception):
    pass

class DonadorUpdateError(Exception):
    pass

class DonadorNotFoundError(Exception): # Reutilizar la de dominio si es la misma semántica
    pass

class CrearDonadorUseCase:
    def __init__(self, donador_repository: IDonadorRepository):
        self.donador_repository = donador_repository

    def execute(self, usuario, nombre, apellidoP, apellidoM, edad, tipoSangre, peso, telefonoUno, telefonoDos, estado, primeraDonacion, ultimaDonacion, direccion):
        # Aquí podrías tener validaciones de alto nivel o reglas de negocio que
        # involucren a múltiples atributos o interacciones con otros servicios.

        # Ejemplo: Validar que el usuario asociado exista (si ya no lo hace el serializer)
        # o que la dirección sea válida.
        # En una aplicación real, 'usuario' y 'direccion' llegarían como objetos
        # del modelo Django desde el serializador, y necesitarías convertirlos a entidades de dominio
        # o pasar sus IDs para que el repositorio los resuelva.

        # Para simplificar y asumir que el serializador ya resolvió los objetos Django:
        # Creamos entidades de dominio a partir de los objetos Django que vienen del serializador
        usuario_entity = UsuarioDomainEntity(
            id=usuario.id, # Asumimos que el objeto usuario de Django tiene un ID
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            password=usuario.password,
            sexo=usuario.sexo,
            rol=usuario.rol # Asumimos que el rol es un simple atributo
        )

        coordenada_entity = CoordenadaDomainEntity(
            id=direccion.coordenadas.id,
            latitud=direccion.coordenadas.latitud,
            longitud=direccion.coordenadas.longitud
        )
        colonia_entity = ColoniaDomainEntity(
            id=direccion.colonia.id,
            nombre=direccion.colonia.nombre,
            codigoPostal=direccion.colonia.codigoPostal
        )
        direccion_entity = DireccionDomainEntity(
            id=direccion.id,
            calle=direccion.calle,
            numExterior=direccion.numExterior,
            numInterior=direccion.numInterior,
            coordenadas=coordenada_entity,
            colonia=colonia_entity
        )

        nuevo_donador = Donador(
            usuario=usuario_entity,
            nombre=nombre,
            apellidoP=apellidoP,
            apellidoM=apellidoM,
            edad=edad,
            tipoSangre=tipoSangre,
            peso=peso,
            telefonoUno=telefonoUno,
            telefonoDos=telefonoDos,
            estado=estado,
            primeraDonacion=primeraDonacion,
            ultimaDonacion=ultimaDonacion,
            direccion=direccion_entity
        )

        # Aplicar reglas de negocio del dominio
        # if not nuevo_donador.es_mayor_de_edad():
        #     raise DonadorCreationError("El donador debe ser mayor de edad.")
        # nuevo_donador.validate_donador_data() # Invoca validaciones de la entidad

        return self.donador_repository.save(nuevo_donador)

class ObtenerDonadorPorIdUseCase:
    def __init__(self, donador_repository: IDonadorRepository):
        self.donador_repository = donador_repository

    def execute(self, donador_id: int) -> Donador:
        donador = self.donador_repository.get_by_id(donador_id)
        if not donador:
            raise DonadorNotFoundError(f"Donador con ID {donador_id} no encontrado.")
        return donador

class ListarDonadoresUseCase:
    def __init__(self, donador_repository: IDonadorRepository):
        self.donador_repository = donador_repository

    def execute(self) -> list[Donador]:
        return self.donador_repository.get_all()

class ActualizarDonadorUseCase:
    def __init__(self, donador_repository: IDonadorRepository):
        self.donador_repository = donador_repository

    def execute(self, donador_id: int, **data) -> Donador:
        donador_existente = self.donador_repository.get_by_id(donador_id)
        if not donador_existente:
            raise DonadorNotFoundError(f"Donador con ID {donador_id} no encontrado para actualizar.")

        # Actualiza los atributos de la entidad de dominio.
        # Aquí, si `data` contiene objetos de Django (como `usuario` o `direccion`),
        # deberías mapearlos a entidades de dominio antes de asignarlos,
        # o el repositorio debería manejar la actualización de esos campos complejos.

        for key, value in data.items():
            if key == 'usuario':
                donador_existente.usuario = UsuarioDomainEntity(
                    id=value.id,
                    nombre=value.nombre,
                    apellido=value.apellido,
                    email=value.email,
                    password=value.password,
                    sexo=value.sexo,
                    rol=value.rol
                )
            elif key == 'direccion':
                coordenada_entity = CoordenadaDomainEntity(
                    id=value.coordenadas.id,
                    latitud=value.coordenadas.latitud,
                    longitud=value.coordenadas.longitud
                )
                colonia_entity = ColoniaDomainEntity(
                    id=value.colonia.id,
                    nombre=value.colonia.nombre,
                    codigoPostal=value.colonia.codigoPostal
                )
                donador_existente.direccion = DireccionDomainEntity(
                    id=value.id,
                    calle=value.calle,
                    numExterior=value.numExterior,
                    numInterior=value.numInterior,
                    coordenadas=coordenada_entity,
                    colonia=colonia_entity
                )
            else:
                setattr(donador_existente, key, value)

        # donador_existente.validate_donador_data() # Re-validar la entidad después de la actualización

        return self.donador_repository.save(donador_existente)

class EliminarDonadorUseCase:
    def __init__(self, donador_repository: IDonadorRepository):
        self.donador_repository = donador_repository

    def execute(self, donador_id: int):
        donador_existente = self.donador_repository.get_by_id(donador_id)
        if not donador_existente:
            raise DonadorNotFoundError(f"Donador con ID {donador_id} no encontrado para eliminar.")
        self.donador_repository.delete(donador_id)

class ObtenerDonadorPorUsuarioIdUseCase:
    def __init__(self, donador_repository: IDonadorRepository):
        self.donador_repository = donador_repository

    def execute(self, usuario_id: int) -> Donador:
        donador = self.donador_repository.get_by_usuario_id(usuario_id)
        if not donador:
            raise DonadorNotFoundError(f"Donador asociado al Usuario con ID {usuario_id} no encontrado.")
        return donador

class ListarDonadoresParaMapaUseCase:
    def __init__(self, donador_repository: IDonadorRepository):
        self.donador_repository = donador_repository

    def execute(self) -> list[Donador]:
        # Este caso de uso podría tener lógica específica para filtrar o preparar
        # los datos para el mapa si es necesario, antes de que el repositorio los obtenga.
        return self.donador_repository.get_donadores_for_map_entities()