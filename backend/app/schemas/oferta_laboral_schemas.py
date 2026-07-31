from datetime import time, datetime
from typing import Literal
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl



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

    requisitos: str = Field(
        min_length=1,
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

    dias_laborales: str | None = Field(
        default=None,
        max_length=100,
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

    foto_empleador: HttpUrl | None

    ubicacion: str

    direccion: str

    descripcion: str

    requisitos: str

    rubro: str

    salario_tipo: Literal["FIJO", "RANGO", "A_CONVENIR", "NO_INFORMAR"]

    salario_minimo: Decimal | None

    salario_maximo: Decimal | None

    jornada: Literal["COMPLETA", "MEDIA_JORNADA", "TEMPORAL", "A_CONVENIR"]

    turno: Literal["MAÑANA", "TARDE", "NOCHE", "A_CONVENIR"]

    dias_laborales: str | None

    hora_inicio: time | None

    hora_fin: time | None

    fecha_creacion: datetime

class OfertaLaboralSearch(BaseModel):
    """Contrato para visualizar ofertas laborales del empleador desded su perfil"""

    id: int

    titulo: str

    nombre_negocio: str

    ubicacion: str

    direccion: str

    descripcion: str


class OfertaLaboralEmpleador(BaseModel):
    """Contrato para visualizar ofertas laborales del empleador desded su perfil"""

    id: int

    titulo: str

    estado: Literal["ACTIVA","PAUSADA","CERRADA"]

    descripcion: str


