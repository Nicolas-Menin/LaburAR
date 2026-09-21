from datetime import time, datetime
from typing import Literal, List
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl, ConfigDict



class OfertaLaboralCreate(BaseModel):
    """Contrato para crear ofertas laborales"""

    titulo: str = Field(
        min_length=2,
        max_length=100,
        description="Titulo de la oferta laboral"
    )

    descripcion: str = Field(
        min_length=2,
        description="Descripcion de la oferta laboral"
    )

    requisitos: List[str] = Field(
        description="Requisitos de la oferta laboral"
    )

    ubicacion: str = Field(
        min_length=2,
        description="Ubicacion en donde se encuentra la oferta laboral."
    )

    direccion: str = Field(
        min_length=1,
        max_length=100,
        description="Direccion exacta en donde se encuentra la oferta laboral"
    )

    rubro: str = Field(
        min_length=1,
        max_length=50,
        description="Sector donde pertenece la oferta laboral"
    )

    estado: Literal["ACTIVA", "PAUSADA","CERRADA"] = Field(
        description="Estado de la postulacion."
    )

    salario_tipo: Literal["FIJO","RANGO",
                          "A_CONVENIR","NO_INFORMAR"] = Field(
                              description="Tipo de salario que va a tener la oferta laboral."
                          )

    salario_minimo: Decimal | None = Field(
        default=None,
        description="Salario minimo de la oferta laboral"
    )

    salario_maximo: Decimal | None = Field(
        default=None,
        description="Salario maximo de la oferta laboral"
    )

    jornada: Literal["COMPLETA","MEDIA_JORNADA","TEMPORAL","A_CONVENIR"] = Field(
        description="Tipo de jornada que va a tener la oferta laboral"
    )

    turno: Literal["MAÑANA","TARDE",
                   "NOCHE","A_CONVENIR"] = Field(
                       description="Turno que va a tener la oferta laboral."
                   )

    dias_laborales: List[str] | None = Field(
        default=None,
        description="Dias laborales de la oferta laboral"
    )

    hora_inicio: time | None = Field(
        default=None,
        description="Hora de inicio de la jornada laboral."
    )

    hora_fin: time | None = Field(
        default=None,
        description="Hora de finalización de la jornada laboral."
    )


class OfertaLaboralUpdate(BaseModel):
    """Contrato para crear ofertas laborales"""

    titulo: str | None= Field(
        min_length=2,
        max_length=100,
        default= None,
        description="Titulo de la oferta laboral"
    )

    descripcion: str | None = Field(
        min_length=2,
        default= None,
        description="Descripcion de la oferta laboral"
    )

    requisitos: List[str] | None = Field(
        default= None,
        description="Requisitos de la oferta laboral"
    )

    ubicacion: str | None = Field(
        min_length=2,
        default= None,
        description="Ubicacion en donde se encuentra la oferta laboral."
    )

    direccion: str | None = Field(
        min_length=1,
        max_length=100,
        default= None,
        description="Direccion exacta en donde se encuentra la oferta laboral"
    )

    rubro: str | None = Field(
        min_length=1,
        max_length=50,
        default= None,
        description="Sector donde pertenece la oferta laboral"
    )

    estado: Literal["ACTIVA", "PAUSADA","CERRADA"] = Field(
        default= None,
        description="Estado de la postulacion."
    )

    salario_tipo: Literal["FIJO","RANGO",
                          "A_CONVENIR","NO_INFORMAR"] | None = Field(
                              default= None,
                              description="Tipo de salario que va a tener la oferta laboral."
                          )

    salario_minimo: Decimal | None = Field(
        default=None,
        description="Salario minimo de la oferta laboral"
    )

    salario_maximo: Decimal | None = Field(
        default=None,
        description="Salario maximo de la oferta laboral"
    )

    jornada: Literal["COMPLETA","MEDIA_JORNADA","TEMPORAL","A_CONVENIR"] | None= Field(
        default= None,
        description="Tipo de jornada que va a tener la oferta laboral"
    )

    turno: Literal["MAÑANA","TARDE",
                   "NOCHE","A_CONVENIR"] | None = Field(
                       default= None,
                       description="Turno que va a tener la oferta laboral."
                   )

    dias_laborales: List[str] | None = Field(
        default=None,
        description="Dias laborales de la oferta laboral"
    )

    hora_inicio: time | None = Field(
        default=None,
        description="Hora de inicio de la jornada laboral."
    )

    hora_fin: time | None = Field(
        default=None,
        description="Hora de finalización de la jornada laboral."
    )

class OfertaLaboralPerfil(BaseModel):
    """Contrato que muestra el detalle completo de una oferta laboral."""

    titulo: str

    nombre_negocio: str

    foto_empleador: HttpUrl | None = None

    ubicacion: str

    direccion: str

    descripcion: str

    requisitos: List[str] = None

    rubro: str

    salario_tipo: Literal["FIJO", "RANGO", "A_CONVENIR", "NO_INFORMAR"]

    salario_minimo: Decimal | None = None

    salario_maximo: Decimal | None = None

    jornada: Literal["COMPLETA", "MEDIA_JORNADA", "TEMPORAL", "A_CONVENIR"]

    turno: Literal["MAÑANA", "TARDE", "NOCHE", "A_CONVENIR"]

    dias_laborales: List[str] | None = None

    hora_inicio: time | None = None

    hora_fin: time | None = None

    fecha_creacion: datetime

class OfertaLaboralSearch(BaseModel):
    """Contrato para visualizar ofertas laborales del empleador desde su vista previa de perfil"""

    id: int

    empleador_id: int

    titulo: str

    nombre_negocio: str

    ubicacion: str

    direccion: str

    descripcion: str

    foto_perfil_empleador: HttpUrl | None = None


class OfertaLaboralEmpleador(BaseModel):
    """Contrato para visualizar ofertas laborales del empleador desde su perfil"""
    model_config = ConfigDict(from_attributes=True)

    id: int

    titulo: str

    estado: Literal["ACTIVA","PAUSADA","CERRADA"]

    descripcion: str

    fecha_creacion: datetime

class OfertaLaboralFiltro(BaseModel):
    """Contrato para filtrar ofertas laborales"""


    rubro: str | None = None

    jornada: Literal["COMPLETA", "MEDIA_JORNADA", "TEMPORAL", "A_CONVENIR"] | None = None

    turno:  Literal["MAÑANA", "TARDE", "NOCHE", "A_CONVENIR"] | None = None

