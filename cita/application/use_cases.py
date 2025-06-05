# citas/application/use_cases.py

from typing import List, Optional
from datetime import datetime
from cita.domain.entities import Cita # Importación correcta
from cita.domain.repositories import CitaRepository # Importación correcta

class CrearCita:
    def __init__(self, repository: CitaRepository):
        self.repository = repository

    def execute(self, id: str, fecha_hora: datetime, donador_id: str, receptor_id: str) -> Cita:
        nueva_cita = Cita(id=id, fecha_hora=fecha_hora, donador_id=donador_id, receptor_id=receptor_id, estado="pendiente")
        self.repository.save(nueva_cita)
        return nueva_cita

class ObtenerCitaPorId:
    def __init__(self, repository: CitaRepository):
        self.repository = repository

    def execute(self, cita_id: str) -> Optional[Cita]:
        return self.repository.get_by_id(cita_id)

class ObtenerTodasLasCitas:
    def __init__(self, repository: CitaRepository):
        self.repository = repository

    def execute(self) -> List[Cita]:
        return self.repository.get_all()

class ObtenerCitasPorDonador:
    def __init__(self, repository: CitaRepository):
        self.repository = repository

    def execute(self, donador_id: str) -> List[Cita]:
        return self.repository.get_by_donador_id(donador_id)

class ActualizarEstadoCita:
    def __init__(self, repository: CitaRepository):
        self.repository = repository

    def execute(self, cita_id: str, nuevo_estado: str) -> Optional[Cita]:
        cita = self.repository.get_by_id(cita_id)
        if cita:
            cita.actualizar_estado(nuevo_estado)
            self.repository.save(cita)
        return cita

class EliminarCita:
    def __init__(self, repository: CitaRepository):
        self.repository = repository

    def execute(self, cita_id: str) -> bool:
        cita = self.repository.get_by_id(cita_id)
        if cita:
            self.repository.delete(cita_id)
            return True
        return False