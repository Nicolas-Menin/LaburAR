from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base
#pylint: disable = E1102

class Usuario(Base):
    """Clase que representa la tabla usuarios de la base de datos"""

    __tablename__ = "usuarios"


    id: Mapped[int] = mapped_column(
        primary_key=True
        )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
        )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
        )

    rol: Mapped[str] = mapped_column(
        String(20),
        nullable=False
        )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False
        )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
        )

    # RELACIONES ENTRE OBJETOS DE MODELO DE DATOS

    postulante: Mapped["Postulante"] = relationship(
        back_populates= "usuario"
    )

    empleador: Mapped["Empleador"] = relationship(
        back_populates= "usuario"
    )

    administrador: Mapped["Administrador"] = relationship(
        back_populates= "usuario"
    )

    reportes_realizados: Mapped[list["Reporte"]] = relationship(
        back_populates= "usuario",
        foreign_keys="Reporte.usuario_id"
    )

    reportes_recibidos: Mapped[list["Reporte"]] = relationship(
        back_populates= "usuario_reportado",
        foreign_keys="Reporte.usuario_reportado_id"
    )