from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.dependencies.database import obtener_sesion_bd
from backend.app.repositories.usuario_dao import UsuarioDAO
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.empleador_dao import EmpleadorDAO
from backend.app.services.autenticacion_service import AutenticacionService
from backend.app.services.token_service import TokenService
from backend.app.services.brevo_service import BrevoService
from backend.app.core.config import client_brevo, sender
from backend.app.services.usuario_service import UsuarioService

def obtener_usuario_service(
    db: Session = Depends(obtener_sesion_bd)
):
    """Funcion para obtener el servicio de usuario"""


    usuario_dao = UsuarioDAO(db)

    postulante_dao = PostulanteDAO(db)

    empleador_dao = EmpleadorDAO(db)

    autenticacion_service = AutenticacionService()

    token_service = TokenService()

    brevo_service = BrevoService(client_brevo,sender)


    return UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )