from typing import List, Literal
from fastapi import APIRouter, Depends, HTTPException
from backend.app.core.security import oauth2_scheme
from backend.app.dependencies.usuario import obtener_usuario_service
from backend.app.dependencies.administrador import obtener_administrador_service
from backend.app.dependencies.postulante import obtener_postulante_service
from backend.app.dependencies.empleador import obtener_empleador_service
from backend.app.services.usuario_service import UsuarioService
from backend.app.services.administrador_service import AdministradorService
from backend.app.services.postulante_service import PostulanteService
from backend.app.services.empleador_service import EmpleadorService
from backend.app.schemas.reporte_schemas import ReporteAdministrador, EmpleadorReporte,PostulanteReporte,ReporteUpdate
from backend.app.schemas.usuario_schemas import UsuarioAdministrador
#ROUTER DE ADMINISTRADOR
administrador_router = APIRouter(prefix="/administrador",tags=["Administrador"])

@administrador_router.put("/actualizar-reporte")
async def actualizar_reporte_estado(
    datos: ReporteUpdate,
    reporte_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para actualizar el estado de reporte"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return administrador_service.moderar_reporte(
        estado=datos.estado,
        reporte_id=reporte_id,
        usuario_id=usuario_id
    )
@administrador_router.get("/obtener-postulante-usuario-id",response_model=PostulanteReporte)
async def obtener_postulante_usuario_id(
    usuario_id: int,
    token: str = Depends(oauth2_scheme),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Metodo para traer postulante mediante el id del usuario"""

    if not token:
        raise HTTPException(401, "Credenciales inexistentes")

    return postulante_service.buscar_por_usuario_id(
        usuario_id=usuario_id
    )

@administrador_router.get("/obtener-empleador-usuario-id",response_model=EmpleadorReporte)
async def obtener_empleador_usuario_id(
    usuario_id: int,
    token: str = Depends(oauth2_scheme),
    empleaodr_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Metodo para traer postulante mediante el id del usuario"""

    if not token:
        raise HTTPException(401, "Credenciales inexistentes")


    return empleaodr_service.buscar_por_usuario_id(
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
@administrador_router.put("/activar-usuario")
async def activar_usuario(
    activar_usuario_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    administrador_service: AdministradorService = Depends(obtener_administrador_service)
):
    """Funcion para desactivar usuario"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return administrador_service.activar_usuario(
        usuario_id=usuario_id,
        activar_usuario_id=activar_usuario_id
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
