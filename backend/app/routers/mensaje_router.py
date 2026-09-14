from fastapi import APIRouter, Depends,WebSocket
from backend.app.schemas.mensaje_schemas import MensajeCreate,MensajeList, MensajeStateUpdate
from backend.app.services.mensaje_service import MensajeService
from backend.app.services.usuario_service import UsuarioService
from backend.app.dependencies.usuario import obtener_usuario_service
from backend.app.dependencies.mensaje import obtener_mensaje_service
from backend.app.core.security import oauth2_scheme


#ROUTER DE MENSAJE
mensaje_router = APIRouter(prefix="/mensajes",tags=["Mensajes"])


@mensaje_router.websocket("/{conversacion_id}")
async def conectar_chat(
    websocket: WebSocket,
    conversacion_id: int,
    mensaje_service: MensajeService = Depends(obtener_mensaje_service)
):
    """Funcion para conectar un chat entre postulante y empleador"""
    await websocket.accept()


    while True:

        datos = await websocket.receive_json()

        nuevo_mensaje = MensajeCreate(
            remitente_id= datos["remitente_id"],
            conversacion_id= conversacion_id,
            contenido=datos["contenido"]
        )

        mensaje = mensaje_service.crear_mensaje(nuevo_mensaje)

        await websocket.send_json({
            "id": mensaje.id,
            "remitente_id": mensaje.remitente_id,
            "contenido": mensaje.contenido,
            "fecha_envio": mensaje.fecha_envio,
            "leido": mensaje.leido
        })

@mensaje_router.get("/listar-mensajes/{conversacion_id}",response_model=MensajeList)
async def listar_mennsajes(
    conversacion_id: int,
    mensaje_service: MensajeService = Depends(obtener_mensaje_service)
):
    """Funcion para listar mensajes de conversacion"""

    return mensaje_service.listar_mensajes(
        conversacion_id= conversacion_id
    )

@mensaje_router.put("/actualizar-estado-mensajes")
async def actualizar_estado_mensajes(
    datos: MensajeStateUpdate,
    mensaje_service: MensajeService = Depends(obtener_mensaje_service)
):
    """Funcion para actualizar el estado de mensajes"""


    return mensaje_service.actualizar_estados_mensajes(datos)

@mensaje_router.get("/mensajes-no-leidos")
async def verificar_mensajes_no_leidos(
    token: str = Depends(oauth2_scheme),
    usuario_service: UsuarioService = Depends(obtener_usuario_service),
    mensaje_service: MensajeService = Depends(obtener_mensaje_service)
):
    """Funcion para verificar si el usuario tiene mensajes no leidos"""

    usuario_id = usuario_service.obtener_usuario_id(token)

    return mensaje_service.existe_mensajes_no_leidos(
        usuario_id=usuario_id
    )
