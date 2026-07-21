from datetime import datetime
from sqlalchemy import ForeignKey, DateTime,func,String,Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base

#pylint: disable = E1102


class Reporte(Base):
    """Clase que representa la tabla reportes en la base de datos """

    __tablename__ = "reportes"

    id: Mapped[int] = mapped_column(

        primary_key=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    usuario_reportado_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    motivo: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
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

    usuario: Mapped["Usuario"] = relationship(
        back_populates= "reportes_realizados",
        foreign_keys= [usuario_id]
    )

    usuario_reportado: Mapped["Usuario"] = relationship(
        back_populates= "reportes_recibidos",
        foreign_keys= [usuario_reportado_id]
    )