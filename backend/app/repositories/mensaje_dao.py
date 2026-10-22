from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from backend.app.models.mensaje import Mensaje
from backend.app.models.conversacion import Conversacion
from backend.app.models.empleador import Empleador
from backend.app.models.postulante import Postulante
from backend.app.models.conexion_laboral import ConexionLaboral

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
        """Metodo para contar todos los mensajes no leidos del usuario"""

        return (
            self.db.query(func.count(Mensaje.id))
            .join(Conversacion, Conversacion.id == Mensaje.conversacion_id)
            .join(
                ConexionLaboral,
                ConexionLaboral.id == Conversacion.conexion_laboral_id
            )
            .join(Postulante, Postulante.id == ConexionLaboral.postulante_id)
            .join(Empleador, Empleador.id == ConexionLaboral.empleador_id)
            .filter(Mensaje.leido.is_(False))
            .filter(Mensaje.remitente_id != usuario_id)
            .filter(
                or_(
                    Postulante.usuario_id == usuario_id,
                    Empleador.usuario_id == usuario_id,
                )
            )
            .scalar()
        )

    def buscar_por_id(self,id_mensaje: int):
        """Metodo para buscar un mensaje por id"""


        return self.db.query(Mensaje).filter(Mensaje.id == id_mensaje).first()

    def contar_mensajes_no_leidos(self,usuario_id: int, conversacion_id: int):
        """Metodo para contar mensajes no leidos de una conversacion."""

        return (
            self.db.query(Mensaje)
            .join(
                Conversacion,
                Mensaje.conversacion_id == Conversacion.id
            )
            .filter(Mensaje.conversacion_id == conversacion_id)
            .filter(Mensaje.remitente_id != usuario_id)
            .filter(Mensaje.leido == False)
            .filter(Mensaje.conversacion_id == Conversacion.id)

        ).count()
