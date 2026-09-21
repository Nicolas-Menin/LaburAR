from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.services.administrador_service import AdministradorService
from backend.app.repositories.administtrador_dao import AdministradorDAO
from backend.app.repositories.usuario_dao import UsuarioDAO
from backend.app.repositories.reporte_dao import ReporteDAO
from backend.app.dependencies.database import obtener_sesion_bd



def obtener_administrador_service(
    db: Session = Depends(obtener_sesion_bd)
):
    """Funcion para obtener el servicio de administrador"""

    addministrador_dao = AdministradorDAO(db)

    reporte_dao = ReporteDAO(db)

    usuario_dao = UsuarioDAO(db)

    return AdministradorService(
        administrador_dao=addministrador_dao,
        reporte_dao=reporte_dao,
        usuario_dao=usuario_dao
    )
