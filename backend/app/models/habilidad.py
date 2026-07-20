from sqlalchemy import String,  ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base



class Habilidad(Base):
    """Clase que representa la tabla habilidades de la base de datos"""

    __tablename__ = "habilidades"

    __table_args__ = (
        UniqueConstraint(
            "postulante_id",
            "nombre",
            name="uq_postulante_habilidad"
        ),
    )


    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    postulante_id: Mapped[int] = mapped_column(
        ForeignKey("postulantes.id"),
        nullable=False,
    )

    nombre: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )