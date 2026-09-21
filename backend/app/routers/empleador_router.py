from typing import List, Literal
from fastapi import APIRouter, Depends
from backend.app.services.empleador_service import EmpleadorService
from backend.app.services.conexion_laboral_service import ConexionLaboralService
from backend.app.schemas.conexion_laboral_schemas import ConexionLaboralEmpleador
from backend.app.services.usuario_service import UsuarioService
from backend.app.dependencies.usuario import obtener_usuario_service
from backend.app.dependencies.conexion_laboral import obtener_conexion_laboral_service
from backend.app.dependencies.empleador import obtener_empleador_service
from backend.app.schemas.empleador_schemas import (EmpleadorUpdate, EmpleadorPerfil,
                                                   EmpleadorSearch,EmpleadorFiltro)
from backend.app.schemas.postulacion_schemas import PostulacionEmpleador
from backend.app.schemas.oferta_laboral_schemas import OfertaLaboralCreate,OfertaLaboralUpdate
from backend.app.core.security import oauth2_scheme

# ROUTER DE EMPLEADOR
empleador_router = APIRouter(prefix="/empleador",tags=["Empleador"])

@empleador_router.get("/perfil-empleador",response_model=EmpleadorPerfil)
async def perfil_empleador(
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para obtener perfil de empleador"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return empleador_service.perfil_empleador(usuario_id)

@empleador_router.get("/buscar-empleadores",response_model=List[EmpleadorSearch])
async def buscar_empleadores(
    filtros: EmpleadorFiltro = Depends(),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para buscar empleadores"""

    return empleador_service.buscar_empleadores(filtros)

@empleador_router.put("/actualizar-empleador")
async def actualizar_empleador(
    datos: EmpleadorUpdate,
    foto_perfil: str | None = None,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para actualizar los datos del empleador"""

    usuario_id = usuario_service.obtener_usuario_id(token)


    return empleador_service.actualizar_empleador(
        datos=datos,
        usuario_id=usuario_id,
        foto_perfil=foto_perfil
    )

@empleador_router.get("/filtrar-postulaciones-oferta-laboral",response_model=List[PostulacionEmpleador])
async def filtrar_postulaciones(
    offset: int = 0,
    busqueda: str | None = None,
    oferta_id: int | None = None,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para filtrar postulaciones de una oferta laboral"""

    usuario_id = usuario_service.obtener_usuario_id(token)


    return empleador_service.filtrar_postulaciones_oferta_laboral(
        usuario_id=usuario_id,
        offset=offset,
        busqueda=busqueda,
        oferta_id=oferta_id
    )


@empleador_router.post("/crear-oferta-laboral")
async def crear_oferta_laboral(
    datos: OfertaLaboralCreate,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para crear una oferta laboral de empleador"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return empleador_service.crear_oferta_laboral(datos,usuario_id)


@empleador_router.put("/actualizar-oferta-laboral")
async def actualizar_oferta_laboral(
    datos: OfertaLaboralUpdate,
    oferta_laboral_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para actualizar oferta laboral de empleador"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return empleador_service.actualizar_oferta_laboral(
        datos=datos,
        oferta_laboral_id=oferta_laboral_id,
        usuario_id=usuario_id
    )

@empleador_router.post("/crear-conexion-laboral")
async def crear_conexion_laboral(
    oferta_laboral_id: int,
    postulante_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    conexion_laboral_service: ConexionLaboralService = Depends(obtener_conexion_laboral_service)
):
    """Funcion para crear conexion laboral"""

    usuario_id = usuario_service.obtener_usuario_id(token)


    return conexion_laboral_service.crear_conexion_laboral(
        usuario_id=usuario_id,
        oferta_id=oferta_laboral_id,
        postulante_id=postulante_id
    )

@empleador_router.post("/crear-conexion-laboral-postulacion")
async def crear_conexion_laboral_postulacion(
    oferta_laboral_id: int,
    postulante_id: int,
    estado: Literal["ACEPTADA","RECHAZADA"],
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    conexion_laboral_service: ConexionLaboralService = Depends(obtener_conexion_laboral_service)
):
    """Funcion para crear conexion laboral medianter la aceptacion de una postulacion"""

    usuario_id = usuario_service.obtener_usuario_id(token)


    return conexion_laboral_service.crear_conexion_laboral_postulacion(
        usuario_id=usuario_id,
        oferta_id=oferta_laboral_id,
        postulante_id=postulante_id,
        estado=estado
    )

@empleador_router.get("/buscar-conexiones-laboorales",response_model=List[ConexionLaboralEmpleador])
async def buscar_conexiones_laborales(
    offset: int = 0,
    busqueda: str | None = None,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    conexion_laboral_service: ConexionLaboralService = Depends(obtener_conexion_laboral_service)
):
    """Funcion para buscar las conexiones laborales de empleador"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return conexion_laboral_service.traer_conexiones_laborales_empleador(
        usuario_id=usuario_id,
        offset=offset,
        busqueda=busqueda
    )

@empleador_router.get("/verificar-conexion-laboral",response_model= ConexionLaboralEmpleador | None)
async def verificar_conexion_laboral(
    postulante_id: int,
    token: str = Depends(oauth2_scheme),
    oferta_id: int | None = None,
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    conexion_laboral_service: ConexionLaboralService = Depends(obtener_conexion_laboral_service)
):
    """Funcion para verificar si existe una conexion laboral de postulante"""

    usuario_id = usuario_service.obtener_usuario_id(token)


    return conexion_laboral_service.verificar_conexion_laboral_empleador(
        usuario_id=usuario_id,
        postulante_id=postulante_id,
        oferta_id=oferta_id
    )
