from datetime import datetime, time
from decimal import Decimal
from sqlalchemy import ForeignKey, DateTime,Text,func,String,Numeric, Time,UniqueConstraint,ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import Base

#pylint: disable = E1102



class OfertaLaboral(Base):
    """Clase que representa la tabla oferta laborales de la base de datoss"""


    __tablename__ = "ofertas_laborales"

    __table_args__ = (
        UniqueConstraint(
            "empleador_id",
            "titulo",
            "direccion",
            "estado",
            name="uq_empleador_oferta"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    empleador_id : Mapped[int] = mapped_column(
        ForeignKey("empleadores.id"),
        nullable=False
    )

    titulo: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    requisitos: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False
    )

    ubicacion: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    direccion: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    rubro: Mapped[str] = mapped_column(
        String(50),
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

    salario_tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    salario_minimo: Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        nullable=True
    )

    salario_maximo: Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        nullable=True
    )


    jornada: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    turno: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    dias_laborales: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=True
    )

    hora_inicio: Mapped[time] = mapped_column(
        Time,
        nullable=True
    )

    hora_fin: Mapped[time] = mapped_column(
        Time,
        nullable=True
    )

    empleador: Mapped["Empleador"] = relationship(
        back_populates= "ofertas_laborales"
    )

    conexiones_laborales: Mapped[list["ConexionLaboral"]] = relationship(
        back_populates= "oferta_laboral"
    )
