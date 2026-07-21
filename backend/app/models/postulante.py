from sqlalchemy import String,  ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    usuario: Mapped["Usuario"] = relationship(
        back_populates= "postulante"
    )

    habilidades: Mapped[list["Habilidad"]] = relationship(
        back_populates= "postulante"
    )

    estudios: Mapped[list["Estudio"]] = relationship(
        back_populates= "postulante"
    )

    experiencias_laborales: Mapped[list["ExperienciaLaboral"]] = relationship(
        back_populates= "postulante"
    )

    postulaciones: Mapped[list["Postulacion"]] = relationship(
        back_populates= "postulante"
    )

    conexiones_laborales: Mapped[list["ConexionLaboral"]] = relationship(
        back_populates= "postulante"
    )

