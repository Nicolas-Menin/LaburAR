from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.services.conexion_laboral_service import ConexionLaboralService
from backend.app.repositories.conexion_laboral_dao import ConexionLaboralDAO
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.empleador_dao import EmpleadorDAO
from backend.app.repositories.oferta_laboral_dao import OfertaLaboralDAO
from backend.app.repositories.postulacion_dao import PostulacionDAO
from backend.app.repositories.conversacion_dao import ConversacionDAO
from backend.app.dependencies.database import obtener_sesion_bd


def obtener_conexion_laboral_service(
    db: Session = Depends(obtener_sesion_bd)
):
    """Funcion para obtener servicio de conexion laboral"""

    conexion_laboral_dao = ConexionLaboralDAO(db)

    postulante_dao = PostulanteDAO(db)

    empleador_dao = EmpleadorDAO(db)

    oferta_laboral_dao = OfertaLaboralDAO(db)

    conversacion_dao = ConversacionDAO(db)

    postulacion_dao = PostulacionDAO(db)

    return ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
        )
