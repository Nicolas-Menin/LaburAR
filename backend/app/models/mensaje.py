from datetime import datetime
from sqlalchemy import ForeignKey, DateTime,Text,Boolean,func
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base

#pylint: disable = E1102



class Mensaje(Base):
    """Clase que representa la tabla mensajes de la base de datos"""

    __tablename__ = "mensajes"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    conversacion_id: Mapped[int] = mapped_column(
        ForeignKey("conversaciones.id"),
        nullable=False,
    )

    remitente_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
    )

    contenido: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    leido: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    fecha_envio: Mapped[datetime] = mapped_column(
        DateTime,
        server_default= func.now(),
        nullable=False
    )
