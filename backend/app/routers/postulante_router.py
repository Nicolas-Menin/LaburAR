from typing import List, Literal
from fastapi import APIRouter, Depends
from backend.app.services.postulante_service import PostulanteService
from backend.app.dependencies.postulante import obtener_postulante_service
from backend.app.schemas.postulante_schemas import (PostulantePerfil, PostulanteSearch,
                                                    PostulanteFiltro,PostulanteUpdate)
from backend.app.dependencies.usuario import obtener_usuario_service
from backend.app.dependencies.conexion_laboral import obtener_conexion_laboral_service
from backend.app.services.conexion_laboral_service import ConexionLaboralService
from backend.app.services.usuario_service import UsuarioService
from backend.app.services.postulacion_service import PostulacionService
from backend.app.schemas.conexion_laboral_schemas import ConexionLaboralPostulante
from backend.app.dependencies.postulacion import obtener_postulacion_service
from backend.app.schemas.estudio_schemas import EstudioCreate, EstudioUpdate
from backend.app.schemas.experiencia_laboral_schemas import (ExperienciaLaboralCreate,
                                                             ExperienciaLaboralUpdate)
from backend.app.schemas.habilidad_schemas import HabilidadCreate
from backend.app.schemas.postulacion_schemas import PostulacionPostulante,PostulacionFiltro
from backend.app.core.security import oauth2_scheme


#ROUTER DE POSTULANTE
postulante_router = APIRouter(prefix="/postulante",tags=["Postulante"])


@postulante_router.get("/perfil",response_model=PostulantePerfil)

async def perfil_postulante(
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
    ):
    """Funcion para obtener el perfil del postulante"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulante_service.perfil_postulante(usuario_id)


@postulante_router.get("/buscar-postulantes",response_model=List[PostulanteSearch])

async def buscar_postulantes(
    offset: int = 0,
    filtros: PostulanteFiltro = Depends(),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para buscar postulantes"""

    return postulante_service.buscar_postulantes(filtros,offset)

@postulante_router.put("/actualizar-postulante")

async def actualizar_postulante(
    datos: PostulanteUpdate,
    foto_perfil: str | None = None,
    cv: str | None = None,
    token:  str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para actualizar los datos de postulante"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulante_service.actualizar_postulante(
        datos=datos,
        usuario_id=usuario_id,
        foto_perfil=foto_perfil,
        cv =  cv
    )

@postulante_router.post("/crear-estudio")

async def crear_estudio(
    datos: EstudioCreate,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulate_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para crear estudio de postulante"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulate_service.crear_estudio(
        datos=datos,
        usuario_id=usuario_id
    )

