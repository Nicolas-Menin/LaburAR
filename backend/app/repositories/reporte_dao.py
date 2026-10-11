from typing import Literal
from sqlalchemy.orm import Session,aliased
from sqlalchemy import func
from backend.app.models.reporte import Reporte
from backend.app.models.usuario import Usuario
from backend.app.models.postulante import Postulante
from backend.app.models.empleador import Empleador

UsuarioReportante = aliased(Usuario)
UsuarioReportado = aliased(Usuario)

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
                Reporte.id.label("id"),
                Reporte.motivo.label("motivo"),
                Reporte.descripcion.label("descripcion"),
                Usuario.rol.label("tipo_usuario"),
                Reporte.estado.label("estado"),
                UsuarioReportante.rol.label("rol_reportante"),
                Reporte.usuario_id.label("usuario_reportante_id"),
                UsuarioReportado.rol.label("rol_reportado"),
                Reporte.usuario_reportado_id.label("usuario_reportado_id"),
                func.coalesce(
                    Empleador.foto_perfil,
                    Postulante.foto_perfil
                ).label("foto_perfil"),
                Reporte.fecha_creacion.label("fecha_creacion"),
            )
            .join(UsuarioReportante,
                   Reporte.usuario_id == UsuarioReportante.id
                  )
            .join(
                UsuarioReportado,
                Reporte.usuario_reportado_id == UsuarioReportado.id
            )
            .join(Usuario,
                  Reporte.usuario_reportado_id == Usuario.id)
            .outerjoin(Empleador,
                  Usuario.id == Empleador.usuario_id)
            .outerjoin(Postulante,
                  Usuario.id == Postulante.usuario_id)
            .filter(
                Reporte.estado == estado
            )
        )

        if busqueda:
            query = query.filter(
                Reporte.motivo.ilike(f"{busqueda}%")
            )

        return query.offset(offset).limit(limit).all()
