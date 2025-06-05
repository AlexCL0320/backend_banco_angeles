# citas/infrastructure/django_repo.py

from typing import List, Optional
from cita.domain.entities import Cita # Importación correcta de la entidad
from cita.domain.repositories import CitaRepository # Importación correcta de la interfaz
from cita.models import Cita as CitaModel # Tu modelo de Django

class DjangoCitaRepository(CitaRepository):
    def _map_to_entity(self, django_cita: CitaModel) -> Cita:
        """Mapea un objeto de modelo Django a una entidad Cita."""
        return Cita(
            id=str(django_cita.id),
            fecha_hora=django_cita.fecha_hora,
            donador_id=str(django_cita.donador_id),
            receptor_id=str(django_cita.receptor_id),
            estado=django_cita.estado
        )

    def _map_to_model(self, cita_entity: Cita) -> CitaModel:
        """Mapea una entidad Cita a un objeto de modelo Django."""
        try:
            django_cita = CitaModel.objects.get(id=cita_entity.id)
            django_cita.fecha_hora = cita_entity.fecha_hora
            django_cita.donador_id = cita_entity.donador_id
            django_cita.receptor_id = cita_entity.receptor_id
            django_cita.estado = cita_entity.estado
        except CitaModel.DoesNotExist:
            django_cita = CitaModel(
                id=cita_entity.id,
                fecha_hora=cita_entity.fecha_hora,
                donador_id=cita_entity.donador_id,
                receptor_id=cita_entity.receptor_id,
                estado=cita_entity.estado
            )
        return django_cita

    def get_by_id(self, cita_id: str) -> Optional[Cita]:
        try:
            django_cita = CitaModel.objects.get(id=cita_id)
            return self._map_to_entity(django_cita)
        except CitaModel.DoesNotExist:
            return None

    def get_all(self) -> List[Cita]:
        django_citas = CitaModel.objects.all()
        return [self._map_to_entity(cita) for cita in django_citas]

    def get_by_donador_id(self, donador_id: str) -> List[Cita]:
        django_citas = CitaModel.objects.filter(donador_id=donador_id)
        return [self._map_to_entity(cita) for cita in django_citas]

    def save(self, cita: Cita) -> None:
        django_cita = self._map_to_model(cita)
        django_cita.save()

    def delete(self, cita_id: str) -> None:
        try:
            django_cita = CitaModel.objects.get(id=cita_id)
            django_cita.delete()
        except CitaModel.DoesNotExist:
            pass