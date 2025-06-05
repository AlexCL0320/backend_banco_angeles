# citas/domain/entities.py

from datetime import datetime

class Cita:
    def __init__(self, id: str, fecha_hora: datetime, donador_id: str, receptor_id: str, estado: str):
        if not isinstance(id, str) or not id:
            raise ValueError("El ID debe ser una cadena no vacía.")
        if not isinstance(fecha_hora, datetime):
            raise ValueError("La fecha y hora deben ser un objeto datetime.")
        if not isinstance(donador_id, str) or not donador_id:
            raise ValueError("El ID del donador debe ser una cadena no vacía.")
        if not isinstance(receptor_id, str) or not receptor_id:
            raise ValueError("El ID del receptor debe ser una cadena no vacía.")
        if not isinstance(estado, str) or not estado:
            raise ValueError("El estado debe ser una cadena no vacía.")

        self.id = id
        self.fecha_hora = fecha_hora
        self.donador_id = donador_id
        self.receptor_id = receptor_id
        self.estado = estado

    def actualizar_estado(self, nuevo_estado: str):
        estados_validos = ["pendiente", "aceptada", "rechazada", "completada", "cancelada"]
        if nuevo_estado not in estados_validos:
            raise ValueError(f"Estado '{nuevo_estado}' no válido para una cita.")
        self.estado = nuevo_estado

    def __eq__(self, other):
        if not isinstance(other, Cita):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)