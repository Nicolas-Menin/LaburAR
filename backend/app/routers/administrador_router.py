from typing import List
from fastapi import APIRouter, Depends
from backend.app.dependencies.reporte import obtener_reporte_service
from backend.app.dependencies.administrador import obtener_administrador_service
from backend.app.services.reporte_service import ReporteService
from backend.app.services.administrador_service import AdministradorService
from backend.app.schemas.reporte_schemas import( ReporteAdministrador,
                                                ReporteEstadoUpdate,
                                                ReporteFiltro)
from backend.app.schemas.usuario_schemas import UsuarioAdministrador, UsuarioFiltro

#ROUTER DE ADMINISTRADOR
administrador_router = APIRouter(prefix="/administrador",tags=["Administrador"])

@administrador_router.put("/actualizar-reporte")
async def actualizar_reporte_estado(
    datos: ReporteEstadoUpdate,
    reporte_id: int,
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para actualizar el estado de reporte"""

    return administrador_service.moderar_reporte(
        datos=datos,
        reporte_id=reporte_id
    )

@administrador_router.get("/buscar-reportes",response_model=List[ReporteAdministrador])
async def buscar_reportes(
    filros: ReporteFiltro = Depends(),
    offset: int = 0,
    busqueda: str | None = None,
    reporte_service: ReporteService = Depends(obtener_reporte_service)
):
    """Funcion para que el administrador busque reportes"""


    return reporte_service.filtrar_reportes(
        filtros=filros,
        busqueda=busqueda,
        offset=offset
    )

@administrador_router.get("buscar-usuarios",response_model=List[UsuarioAdministrador])
async def buscar_usuarios(
    datos: UsuarioFiltro,
    busqueda: str | None = None,
    offset: int = 0,
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para que el administrador busque usuarios"""

    return administrador_service.filtrar_usuarios(
        datos=datos,
        offset=offset,
        busqueda=busqueda
    )

@administrador_router.put("/desactivar-usuario")
async def desactivar_usuario(
    usuario_id: int,
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para desactivar usuario"""

    return administrador_service.desactivar_usuario(usuario_id=usuario_id)

@administrador_router.put("/banear-usuario")
async def banear_usuario(
    usuario_id: int,
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para desactivar usuario"""

    return administrador_service.banear_usuario(usuario_id=usuario_id)