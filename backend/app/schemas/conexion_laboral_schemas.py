from typing import Literal
from datetime import datetime
from pydantic import BaseModel, HttpUrl




class ConexionLaboralCreate(BaseModel):
    """Contrato para crear conexion laboral"""

    oferta_laboral_id: int

    postulante_id: int

class ConexionLaboralPostulante(BaseModel):
    """Contrato para visualizar las conexiones laborales del postulante."""

    id: int

    empleador_id: int

    oferta_id: int

    nombre_empleador: str

    nombre_oferta: str

    estado: Literal["PENDIENTE","ACEPTADA","RECHAZADA"]

    fecha_conexion: datetime

    foto_perfil_empleador: HttpUrl | None = None


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

    foto_perfil_postulante: HttpUrl | None = None

class ConexionLaboralEmpleadorFiltros(BaseModel):
    """Contrato para filtrar las conexiones laborales del empleador"""

    oferta_id: int | None = None

class ConexionLaboralUpdate(BaseModel):
    """Contrato para actualizar la conexion laboral"""

    conexion_laboral_id: int

    estado: Literal["ACEPTADA","RECHAZADA"]