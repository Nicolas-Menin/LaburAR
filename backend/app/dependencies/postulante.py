from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.services.postulante_service import PostulanteService
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.estudio_dao import EstudiosDAO
from backend.app.repositories.experiencia_laboral_dao import ExperienciaLaboralDAO
from backend.app.repositories.habilidad_dao import HabilidadDAO
from backend.app.services.cloudinary_service  import CloudinaryService
from backend.app.dependencies.postulacion import obtener_postulacion_service
from backend.app.dependencies.database import obtener_sesion_bd

def obtener_postulante_service(
    db: Session = Depends(obtener_sesion_bd)
):
    """Funcion para obtener el servicio de postulante"""

    postulante_dao = PostulanteDAO(db)

    estudio_dao = EstudiosDAO(db)

    experiencia_laboral_dao = ExperienciaLaboralDAO(db)

    habilidad_dao = HabilidadDAO(db)

    cloudinary_service = CloudinaryService()

    postulacion_service = obtener_postulacion_service(db)

    return PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=habilidad_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service
    )
