from backend.app.repositories.mensaje_dao import MensajeDAO
from backend.app.schemas.mensaje_schemas import MensajeCreate, MensajeStateUpdate
from backend.app.models.mensaje import Mensaje


class MensajeService:
    """Service de Mensaje"""


    def __init__(self,mensaje_dao: MensajeDAO):
        self.mensaje_dao = mensaje_dao



    def crear_mensaje(self,datos:MensajeCreate):
        """Metodo para crear mensae"""

        mensaje = Mensaje(
            conversacion_id = datos.conversacion_id,
            remitente_id = datos.remitente_id,
            contenido = datos.contenido
        )

        return self.mensaje_dao.crear_mensaje(mensaje)

    def listar_mensajes(self,conversacion_id: int):
        """Metodo para listar los mensajes de un chat"""

        mensajes =  self.mensaje_dao.listar_mensajes(conversacion_id)

        return {
            "mensajes": mensajes
        }

    def actualizar_estados_mensajes(self,datos: MensajeStateUpdate):
        """Metodo para actualizar el estado de leido del mensaje"""

        mensajes = self.mensaje_dao.listar_mensajes(datos.id_conversacion)

        for mensaje in mensajes:

            if mensaje.remitente_id != datos.usuario_id and not mensaje.leido:
                mensaje.leido = True

        return self.mensaje_dao.actualizar_estados_mensajes()

    def existe_mensajes_no_leidos(self,usuario_id:int):
        """Metodo para verificar si el usuario tiene mensajes no leidos"""

        mensajes = self.mensaje_dao.existe_mensajes_no_leidos(usuario_id)

        return {
            "cantidad_mensajes_no_leidos": len(mensajes),
        }