from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from backend.app.repositories.usuario_dao import UsuarioDAO
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.empleador_dao import EmpleadorDAO
from backend.app.models.usuario import Usuario
from backend.app.models.postulante import Postulante
from backend.app.models.empleador import Empleador
from backend.app.schemas.postulante_schemas import RegistroPostulante
from backend.app.schemas.empleador_schemas import RegistroEmpleador
from backend.app.services.autenticacion_service import AutenticacionService
from backend.app.services.token_service import TokenService
from backend.app.services.brevo_service import BrevoService

class UsuarioService:
    """Service de usuario"""

    def __init__(self,
                usuario_dao: UsuarioDAO,
                postulante_dao: PostulanteDAO,
                empleador_dao: EmpleadorDAO,
                autenticacion_service: AutenticacionService,
                token_service: TokenService,
                brevo_service: BrevoService
        ):

        self.usuario_dao = usuario_dao
        self.postulante_dao = postulante_dao
        self.empleador_dao = empleador_dao
        self.autenticacion_service = autenticacion_service
        self.token_service = token_service
        self.brevo_service = brevo_service

    def registrar_postulante(self, datos: RegistroPostulante):
        """Metodo para regisrar usuario postulante"""

        if self.usuario_dao.buscar_por_email(datos.usuario.email):
            raise HTTPException(409,"El email ya existe")

        password_hash = self.autenticacion_service.password_hash(datos.usuario.password)

        usuario = Usuario(
            email=datos.usuario.email,
            password_hash = password_hash,
            rol = "POSTULANTE"
        )

        self.usuario_dao.crear_usuario(usuario)

        postulante= Postulante(
            usuario_id = usuario.id,
            nombre = datos.postulante.nombre,
            apellido = datos.postulante.apellido,
            ubicacion = datos.postulante.ubicacion,
            descripcion_personal = datos.postulante.descripcion_personal
                    if datos.postulante.descripcion_personal else None,
            foto_perfil = datos.postulante.foto_perfil
                    if datos.postulante.foto_perfil else None,
            cv_url = datos.postulante.cv_url
                    if datos.postulante.cv_url else None,
            disponibilidad = datos.postulante.disponibilidad
                    if datos.postulante.disponibilidad else None
        )

        self.postulante_dao.crear_postulante(postulante)

        return postulante

    def registrar_empleador(self,datos: RegistroEmpleador):
        """Metodo para registrar usuario empleador"""


        if self.usuario_dao.buscar_por_email(datos.usuario.email):
            raise HTTPException(409,"El email ya existe")

        password_hash = self.autenticacion_service.password_hash(datos.usuario.password)


        usuario = Usuario(
            email =  datos.usuario.email,
            password_hash = password_hash,
            rol = "EMPLEADOR"
        )

        self.usuario_dao.crear_usuario(usuario)

        empleador = Empleador(
            usuario_id = usuario.id,
            nombre_negocio = datos.empleador.nombre_negocio,
            direccion = datos.empleador.direccion,
            ubicacion = datos.empleador.ubicacion,
            descripcion = datos.empleador.descripcion
                    if datos.empleador.descripcion else None,
            rubro = datos.empleador.rubro
                    if datos.empleador.rubro else None,
            foto_perfil = datos.empleador.foto_perfil
                    if datos.empleador.foto_perfil else None
        )

        self.empleador_dao.crear_empleador(empleador)

        return empleador


    def iniciar_sesion(self,email: str, password: str):
        """Metodo para iniciar sesion"""

        usuario = self.usuario_dao.buscar_por_email(email)


        if not usuario:
            raise HTTPException(401,"Credenciales invalidas")


        password_verification = self.autenticacion_service.verify_password(
                password,usuario.password_hash)


        if not password_verification:
            raise HTTPException(401,"Credenciales invalidas")


        payload = {
            "user": usuario.id,
        }

        token = self.token_service.crear_token(payload)

        return {
            "access_token": token,
            "token_type": "bearer",
            "rol": usuario.rol
        }

    def recuperacion_contrasena(self,email: str):
        """Metodo para recuperar contraseña de usuario"""

        usuario = self.usuario_dao.buscar_por_email(email)

        if not usuario:
            raise HTTPException(404,"Usuario no encontrado")

        payload = {
            "sub": usuario.id,
            "type": "password_reset",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
        }

        token = self.token_service.crear_token(payload)

        return self.brevo_service.enviar_email_recuperacion_contrasena(email,token)

