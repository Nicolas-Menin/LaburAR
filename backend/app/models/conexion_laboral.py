from datetime import datetime
from sqlalchemy import ForeignKey, DateTime,func,String,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column,relationship
from backend.app.db.base import Base

#pylint: disable = E1102


class ConexionLaboral(Base):
    """Clase que representa las conexiones laborales de la base de datos"""

    __tablename__ = "conexiones_laborales"

    __table_args__ = (
        UniqueConstraint(
            "postulante_id",
            "empleador_id",
            "oferta_id",
            "tipo",
            name="uq_postulante_empleador_oferta"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    postulante_id: Mapped[int] = mapped_column(
        ForeignKey("postulantes.id"),
        nullable=False
    )

    empleador_id: Mapped[int] = mapped_column(
        ForeignKey("empleadores.id"),
        nullable=False
    )

    oferta_id: Mapped[int] = mapped_column(
        ForeignKey("ofertas_laborales.id"),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    fecha_conexion: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )


    postulante: Mapped["Postulante"] = relationship(
        back_populates="conexiones_laborales"
    )

    empleador: Mapped["Empleador"] = relationship(
        back_populates="conexiones_laborales"
    )

    oferta_laboral: Mapped["OfertaLaboral"] = relationship(
        back_populates= "conexiones_laborales"
    )

    conversacion: Mapped["Conversacion"]= relationship(
        back_populates= "conexion_laboral"
    )