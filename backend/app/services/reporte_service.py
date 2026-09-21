
from backend.app.repositories.reporte_dao import ReporteDAO
from backend.app.models.reporte import Reporte
from backend.app.schemas.reporte_schemas import ReporteCreate

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

