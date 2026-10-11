from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl


class ReporteCreate(BaseModel):
    """Contrato para crear reporte de usuario"""


    motivo: str = Field(
        min_length=1,
        max_length=50,
        description="Motivo el cual se esta reportando"
    )

    descripcion: str = Field(
        min_length=1,
        description="Descripcion del porque se esta reportando"
    )

class ReporteAdministrador(BaseModel):
    """Contrato para que el administrador visualice y gestione los reportes."""

    id: int

    motivo: str

    descripcion: str

    rol_reportante: Literal["POSTULANTE", "EMPLEADOR"]

    usuario_reportante_id: int

    rol_reportado: Literal["POSTULANTE", "EMPLEADOR"]

    usuario_reportado_id: int

    estado: Literal["REVISADO", "PENDIENTE", "SANCIONADO"]

    foto_perfil: HttpUrl | None = None

    fecha_creacion: datetime

class Reporte(BaseModel):
    """Contrato para que el administrado visualice y gestione los reportes."""

    id: int

    motivo: str

    descripcion: str

    tipo_usuario: Literal["POSTULANTE", "EMPLEADOR"]

    estado: Literal["REVISADO","PENDIENTE","SANCIONADO"]

    foto_perfil: HttpUrl | None = None


class EmpleadorReporte(BaseModel):

    nombre_negocio: str

    foto_perfil: HttpUrl | None = None

class PostulanteReporte(BaseModel):

    nombre: str

    apellido: str

    foto_perfil: HttpUrl | None = None

class ReporteUpdate(BaseModel):

    estado:  Literal["REVISADO","SANCIONADO"]