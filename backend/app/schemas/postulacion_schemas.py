from datetime import datetime
from typing import Literal
from pydantic import BaseModel, HttpUrl


class PostulacionPostulante(BaseModel):
    """Contrato para visualizar las postulaciones del postulante"""

    id: int

    oferta_id: int

    titulo_oferta: str

    nombre_empleador: str

    foto_empleador: HttpUrl | None

    estado: Literal["PENDIENTE", "ACEPTADA", "RECHAZADA"]

    fecha_postulacion: datetime

class PostulacionEmpleador(BaseModel):
    """Contrato para visualizar las postulaciones de las ofertas de trabajo del empleador."""

    id: int

    postulante_id: int

    titulo_oferta: str

    nombre_postulante: str

    foto_postulante: HttpUrl | None

    estado: Literal["PENDIENTE", "ACEPTADA", "RECHAZADA"]

    fecha_postulacion: datetime