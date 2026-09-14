from typing import Literal
from datetime import datetime
from pydantic import BaseModel






class ConexionLaboralPostulante(BaseModel):
    """Contrato para visualizar las conexiones laborales del postulante."""

    id: int

    empleador_id: int

    oferta_id: int

    nombre_empleador: str

    nombre_oferta: str

    estado: Literal["PENDIENTE","ACEPTADA","RECHAZADA"]

    fecha_conexion: datetime


class ConexionLaboralEmpleador(BaseModel):
    """Contrato para visualizar las conexiones laborales del empleador."""

    id: int

    postulante_id: int

    oferta_id: int

    nombre_postulante: str

    apellido_postulante: str

    nombre_oferta: str

    estado: Literal["PENDIENTE","ACEPTADA","RECHAZADA"]

    fecha_conexion: datetime