from typing import Literal
from sqlalchemy.orm import Session
from backend.app.models.reporte import Reporte



class ReporteDAO:
    """Clase encargada del acceso a los datos de reporte"""

    def __init__(self,db: Session):
        self.db = db


    def crear_reporte(self,reporte: Reporte):
        """Metodo para crear reporte"""

        self.db.add(reporte)
        self.db.commit()
        self.db.refresh(reporte)

        return reporte


    def actualizar_reporte(self, reporte: Reporte):
        """Metodo para actualizar el reporte"""
        self.db.commit()
        self.db.refresh(reporte)

        return reporte

    def buscar_reporte_por_id(self,reporte_id: int):
        """Metodo para buscar un reporte mediante id"""

        return (
            self.db.query(Reporte)
            .where(Reporte.id == reporte_id)
            .first()
        )

    def listar_reportes(
        self,
        estado: Literal["REVISADO","PENDIENTE","SANCIONADO"],
        busqueda: str | None = None,
        offset: int = 0,
        limit: int = 10
        ):
        """Metodo para filtrar reportes"""

        query = (
            self.db.query(
                Reporte.id,
                Reporte.motivo,
                Reporte.descripcion,
                Reporte.estado,
                Reporte.fecha_creacion
            )
            .filter(
                Reporte.estado == estado
            )
        )

        if busqueda:
            query = query.filter(
                Reporte.motivo.ilike(f"${busqueda}%")
            )

        return query.offset(offset).limit(limit).all()
