from datetime import datetime
from sqlalchemy import ForeignKey, DateTime,func,String,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base

#pylint: disable = E1102



class Postulacion(Base):
    """Clase que representa la tabla postulaciones de la base de datos"""

    __tablename__ = "postulaciones"

    __table_args__ = (
        UniqueConstraint(
            "postulante_id",
            "oferta_id",
            name="uq_postulante_oferta"
        ),
    )



    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    postulante_id: Mapped[int] = mapped_column(
        ForeignKey("postulantes.id"),
        nullable=False
    )

    oferta_id: Mapped[int] = mapped_column(
        ForeignKey("ofertas_laborales.id"),
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    fecha_postulacion: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    postulante: Mapped["Postulante"] = relationship(
        back_populates="postulaciones"
    )