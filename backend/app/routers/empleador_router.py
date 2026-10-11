from typing import List, Literal
from fastapi import APIRouter, Depends
from backend.app.services.empleador_service import EmpleadorService
from backend.app.services.conexion_laboral_service import ConexionLaboralService
from backend.app.schemas.conexion_laboral_schemas import ConexionLaboralEmpleador,ConexionLaboralCreate,ConexionLaboralEmpleadorFiltros
from backend.app.services.usuario_service import UsuarioService
from backend.app.dependencies.usuario import obtener_usuario_service
from backend.app.dependencies.conexion_laboral import obtener_conexion_laboral_service
from backend.app.dependencies.empleador import obtener_empleador_service
from backend.app.schemas.empleador_schemas import (EmpleadorUpdate, EmpleadorPerfil,
                                                   EmpleadorSearch,EmpleadorFiltro)
from backend.app.schemas.postulacion_schemas import PostulacionEmpleador, PostulacionStateUpdate
from backend.app.schemas.oferta_laboral_schemas import OfertaLaboralCreate,OfertaLaboralUpdate,OfertaLaboralEmpleador
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
    busqueda: str | None = None,
    offset: int = 0,
    filtros: EmpleadorFiltro = Depends(),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para buscar empleadores"""

    return empleador_service.buscar_empleadores(filtros,busqueda,offset)

@empleador_router.put("/actualizar-empleador")
async def actualizar_empleador(
    datos: EmpleadorUpdate,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para actualizar los datos del empleador"""

    usuario_id = usuario_service.obtener_usuario_id(token)


    return empleador_service.actualizar_empleador(
        datos=datos,
        usuario_id=usuario_id,
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

@empleador_router.put("/actualizar-estado-postulacion")
async def actualizar_estado_postulacion(
    datos: PostulacionStateUpdate,
    oferta_id: int,
    postulacion_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_servicec: UsuarioService = Depends(obtener_usuario_service),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Metodo para actualizar el estado de una postulacion de oferta laboral"""

    usuario_id = usuario_servicec.obtener_usuario_id(token)

    return empleador_service.actualizar_estado_postulacion(
        usuario_id,
        oferta_id,
        postulacion_id,
        datos.estado
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

@empleador_router.get("/filtrar-ofertas-laborales",response_model=List[OfertaLaboralEmpleador])
async def filtrar_ofertas_laborales(
    busqueda: str | None = None,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para filtrar ofertas laborales de empleador"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return empleador_service.listar_ofertas_laborales(usuario_id,busqueda)

@empleador_router.get("/verificar-conexion-oferta-laboral",response_model=List[OfertaLaboralEmpleador] | None)
async def verificar_conexion_oferta_laboral(
    postulante_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para verificar si un postulante posee una conexion laboral con oferta laboral de empleador"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return empleador_service.verificar_conexion_por_oferta(usuario_id,postulante_id)

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
    datos: ConexionLaboralCreate,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    conexion_laboral_service: ConexionLaboralService = Depends(obtener_conexion_laboral_service)
):
    """Funcion para crear conexion laboral"""

    usuario_id = usuario_service.obtener_usuario_id(token)


    return conexion_laboral_service.crear_conexion_laboral(
        usuario_id=usuario_id,
        oferta_id=datos.oferta_laboral_id,
        postulante_id=datos.postulante_id
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
    """Funcion para crear conexion laboral mediante la aceptacion de una postulacion"""

    usuario_id = usuario_service.obtener_usuario_id(token)


    return conexion_laboral_service.crear_conexion_laboral_postulacion(
        usuario_id=usuario_id,
        oferta_id=oferta_laboral_id,
        postulante_id=postulante_id,
        estado=estado
    )

@empleador_router.get("/buscar-conexiones-laborales",response_model=List[ConexionLaboralEmpleador])
async def buscar_conexiones_laborales(
    filtros: ConexionLaboralEmpleadorFiltros = Depends(),
    busqueda: str | None = None,
    offset: int = 0,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    conexion_laboral_service: ConexionLaboralService = Depends(obtener_conexion_laboral_service)
):
    """Funcion para buscar las conexiones laborales de empleador"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return conexion_laboral_service.traer_conexiones_laborales_empleador(
        usuario_id=usuario_id,
        offset=offset,
        busqueda=busqueda,
        oferta_id=filtros.oferta_id
    )

@empleador_router.get("/verificar-conexion-laboral",response_model= ConexionLaboralEmpleador | None)
async def verificar_conexion_laboral(
    postulante_id: int,
    oferta_id: int | None = None,
    token: str = Depends(oauth2_scheme),
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

@empleador_router.get("/{empleador_id}",response_model=EmpleadorPerfil)
async def obtener_empleador_por_id(
    empleador_id: int,
    empleador_service: EmpleadorService = Depends(obtener_empleador_service)
):
    """Funcion para obtener el perfil publico de un empleador por su id"""

    return empleador_service.obtener_por_empleador_id(empleador_id)
