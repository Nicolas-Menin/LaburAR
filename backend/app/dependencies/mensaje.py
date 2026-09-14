from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.services.mensaje_service import MensajeService
from backend.app.repositories.mensaje_dao import MensajeDAO
from backend.app.dependencies.database import obtener_sesion_bd

def obtener_mensaje_service(
    db: Session = Depends(obtener_sesion_bd)
):
    """Funcion para obtener el servicio de mensaje"""

    mensaje_dao = MensajeDAO(db)

    return MensajeService(mensaje_dao=mensaje_dao)
