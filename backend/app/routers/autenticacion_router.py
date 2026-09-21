from fastapi import APIRouter, Depends
from backend.app.schemas.postulante_schemas import RegistroPostulante
from backend.app.schemas.empleador_schemas import RegistroEmpleador
from backend.app.services.usuario_service import UsuarioService
from backend.app.schemas.usuario_schemas import UsuarioLogin, UsuarioEmail,TokenResponse
from backend.app.dependencies.usuario import obtener_usuario_service

#ROUTER DE AUTENTICACION
autenticacion_router = APIRouter(prefix="/autenticacion",tags=["Autenticacion"])


@autenticacion_router.post("/registrar-postulante")
async def registrar_postulante(
    postulante: RegistroPostulante,
    usuario_service: UsuarioService = Depends(obtener_usuario_service)
    ):
    """Funcion para registrar postulante"""

    return usuario_service.registrar_postulante(postulante)


@autenticacion_router.post("/registrar-empleador")
async def registrar_empleador(
    empleador: RegistroEmpleador,
    usuario_service: UsuarioService = Depends(obtener_usuario_service)
    ):
    """Funcion para registrar empleador"""

    return usuario_service.registrar_empleador(empleador)


@autenticacion_router.post("/login/",response_model=TokenResponse)
async def iniciar_sesion(
    usuario: UsuarioLogin,
    usuario_service: UsuarioService = Depends(obtener_usuario_service)
    ):
    """Funcion para que el usuario iniciar sesion"""

    return usuario_service.iniciar_sesion(
        email= usuario.email,
        password= usuario.password
    )

@autenticacion_router.post("/resetear-contraseña")
async def recuperar_contrasena(
    datos: UsuarioEmail,
    usuario_service: UsuarioService = Depends(obtener_usuario_service)
    ):
    """Funcion para restablecer contraseña del usuario"""

    return usuario_service.recuperacion_contrasena(datos.email)
