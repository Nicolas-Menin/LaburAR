import json
import websockets

from frontend.src.session.sesion import Sesion
from frontend.src.core.config import API_URL


class ChatService:
    """Service de Chat"""

    @staticmethod
    async def conectar(
        conversacion_id: int
    ):
        """Metodo para conectar conexion websocket"""

        url = f"ws://{API_URL}/mensajes/{conversacion_id}?token={Sesion.token}"

        return await websockets.connect(url)

    @staticmethod
    async def enviar_mensajes(
        conexion: websockets.ClientConnection,
        contenido: str
    ):
        """Metodo para enviar mensajes mediante websocket"""


        await conexion.send(
            json.dumps({
                "contenido": contenido
            })
        )

    @staticmethod
    async def recibir_mensajes(
        conexion: websockets.ClientConnection
    ):
        """Metodo para recibir mensajes mediante websocket"""

        return json.loads(await conexion.recv())

    @staticmethod
    async def cerrar(
        conexion: websockets.ClientConnection
    ):
        """Metodo para cerrar conexion websocket"""

        await conexion.close()