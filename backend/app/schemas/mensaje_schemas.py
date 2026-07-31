from datetime import datetime
from pydantic import BaseModel, Field


class MensajeCreate(BaseModel):
    """Contrato donde se crea un mensaje."""

    contenido: str = Field(
        min_length=1,
        description="Contenido del mensaje."
    )


class MensajeChat(BaseModel):
    """Contrato que muestra un mensaje del chat"""

    id: int

    remitente_id: int

    contenido: str

    fecha_envio: datetime

    leido: bool