@postulante_router.put("/actualizar-estudio")
async def actualizar_estudio(
    datos: EstudioUpdate,
    estudio_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para actualizar el estudio de un postulante"""


    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulante_service.actualizar_estudio(
        datos=datos,
        usuario_id=usuario_id,
        estudio_id=estudio_id
    )


@postulante_router.delete("/eliminar-estudio")
async def eliminar_estudio(
    estudio_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para eliminar el estudio de un postulante"""


    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulante_service.eliminar_estudio(
        estudio_id=estudio_id,
        usuario_id=usuario_id
    )

@postulante_router.post("/crear-experiencia-laboral")
async def crear_experiencia_laboral(
    datos: ExperienciaLaboralCreate,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para crear experiencia laboral de postulante"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulante_service.crear_experiencia_laboral(
        datos=datos,
        usuario_id=usuario_id
    )

@postulante_router.put("/actualizar-experiencia-laboral")
async def actualizar_experiencia_laboral(
    datos: ExperienciaLaboralUpdate,
    experiencia_laboral_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para actualizar experiencia laboral de postulante"""


    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulante_service.actualizar_experiencia_laboral(
        datos=datos,
        usuario_id=usuario_id,
        experiencia_laboral_id=experiencia_laboral_id
    )

@postulante_router.delete("/eliminar-experiencia-laboral")
async def eliminar_experiencia_laboral(
    experiencia_laboral_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para eliminar experiencia laboral de postulante"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulante_service.eliminar_experiencia_laboral(
        experiencia_laboral_id=experiencia_laboral_id,
        usuario_id=usuario_id
    )

@postulante_router.post("/crear-habilidad")
async def crear_habilidad(
    datos: HabilidadCreate,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para crear habilidad de postulante"""

    usuario_id = usuario_service.obtener_usuario_id(token)


    return postulante_service.crear_habilidad(
        datos=datos,
        usuario_id=usuario_id
    )

@postulante_router.delete("/eliminar-habilidad")
async def eliminar_habilidad(
    habilidad_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para eliminar habilidad de postulante"""

    usuario_id =  usuario_service.obtener_usuario_id(token)


    return postulante_service.eliminar_habilidad(
        habilidad_id= habilidad_id,
        usuario_id=usuario_id
    )


@postulante_router.get("/mis-postulaciones",response_model=List[PostulacionPostulante])
async def filtrar_postulaciones(
    datos: PostulacionFiltro,
    offset: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulante_service: PostulanteService = Depends(obtener_postulante_service)
):
    """Funcion para obtener las postulacuiones del postulante"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulante_service.filtrar_postulaciones(
        datos= datos,
        usuario_id=usuario_id,
        offset=offset
    )

@postulante_router.post("crear-postulacion")
async def crear_postulacion(
    oferta_id: int,
    token: str =  Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulacion_service: PostulacionService = Depends(obtener_postulacion_service)
):
    """Funcion para crear postulacion a oferta laboral"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulacion_service.crear_postulacion(
        usuario_id=usuario_id,
        oferta_id=oferta_id
    )

@postulante_router.get("verificar-postulacion",response_model=PostulacionPostulante)
async def verificar_postulacion(
    oferta_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    postulacion_service: PostulacionService = Depends(obtener_postulacion_service)
):
    """Funcion para verificar si un postulante esta postulado a una oferta laboral"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return postulacion_service.verificar_postulacion(
        usuario_id=usuario_id,
        oferta_id=oferta_id
    )

@postulante_router.put("/actualizar-solicitud-laboral")
async def actualizar_conexion_laboral(
    conexion_laboral_id: int,
    estado: Literal["ACEPTADA","RECHAZADA"],
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    conexion_laboral_service: ConexionLaboralService = Depends(obtener_conexion_laboral_service)
):
    """Funcion para aceptar conexion laboral con empleador"""


    usuario_id = usuario_service.obtener_usuario_id(token)

    return conexion_laboral_service.actualizar_conexion_laboral_estado(
        usuario_id=usuario_id,
        conexion_laboral_id=conexion_laboral_id,
        estado=estado
    )

@postulante_router.get("/verificar-conexion-laboral",response_model=ConexionLaboralPostulante | None)
async def verificar_conexion_laboral(
    oferta_id: int,
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    conexion_laboral_service: ConexionLaboralService = Depends(obtener_conexion_laboral_service)
):
    """Funcion paara verificar si existe una conexion laboral de postulante"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return conexion_laboral_service.verificar_conexion_laboral_postulante(
        usuario_id=usuario_id,
        oferta_id=oferta_id
    )

@postulante_router.get("/buscar-solicitudes-laborales",response_model=List[ConexionLaboralPostulante])
async def buscar_conexiones_laborales(
    offset: int = 0,
    token: str = Depends(oauth2_scheme),
    busqueda: str | None = None,
    conexion_laboral_service: ConexionLaboralService = Depends(obtener_conexion_laboral_service),
    usuario_service: UsuarioService = Depends(obtener_usuario_service)
):
    """Funcion para buscar conexiones laborales del postulante"""


    usuario_id = usuario_service.obtener_usuario_id(token)

    return conexion_laboral_service.traer_conexiones_laborales_postulante(
        usuario_id=usuario_id,
        busqueda=busqueda,
        offset=offset
    )
