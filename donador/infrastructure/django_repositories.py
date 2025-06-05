# donador/infrastructure/django_repositories.py
from django.db import models # Para manejar excepciones como DoesNotExist
from typing import List, Optional

from ..domain.repositories import IDonadorRepository
from ..domain.entities import Donador
from donador.models import Donador as DonadorDjangoModel # Importa tu modelo Django

# Importa los modelos Django de otras aplicaciones si son referenciados
from usuario.models import Usuario as UsuarioDjangoModel
from direccion.models import Direccion as DireccionDjangoModel
from coordenada.models import Coordenada as CoordenadaDjangoModel
from colonia.models import Colonia as ColoniaDjangoModel # Si Colonia se usa en Direccion

# Importa las entidades de dominio de otros módulos para el mapeo
from usuario.domain.entities import Usuario as UsuarioDomainEntity
from direccion.domain.entities import Direccion as DireccionDomainEntity
from coordenada.domain.entities import Coordenada as CoordenadaDomainEntity
from colonia.domain.entities import Colonia as ColoniaDomainEntity

class DjangoDonadorRepository(IDonadorRepository):

    def _map_to_domain_entity(self, donador_model: DonadorDjangoModel) -> Donador:
        """Mapea un objeto de modelo Django a una entidad de dominio Donador."""
        if not donador_model:
            return None

        # Mapea Usuario (asumiendo que UsuarioDjangoModel tiene los campos necesarios)
        usuario_domain_entity = UsuarioDomainEntity(
            id=donador_model.usuario.id,
            nombre=donador_model.usuario.nombre,
            apellido=donador_model.usuario.apellido,
            email=donador_model.usuario.email,
            password=donador_model.usuario.password, # Solo si es absolutamente necesario en la entidad de dominio
            sexo=donador_model.usuario.sexo,
            rol=donador_model.usuario.rol.nombre # Asumiendo que Rol es un objeto relacionado con un campo 'nombre'
        )

        # Mapea Coordenada
        coordenada_domain_entity = CoordenadaDomainEntity(
            id=donador_model.direccion.coordenadas.id,
            latitud=donador_model.direccion.coordenadas.latitud,
            longitud=donador_model.direccion.coordenadas.longitud
        )

        # Mapea Colonia
        colonia_domain_entity = ColoniaDomainEntity(
            id=donador_model.direccion.colonia.id,
            nombre=donador_model.direccion.colonia.nombre,
            codigoPostal=donador_model.direccion.colonia.codigoPostal
            # ... otros campos de Colonia
        )

        # Mapea Direccion
        direccion_domain_entity = DireccionDomainEntity(
            id=donador_model.direccion.id,
            calle=donador_model.direccion.calle,
            numExterior=donador_model.direccion.numExterior,
            numInterior=donador_model.direccion.numInterior,
            coordenadas=coordenada_domain_entity,
            colonia=colonia_domain_entity
        )

        return Donador(
            id=donador_model.id,
            usuario=usuario_domain_entity,
            nombre=donador_model.nombre,
            apellidoP=donador_model.apellidoP,
            apellidoM=donador_model.apellidoM,
            edad=donador_model.edad,
            tipoSangre=donador_model.tipoSangre,
            peso=donador_model.peso,
            telefonoUno=donador_model.telefonoUno,
            telefonoDos=donador_model.telefonoDos,
            estado=donador_model.estado,
            primeraDonacion=donador_model.primeraDonacion,
            ultimaDonacion=donador_model.ultimaDonacion,
            direccion=direccion_domain_entity
        )

    def _map_to_django_model_data(self, donador_entity: Donador) -> dict:
        """
        Mapea una entidad de dominio a un diccionario de datos para el modelo Django.
        Asume que los objetos relacionados (usuario, dirección) ya existen en la BD.
        """
        # Obtener las instancias de los modelos Django relacionados
        # Aquí asumimos que los IDs de las entidades de dominio corresponden a IDs existentes en la DB.
        # En un flujo de creación, estos IDs podrían ser None y necesitarías crear los objetos relacionados.
        usuario_django_model = UsuarioDjangoModel.objects.get(id=donador_entity.usuario.id)
        direccion_django_model = DireccionDjangoModel.objects.get(id=donador_entity.direccion.id)

        return {
            'usuario': usuario_django_model,
            'nombre': donador_entity.nombre,
            'apellidoP': donador_entity.apellidoP,
            'apellidoM': donador_entity.apellidoM,
            'edad': donador_entity.edad,
            'tipoSangre': donador_entity.tipoSangre,
            'peso': donador_entity.peso,
            'telefonoUno': donador_entity.telefonoUno,
            'telefonoDos': donador_entity.telefonoDos,
            'estado': donador_entity.estado,
            'primeraDonacion': donador_entity.primeraDonacion,
            'ultimaDonacion': donador_entity.ultimaDonacion,
            'direccion': direccion_django_model,
        }

    def get_by_id(self, donador_id: int) -> Optional[Donador]:
        try:
            # Usamos select_related para obtener los objetos relacionados en una sola consulta
            donador_model = DonadorDjangoModel.objects.select_related(
                'usuario', 
                'direccion__coordenadas', 
                'direccion__colonia'
            ).get(pk=donador_id)
            return self._map_to_domain_entity(donador_model)
        except DonadorDjangoModel.DoesNotExist:
            # Podrías lanzar una excepción de dominio aquí si la definiste (ej. DonadorNotFoundError)
            # para que la capa de aplicación no dependa de Django.
            raise DonadorDjangoModel.DoesNotExist("Donador no encontrado.") # Re-lanzamos la excepción de Django para el ejemplo.

    def get_by_usuario_id(self, usuario_id: int) -> Optional[Donador]:
        try:
            donador_model = DonadorDjangoModel.objects.select_related(
                'usuario', 
                'direccion__coordenadas', 
                'direccion__colonia'
            ).get(usuario__id=usuario_id)
            return self._map_to_domain_entity(donador_model)
        except DonadorDjangoModel.DoesNotExist:
            raise DonadorDjangoModel.DoesNotExist("Donador no registrado.")

    def save(self, donador: Donador) -> Donador:
        # Aquí, si donador.usuario o donador.direccion son nuevas entidades de dominio
        # y no tienen ID, necesitarías lógica para crearlas o guardarlas primero.
        # Para simplificar, asumimos que ya existen o se crean a través de los validated_data
        # del serializador, que ya los resuelve a objetos de Django Model.

        # Si el donador ya tiene un ID, intentamos actualizarlo
        if donador.id:
            try:
                donador_model = DonadorDjangoModel.objects.get(pk=donador.id)
                # Actualiza los campos del modelo Django con los de la entidad de dominio
                donador_model.usuario = UsuarioDjangoModel.objects.get(id=donador.usuario.id)
                donador_model.nombre = donador.nombre
                donador_model.apellidoP = donador.apellidoP
                donador_model.apellidoM = donador.apellidoM
                donador_model.edad = donador.edad
                donador_model.tipoSangre = donador.tipoSangre
                donador_model.peso = donador.peso
                donador_model.telefonoUno = donador.telefonoUno
                donador_model.telefonoDos = donador.telefonoDos
                donador_model.estado = donador.estado
                donador_model.primeraDonacion = donador.primeraDonacion
                donador_model.ultimaDonacion = donador.ultimaDonacion
                donador_model.direccion = DireccionDjangoModel.objects.get(id=donador.direccion.id)
                donador_model.save()
                return self._map_to_domain_entity(donador_model)
            except DonadorDjangoModel.DoesNotExist:
                # Si no se encuentra, podría significar un intento de actualizar un ID inexistente
                raise ValueError(f"No se pudo actualizar el donador con ID {donador.id}: no encontrado.")
        else:
            # Si el donador no tiene ID, es una nueva creación
            # Necesitamos los objetos Django User y Direccion
            usuario_instance = UsuarioDjangoModel.objects.get(id=donador.usuario.id)
            direccion_instance = DireccionDjangoModel.objects.get(id=donador.direccion.id)

            donador_model = DonadorDjangoModel.objects.create(
                usuario=usuario_instance,
                nombre=donador.nombre,
                apellidoP=donador.apellidoP,
                apellidoM=donador.apellidoM,
                edad=donador.edad,
                tipoSangre=donador.tipoSangre,
                peso=donador.peso,
                telefonoUno=donador.telefonoUno,
                telefonoDos=donador.telefonoDos,
                estado=donador.estado,
                primeraDonacion=donador.primeraDonacion,
                ultimaDonacion=donador.ultimaDonacion,
                direccion=direccion_instance
            )
            donador.id = donador_model.id # Asigna el ID generado a la entidad de dominio
            return self._map_to_domain_entity(donador_model)


    def delete(self, donador_id: int) -> None:
        try:
            donador_model = DonadorDjangoModel.objects.get(pk=donador_id)
            donador_model.delete()
        except DonadorDjangoModel.DoesNotExist:
            # Si no existe, simplemente no hacemos nada o lanzamos una excepción de dominio
            raise DonadorDjangoModel.DoesNotExist(f"Donador con ID {donador_id} no encontrado para eliminar.")

    def get_all(self) -> List[Donador]:
        donadores_models = DonadorDjangoModel.objects.select_related(
            'usuario', 
            'direccion__coordenadas', 
            'direccion__colonia'
        ).all()
        return [self._map_to_domain_entity(model) for model in donadores_models]

    def get_donadores_for_map_entities(self) -> List[Donador]:
        """Obtiene donadores en formato de entidad para el mapa (con relaciones pre-cargadas)."""
        donadores_models = DonadorDjangoModel.objects.select_related(
            'usuario', 
            'direccion__coordenadas', 
            'direccion__colonia'
        ).all() # Puedes añadir filtros específicos para el mapa aquí
        return [self._map_to_domain_entity(model) for model in donadores_models]

    def get_all_donadores_for_drf(self):
        """Método auxiliar para que DRF pueda inferir el queryset inicial."""
        # Este método retorna el queryset de Django directamente para que DRF
        # pueda aplicar sus filtros y ordenamientos de forma nativa.
        return DonadorDjangoModel.objects.all()

    def map_domain_entities_to_django_queryset(self, entities: List[Donador]):
        """
        Mapea una lista de entidades de dominio a un queryset de Django Model.
        Esto es un "hack" para permitir que DjangoFilterBackend opere sobre
        el resultado de un caso de uso que devuelve entidades de dominio.
        """
        ids = [entity.id for entity in entities if entity.id is not None]
        return DonadorDjangoModel.objects.filter(id__in=ids)

    def get_donador_model_by_id(self, donador_id: int):
        """
        Obtiene el modelo Django Donador por su ID, para uso directo de la API
        (ej. para serialización).
        """
        try:
            return DonadorDjangoModel.objects.select_related(
                'usuario', 
                'direccion__coordenadas', 
                'direccion__colonia'
            ).get(pk=donador_id)
        except DonadorDjangoModel.DoesNotExist:
            raise DonadorDjangoModel.DoesNotExist("Donador no encontrado.")

    def get_donador_model_by_user_id(self, usuario_id: int):
        """
        Obtiene el modelo Django Donador por ID de usuario, para uso directo de la API.
        """
        try:
            return DonadorDjangoModel.objects.select_related(
                'usuario', 
                'direccion__coordenadas', 
                'direccion__colonia'
            ).get(usuario__id=usuario_id)
        except DonadorDjangoModel.DoesNotExist:
            raise DonadorDjangoModel.DoesNotExist("Donador no registrado.")

    def get_donadores_for_map(self):
        """
        Obtiene los modelos Django Donador con las relaciones necesarias
        para el serializador del mapa (`DonadorMapaSerializer`).
        """
        return DonadorDjangoModel.objects.select_related('usuario', 'direccion__coordenadas', 'direccion__colonia').all()