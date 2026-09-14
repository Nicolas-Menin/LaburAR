from sqlalchemy.orm import Session
from backend.app.models.mensaje import Mensaje

class MensajeDAO:
    """Clase encargada del acceso a los datos de mensaje"""

    def __init__(self, db: Session):
        self.db = db


    def crear_mensaje(self,mensaje: Mensaje):
        """Metodo para crear mensaje de usuario"""
        self.db.add(mensaje)
        self.db.commit()
        self.db.refresh(mensaje)

        return mensaje

    def listar_mensajes(self,id_conversacion: int):
        """Metodo para listar los mensajes"""

        return (self.db.query(Mensaje)
            .filter(
            Mensaje.conversacion_id  == id_conversacion)
            .order_by(Mensaje.fecha_envio.asc())
            .all()
        )

    def actualizar_estados_mensajes(self):
        """Metodo para actualizar el estado de lectura del mensaje"""

        self.db.commit()

    def existe_mensajes_no_leidos(self, usuario_id: int):
        """Metodo para verificar si hay mensajes no leidos"""

        return (
            self.db.query(
                Mensaje,
            )
            .filter(Mensaje.leido == False)
            .filter(Mensaje.remitente_id != usuario_id)
        ).all()

    def buscar_por_id(self,id_mensaje: int):
        """Metodo para buscar un mensaje por id"""


        return self.db.query(Mensaje).filter(Mensaje.id == id_mensaje).first()

    def contar_mensajes_no_leidos(self,usuario_id: int, conversacion_id: int):
        """Metodo para contar mensajes no leidos de una conversacion."""

        return (
            self.db.query(Mensaje)
            .filter(Mensaje.conversacion_id == conversacion_id)
            .filter(Mensaje.remitente_id != usuario_id)
            .filter(Mensaje.leido == False)
        ).count()
