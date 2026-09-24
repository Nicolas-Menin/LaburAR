from datetime import date
from pydantic import BaseModel, Field,ConfigDict


class ExperienciaLaboralCreate(BaseModel):
    """Contratoa para crear una experiencia laboral del postulante."""

    empresa: str = Field(
        min_length=2,
        max_length=100,
        description="Nombre de la empresa el cual trabajo el postulante."
    )

    puesto: str = Field(
        min_length=2,
        max_length=100,
        description="Nombre del puesto de trabajo que tuvo el postulante."
    )

    fecha_inicio: date = Field(
        description="fecha donde el postulante comenzo a trabajar en la empresas."
    )

    fecha_fin: date | None = Field(
        default=None,
        description="fecha donde el postulante termino de trabajar en la empresa."
    )

    descripcion: str | None = Field(
        default=None,
        description="Descripcion acerca del puesto de trabajo que tenia el postulante."
    )

    area: str = Field(
        min_length=2,
        max_length=100,
        description="Area de trabajo que tuvo el postulante."
    )



class ExperienciaLaboralUpdate(BaseModel):
    """Contrato para actualizar los datos de la experiencia laboral del postulante."""

    empresa: str  | None = Field(
        default=None,
        max_length=100,
        description="Nombre de la empresa el cual trabajo el postulante."
    )

    puesto: str | None = Field(
        default=None,
        max_length=100,
        description="Nombre del puesto de trabajo que tuvo el postulante."
    )

    fecha_inicio: date | None = Field(
        default=None,
        description="fecha donde el postulante comenzo a trabajar en la empresas."
    )

    fecha_fin: date | None = Field(
        default=None,
        description="fecha donde el postulante termino de trabajar en la empresa."
    )

    descripcion: str | None = Field(
        default=None,
        description="Descripcion acerca del puesto de trabajo que tenia el postulante."
    )

    area: str | None = Field(
        default=None,
        max_length=100,
        description="Area de trabajo que tuvo el postulante."
    )


class ExperienciaLaboralPerfil(BaseModel):
    """Contrato que muestra una experiencia laboral del postulante"""
    model_config = ConfigDict(from_attributes=True)

    id: int

    empresa: str

    puesto: str

    fecha_inicio: date

    fecha_fin: date | None = None

    descripcion: str | None = None

    area: str
