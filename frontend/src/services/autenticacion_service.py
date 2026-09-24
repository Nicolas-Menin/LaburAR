
from frontend.src.services.api_service import ApiService

from frontend.src.session.sesion import Sesion

class AutenticacionService:
    """Service de Autenticacion"""

    @staticmethod
    async def registrar_postulante(datos: dict):
        """Metodo para registrar postulante"""


        return await ApiService.post("/autenticacion/registrar-postulante",datos)

    @staticmethod
    async def registrar_empleador(datos: dict):
        """Metodo para registrar empleador"""


        return await ApiService.post("/autenticacion/registrar-empleador",datos)

    @staticmethod
    async def iniciar_sesion(datos: dict):
        """Metodo para iniciar sesion en la app"""


        response = await ApiService.post("/login/",datos)

        Sesion.token = response["access_token"]
        Sesion.rol = response["rol"]

        return response

    @staticmethod
    async def recuperar_contrasena(datos: dict):
        """Metodo para recuperar contraseña"""


        return await ApiService.post("autenticacion/resetear-contraseña",datos)