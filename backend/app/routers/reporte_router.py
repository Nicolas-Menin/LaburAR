from fastapi import APIRouter, Depends
from backend.app.dependencies.reporte import obtener_reporte_service
from backend.app.services.reporte_service import ReporteService
from backend.app.services.usuario_service import UsuarioService
from backend.app.dependencies.usuario import obtener_usuario_service
from backend.app.schemas.reporte_schemas import ReporteCreate
from backend.app.core.security import oauth2_scheme

#ROUTER DE REPORTE
reporte_router = APIRouter(prefix="/reporte",tags=["Reporte"])

@reporte_router.post("/crear-reporte")
async def crear_reporte(
    datos: ReporteCreate,
    usuario_reportado_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    reporte_service: ReporteService = Depends(obtener_reporte_service)
):
    """Funcion para crear un reporte"""

    usuario_id = usuario_service.obtener_usuario_id(token)


    return reporte_service.crear_reporte(
        datos= datos,
        usuario_id=usuario_id,
        usuario_reportado_id=usuario_reportado_id
    )
