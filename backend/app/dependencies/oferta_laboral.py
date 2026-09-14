from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.services.oferta_laboral_service import OfertaLaboralService
from backend.app.repositories.oferta_laboral_dao import OfertaLaboralDAO
from backend.app.dependencies.database import obtener_sesion_bd


def obtener_oferta_laboral_service(
    db: Session = Depends(obtener_sesion_bd)
):
    """Funcion para obtener el service de oferta laboral"""

    oferta_laboral_service = OfertaLaboralDAO(db)


    return OfertaLaboralService(oferta_laboral_dao=oferta_laboral_service)