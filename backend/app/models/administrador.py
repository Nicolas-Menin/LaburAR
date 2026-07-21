from sqlalchemy import String,  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base


class Administrador(Base):
    """Clase que representa la tabla administradores de la base de datos"""

    __tablename__ = "administradores"


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

    foto_perfil: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates= "administrador"
    )