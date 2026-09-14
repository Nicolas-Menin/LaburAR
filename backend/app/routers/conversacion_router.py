from typing import List
from fastapi import APIRouter, Depends
from backend.app.dependencies.conversacion import obtener_conversacion_service
from backend.app.dependencies.usuario import obtener_usuario_service
from backend.app.services.conversacion_service import ConversacionService
from backend.app.services.usuario_service import UsuarioService
from backend.app.schemas.conversacion_schema import ConversacionResponsePostulante, ConversacionResponseEmpleador
from backend.app.core.security import oauth2_scheme

#ROUTER DE CONVERSACION
conversacion_router = APIRouter(prefix="/conversacion",tags=["Conversacion"])


@conversacion_router.get("/traer-conversaciones-postulante",response_model=List[ConversacionResponsePostulante])
async def traer_conversaciones_postulante(
    token: str = Depends(oauth2_scheme),
    conversacion_service: ConversacionService = Depends(obtener_conversacion_service),
    usuario_service: UsuarioService = Depends(obtener_usuario_service)
):
    """Funcion para traer las conversaciones del postulante"""


    usuario_id = usuario_service.obtener_usuario_id(token)

    return conversacion_service.traer_conversacion_postulante(usuario_id)

@conversacion_router.get("/traer-conversaciones-empleador",response_model=List[ConversacionResponseEmpleador])
async def traer_conversaciones_empleador(
    token: str = Depends(oauth2_scheme),
    conversacion_service: ConversacionService = Depends(obtener_conversacion_service),
    usuario_service: UsuarioService = Depends(obtener_usuario_service)
):
    """Funcion para traer las conversaciones del empleador"""


    usuario_id = usuario_service.obtener_usuario_id(token)

    return conversacion_service.traer_conversacion_empleador(usuario_id)