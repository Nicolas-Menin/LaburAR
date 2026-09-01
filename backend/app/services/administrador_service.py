from backend.app.repositories.administtrador_dao import AdministradorDAO
from backend.app.services.reporte_service import ReporteService
from backend.app.schemas.reporte_schemas import ReporteEstadoUpdate
from backend.app.schemas.usuario_schemas import UsuarioFiltro

class AdministradorService:
    """Service de Adminitrador"""

    def __init__(self,administrador_dao: AdministradorDAO,reporte_service: ReporteService):
        self.administrador_dao = administrador_dao
        self.reporte_service = reporte_service



    def filtrar_usuarios(self, datos: UsuarioFiltro,offset: int):
        """Metodo para filtrar y buscar usuarios por rol"""


        self.administrador_dao.listar_usuarios(datos.rol,datos.busqueda,offset)


    def moderar_reporte(self,datos: ReporteEstadoUpdate):
        """Metodo para moderar el reporte"""

        return self.reporte_service.actualizar_reporte_estado(datos.estado,datos,datos.reporte_id)
