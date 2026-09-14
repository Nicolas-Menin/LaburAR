from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.services.empleador_service import EmpleadorService
from backend.app.repositories.empleador_dao import EmpleadorDAO
from backend.app.services.cloudinary_service import CloudinaryService
from backend.app.dependencies.postulacion import obtener_postulacion_service
from backend.app.repositories.oferta_laboral_dao import OfertaLaboralDAO
from backend.app.dependencies.database import obtener_sesion_bd

def obtener_empleador_service(
    db: Session = Depends(obtener_sesion_bd)
):
    """Funcion para obtener el service del empleador"""

    empleador_dao = EmpleadorDAO(db)

    cloudinary_service = CloudinaryService()

    postulacion_service = obtener_postulacion_service(db)

    oferta_laboral_dao = OfertaLaboralDAO(db)


    return EmpleadorService(
        empleador_dao= empleador_dao,
        cloudinary_service= cloudinary_service,
        postulacion_service= postulacion_service,
        oferta_laboral_dao= oferta_laboral_dao
    )
