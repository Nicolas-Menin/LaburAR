from pydantic import BaseModel, Field


class HabilidadCreate(BaseModel):
    """Conntrato para crear habilidad del postulante"""

    nombre: str = Field(
        min_length=2,
        max_length=50,
        description="Nombre de la habilidad del postulante"
    )


class HabilidadPerfil(BaseModel):
    """Contrato que muestra las habilidades del postulante"""

    id: int

    nombre: str