from datetime import date
from sqlalchemy import String,  ForeignKey, Date, Text,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base



class ExperienciaLaboral(Base):
    """Clase que representa la tabla experiencias laborales de la base de datos"""

    __tablename__ = "experiencias_laborales"

    __table_args__ = (
        UniqueConstraint(
            "postulante_id",
            "empresa",
            "puesto",
            "fecha_inicio",
            name="uq_postulante_experiencia_laboral"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    postulante_id: Mapped[int] = mapped_column(
        ForeignKey("postulantes.id"),
        nullable=False,
    )

    empresa: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    puesto: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    fecha_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    fecha_fin: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    area: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    postulante: Mapped["Postulante"] = relationship(
        back_populates= "experiencias_laborales"
    )