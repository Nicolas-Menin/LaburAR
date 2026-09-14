from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column,relationship
from backend.app.db.base import Base



class Conversacion(Base):

    __tablename__ = "conversaciones"

    __table_args__ = (
        UniqueConstraint(
            "conexion_laboral_id",
            name="uq_conexion_laboral"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    conexion_laboral_id: Mapped[int] = mapped_column(
        ForeignKey("conexiones_laborales.id"),
        unique=True
    )


    conexion_laboral: Mapped["ConexionLaboral"] = relationship(
        back_populates="conversacion"
    )

    mensajes: Mapped[list["Mensaje"]] = relationship(
        back_populates="conversacion"
    )