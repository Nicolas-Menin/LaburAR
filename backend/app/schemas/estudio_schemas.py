from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class EstudioCreate(BaseModel):
    """Contrato que crea un estudio de postulante"""


    titulo: str = Field(
        min_length=2,
        max_length=100,
        description="Titulo de estudio del postulante."
    )

    institucion: str = Field(
        min_length=2,
        max_length=100,
        description="Instituto donde estudio el postulante."
    )

    fecha_inicio: date = Field(
        description="Fecha de inicializacion de estudio."
    )

    fecha_fin: date | None = Field(
        default= None,
        description="Fecha de finalizacion de estudio."
    )

    estado: Literal["EN_CURSO","NO_TERMINADO","FINALIZADO"] = Field(
        description= "Estado de la carrera"
    )

    nivel: Literal["PRIMARIO","SECUNDARIO",
                    "UNIVERSITARIO","TERCIARIO","CURSO"] = Field(
                       description="Nivel de grado de estudio"
                   )

class EstudioUpdate(BaseModel):
    """Contrato para actualizar los datos del estudio"""


    titulo: str | None = Field(
        default=None,
        max_length=100,
        description="Titulo de estudio del postulante."
    )

    institucion: str | None = Field(
        default=None,
        max_length=100,
        description="Instituto donde estudio el postulante."
    )

    fecha_inicio: date | None = Field(
        default=None,
        description="Fecha de inicializacion de estudio."
    )

    fecha_fin: date | None = Field(
        default=None,
        description="Fecha de finalizacion de estudio."
    )

    estado: Literal["EN_CURSO","NO_TERMINADO","FINALIZADO"] | None = Field(
        default=None,
        description= "Estado de la carrera"
    )

    nivel: Literal["PRIMARIO","SECUNDARIO",
                    "UNIVERSITARIO","TERCIARIO","CURSO"] | None = Field(
                        default=None,
                        description="Nivel de grado de estudio"
                    )

class EstudioPerfil(BaseModel):
    """Contrato que muestra un estudio del postulante."""
    model_config = ConfigDict(from_attributes=True)

    id: int

    titulo: str

    institucion: str

    fecha_inicio: date

    fecha_fin: date | None

    estado: Literal["EN_CURSO","NO_TERMINADO","FINALIZADO"]

    nivel: Literal["PRIMARIO","SECUNDARIO",
                    "UNIVERSITARIO","TERCIARIO","CURSO"]


