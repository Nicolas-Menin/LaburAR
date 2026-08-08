from sqlalchemy.orm import Session
from backend.app.models.mensaje import Mensaje
from backend.app.models.conversacion import Conversacion

class MensajeDAO:

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

        return (self.db.query(Conversacion).filter(
            Mensaje.conversacion_id  == id_conversacion).all()
        )

    def actualizar_mensaje(self, mensaje: Mensaje):
        """Metodo para actualizar el estado de lectura del mensaje"""

        self.db.commit()
        self.db.refresh(mensaje)

        return mensaje