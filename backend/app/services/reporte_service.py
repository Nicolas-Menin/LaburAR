from typing import Literal
from backend.app.repositories.reporte_dao import ReporteDAO
from backend.app.models.reporte import Reporte
from backend.app.schemas.reporte_schemas import ReporteCreate, ReporteFiltro

class ReporteService:
    """Service de Reporte"""


    def __init__(self,reporte_dao: ReporteDAO):
        self.reporte_dao = reporte_dao



    def crear_reporte(self,datos: ReporteCreate,usuario_id: int,usuario_reportado_id: int):
        """Metodo para crear un reporte a un usuario"""


        reporte =  Reporte(
            usuario_id = usuario_id,
            usuario_reportado_id = usuario_reportado_id,
            motivo = datos.motivo,
            descripcion = datos.descripcion,
            estado =  "PENDIENTE"
        )

        return self. reporte_dao.crear_reporte(reporte)


    def actualizar_reporte_estado(
        self,
        estado: Literal["REVISADO","PENDIENTE","SANCIONADO"],
        reporte_id: int

        ):
        """Metodo para actualizar el estado de un reporte"""


        reporte = self.reporte_dao.buscar_reporte_por_id(reporte_id)
        reporte.estado = estado


        return self.reporte_dao.actualizar_reporte(reporte)


    def filtrar_reportes(
        self,
        filtros: ReporteFiltro,
        busqueda: str | None = None,
        offset: int = 0,
        ):
        """Metodo para filtrar y buscar reportes"""


        return self.reporte_dao.listar_reportes(filtros.estado,busqueda,offset)