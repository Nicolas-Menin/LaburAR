from sqlalchemy import String,  ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base





class Postulante(Base):
    """Clase que representa la tabla postulantes de la base de datos"""

    __tablename__ = "postulantes"


    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
        unique=True
    )

    nombre: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    apellido: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    ubicacion: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    descripcion_personal: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    foto_perfil: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    cv_url: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    disponibilidad: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
