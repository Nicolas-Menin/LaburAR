from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.dependencies.database import obtener_sesion_bd
from backend.app.services.conversacion_service import ConversacionService
from backend.app.repositories.conversacion_dao import ConversacionDAO
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.empleador_dao import EmpleadorDAO
from backend.app.repositories.mensaje_dao import MensajeDAO

def obtener_conversacion_service(
    db: Session = Depends(obtener_sesion_bd)
):

    conversacion_dao = ConversacionDAO(db)

    postulante_dao = PostulanteDAO(db)

    empleador_dao = EmpleadorDAO(db)

    mensaje_dao = MensajeDAO(db)


    return ConversacionService(
        conversacion_dao=conversacion_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        mensaje_dao=mensaje_dao
    )