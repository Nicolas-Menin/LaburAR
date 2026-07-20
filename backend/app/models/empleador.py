from sqlalchemy import String,  ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.db.base import Base





class Empleador(Base):
    """Clase que representa la tabla empleador de la base de datos"""

    __tablename__ = "empleadores"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
        unique=True
    )

    nombre_negocio: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    direccion: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    ubicacion: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    rubro: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    foto_perfil: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )