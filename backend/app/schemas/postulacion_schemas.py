from datetime import datetime
from typing import Literal
from pydantic import BaseModel, HttpUrl


class PostulacionCreate(BaseModel):
    """Contrato para crear postulacion"""

    oferta_id: int

    postulante_id: int

    empleador_id: int

    estado: Literal["PENDIENTE", "ACEPTADA", "RECHAZADA"]



class PostulacionPostulante(BaseModel):
    """Contrato para visualizar las postulaciones del postulante"""

    id: int

    oferta_id: int

    empleador_id: int

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

    apellido_postulante: str

    foto_postulante: HttpUrl | None

    estado: Literal["PENDIENTE", "ACEPTADA", "RECHAZADA"]

    fecha_postulacion: datetime

class PostulacionFiltro(BaseModel):
    """Contrato para filtrar postulaciones"""

    busqueda: str | None = None

    oferta_id: int | None = None