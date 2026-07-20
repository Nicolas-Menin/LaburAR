from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base



class Conversacion(Base):

    __tablename__ = "conversaciones"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    conexion_laboral_id: Mapped[int] = mapped_column(
        ForeignKey("conexiones_laborales.id"),
        unique=True
    )

