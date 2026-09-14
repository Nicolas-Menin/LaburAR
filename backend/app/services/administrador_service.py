from backend.app.repositories.administtrador_dao import AdministradorDAO
from backend.app.services.reporte_service import ReporteService
from backend.app.schemas.reporte_schemas import ReporteEstadoUpdate
from backend.app.schemas.usuario_schemas import UsuarioFiltro

class AdministradorService:
    """Service de Administrador"""

    def __init__(self,administrador_dao: AdministradorDAO,reporte_service: ReporteService):
        self.administrador_dao = administrador_dao
        self.reporte_service = reporte_service



    def filtrar_usuarios(self, datos: UsuarioFiltro,offset: int = 0,busqueda: str | None = None):
        """Metodo para filtrar y buscar usuarios por rol"""


        self.administrador_dao.listar_usuarios(datos.rol,busqueda,offset)


    def moderar_reporte(self,datos: ReporteEstadoUpdate,reporte_id: int):
        """Metodo para moderar el reporte"""

        return self.reporte_service.actualizar_reporte_estado(datos.estado,datos,reporte_id)

    def desactivar_usuario(self,usuario_id:int):
        """Metodo para desactivar usuario"""

        return self.administrador_dao.desactivar_usuario(usuario_id)

    def banear_usuario(self,usuario_id:int):
        """Metodo para banear usuario"""

        return self.administrador_dao.banear_usuario(usuario_id)