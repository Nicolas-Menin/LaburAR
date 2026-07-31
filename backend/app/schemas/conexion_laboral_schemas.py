from typing import Literal
from datetime import datetime
from pydantic import BaseModel



class ConexionLaboralPerfil(BaseModel):
    """Contrato que crea una conexión laboral."""

    id: int

    postulante_id: int

    empleador_id: int

    oferta_id: int

    tipo: Literal["CONTACTO_DIRECTO","POSTULACION"]

    estado: Literal["SOLICITUD_ENVIADA","ACEPTADA","RECHAZADA"]

    fecha_conexion: datetime


class ConexionLaboralPostulante(BaseModel):
    """Contrato para visualizar las conexiones laborales del postulante."""

    id: int

    empleador_id: int

    nombre_empleador: str

    nombre_oferta: str

    tipo: Literal["CONTACTO_DIRECTO","POSTULACION"]

    estado: Literal["PENDIENTE","ACEPTADA","RECHAZADA"]

    fecha_conexion: datetime


class ConexionLaboralEmpleador(BaseModel):
    """Contrato para visualizar las conexiones laborales del empleador."""

    id: int

    postulante_id: int

    nombre_postulante: str

    nombre_oferta: str

    tipo: Literal["CONTACTO_DIRECTO","POSTULACION"]

    estado: Literal["SOLICITUD_ENVIADA","ACEPTADA","RECHAZADA"]

    fecha_conexion: datetime