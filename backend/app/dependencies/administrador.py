from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.services.administrador_service import AdministradorService
from backend.app.repositories.administtrador_dao import AdministradorDAO
from backend.app.dependencies.reporte import obtener_reporte_service
from backend.app.dependencies.database import obtener_sesion_bd



def obtener_administrador_service(
    db: Session = Depends(obtener_sesion_bd)
):
    """Funcion para obtener el servicio de administrador"""

    addministrador_dao = AdministradorDAO(db)

    reporte_service = obtener_reporte_service(db)


    return AdministradorService(
        administrador_dao=addministrador_dao,
        reporte_service=reporte_service
    )
