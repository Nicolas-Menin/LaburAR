from typing import List
from datetime import datetime
from pydantic import BaseModel, Field,ConfigDict


class MensajeCreate(BaseModel):
    """Contrato donde se crea un mensaje."""

    remitente_id: int

    conversacion_id: int

    contenido: str = Field(
        min_length=1,
        description="Contenido del mensaje."
    )


class MensajeChat(BaseModel):
    """Contrato que muestra un mensaje del chat"""
    model_config = ConfigDict(from_attributes=True)


    id: int

    remitente_id: int

    contenido: str

    fecha_envio: datetime

    leido: bool

class MensajeList(BaseModel):
    """Contrato que  muestra la lista de mensajes del chat"""

    mensajes: List[MensajeChat] | None = None


