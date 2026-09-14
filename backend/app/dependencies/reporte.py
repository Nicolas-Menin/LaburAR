from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.services.reporte_service import ReporteService
from backend.app.repositories.reporte_dao import ReporteDAO
from backend.app.dependencies.database import obtener_sesion_bd

def obtener_reporte_service(
    db: Session = Depends(obtener_sesion_bd)
):
    """Funcion para obtener el service de reporte"""

    reporte_dao = ReporteDAO(db)

    return ReporteService(reporte_dao)