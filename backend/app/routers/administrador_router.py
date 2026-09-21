from typing import List, Literal
from fastapi import APIRouter, Depends
from backend.app.core.security import oauth2_scheme
from backend.app.dependencies.usuario import obtener_usuario_service
from backend.app.dependencies.administrador import obtener_administrador_service
from backend.app.services.usuario_service import UsuarioService
from backend.app.services.administrador_service import AdministradorService
from backend.app.schemas.reporte_schemas import ReporteAdministrador
from backend.app.schemas.usuario_schemas import UsuarioAdministrador

#ROUTER DE ADMINISTRADOR
administrador_router = APIRouter(prefix="/administrador",tags=["Administrador"])

@administrador_router.put("/actualizar-reporte")
async def actualizar_reporte_estado(
    estado:  Literal["REVISADO","PENDIENTE","SANCIONADO"],
    reporte_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para actualizar el estado de reporte"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return administrador_service.moderar_reporte(
        estado=estado,
        reporte_id=reporte_id,
        usuario_id=usuario_id
    )

@administrador_router.get("/buscar-reportes",response_model=List[ReporteAdministrador])
async def buscar_reportes(
    filtro:  Literal["REVISADO","PENDIENTE","SANCIONADO"],
    offset: int = 0,
    busqueda: str | None = None,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para que el administrador busque reportes"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return administrador_service.filtrar_reportes(
        usuario_id=usuario_id,
        filtros=filtro,
        busqueda=busqueda,
        offset=offset
    )

@administrador_router.get("/buscar-usuarios",response_model=List[UsuarioAdministrador])
async def buscar_usuarios(
    filtro: Literal["POSTULANTE","EMPLEADOR"],
    busqueda: str | None = None,
    offset: int = 0,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para que el administrador busque usuarios"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return administrador_service.filtrar_usuarios(
        usuario_id=usuario_id,
        filtros=filtro,
        offset=offset,
        busqueda=busqueda
    )

@administrador_router.put("/desactivar-usuario")
async def desactivar_usuario(
    desactivar_usuario_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para desactivar usuario"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return administrador_service.desactivar_usuario(
        desactivar_usuario_id=desactivar_usuario_id,
        usuario_id=usuario_id
        )

@administrador_router.put("/banear-usuario")
async def banear_usuario(
    banear_usuario_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para desactivar usuario"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return administrador_service.banear_usuario(
        banear_usuario_id=banear_usuario_id,
        usuario_id=usuario_id
        )
