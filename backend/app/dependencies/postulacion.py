from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.services.postulacion_service import PostulacionService
from backend.app.repositories.postulacion_dao import PostulacionDAO
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.oferta_laboral_dao import OfertaLaboralDAO
from backend.app.repositories.empleador_dao import EmpleadorDAO
from backend.app.dependencies.database import obtener_sesion_bd


def obtener_postulacion_service(
    db: Session = Depends(obtener_sesion_bd)
):
    """Funcion para obtener el servicio de postulacion"""

    postulacion_dao = PostulacionDAO(db)

    postulante_dao = PostulanteDAO(db)

    oferta_laboral_dao = OfertaLaboralDAO(db)

    empleador_dao = EmpleadorDAO(db)

    return PostulacionService(postulacion_dao,oferta_laboral_dao,postulante_dao,empleador_dao)
