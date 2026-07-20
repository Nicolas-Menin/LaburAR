from datetime import date
from sqlalchemy import String,  ForeignKey, Date,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base


class Estudio(Base):
    """Clase que representa la tabla estudios de la base de datos"""



    __tablename__ = "estudios"

    __table_args__ = (
        UniqueConstraint(
            "postulante_id",
            "titulo",
            "institucion",
            name="uq_postulante_estudio"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    postulante_id: Mapped[int] = mapped_column(
        ForeignKey("postulantes.id"),
        nullable=False,
    )

    titulo: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    institucion: Mapped[str] = mapped_column(
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

    estado: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    nivel: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )