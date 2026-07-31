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
    """Contrato para que el administrado visualice y gestione los reportes."""


    motivo: str

    descripcion: str

    usuario_reportado_id: int

    tipo_usuario: Literal["POSTULANTE", "EMPLEADOR"]

    estado: Literal["REVISADO","PENDIENTE","SANCIONADO"]

    foto_perfil: HttpUrl | None


