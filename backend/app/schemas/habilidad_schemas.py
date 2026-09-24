from pydantic import BaseModel, Field, ConfigDict


class HabilidadCreate(BaseModel):
    """Conntrato para crear habilidad del postulante"""

    nombre: str = Field(
        min_length=2,
        max_length=50,
        description="Nombre de la habilidad del postulante"
    )


class HabilidadPerfil(BaseModel):
    """Contrato que muestra las habilidades del postulante"""
    model_config = ConfigDict(from_attributes=True)

    id: int

    nombre: str