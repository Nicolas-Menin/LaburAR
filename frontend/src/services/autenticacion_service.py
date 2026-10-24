from datetime import datetime
import flet as ft

from frontend.src.services.api_service import ApiService
from frontend.src.session.sesion import Sesion


class AutenticacionService:
    """Service de Autenticacion"""

    @staticmethod
    async def registrar_postulante(
        page: ft.Page,
        email: str,
        contrasena: str,
        nombre: str,
        apellido: str,
        ubicacion: str
    ):
        """Metodo para registrar postulante"""

        datos = {
            "usuario": {
                "email": email,
                "password": contrasena
            },
            "postulante": {
                "nombre": nombre,
                "apellido": apellido,
                "ubicacion": ubicacion,
            }
        }

        return await ApiService.post(
            page,
            "/autenticacion/registrar-postulante",
            datos
        )

    @staticmethod
    async def registrar_empleador(
        page: ft.Page,
        email: str,
        contrasena: str,
        nombre_negocio: str,
        ubicacion: str,
        direccion: str
    ):
        """Metodo para registrar empleador"""

        datos = {
            "usuario": {
                "email": email,
                "password": contrasena
            },
            "empleador": {
                "nombre_negocio": nombre_negocio,
                "ubicacion": ubicacion,
                "direccion": direccion,
            }
        }

        return await ApiService.post(
            page,
            "/autenticacion/registrar-empleador",
            datos
        )

    @staticmethod
    async def iniciar_sesion(
        page: ft.Page,
        email: str,
        contrasena: str
    ):
        """Metodo para iniciar sesion en la app"""

        datos = {
            "email": email,
            "password": contrasena
        }

        response = await ApiService.post(
            page,
            "/autenticacion/login",
            datos
        )

        Sesion.iniciar(
            page=page,
            token=response["access_token"],
            rol=response["rol"],
            exp=datetime.fromisoformat(response["exp"]),
        )

        return response

    @staticmethod
    async def recuperar_contrasena(
        page: ft.Page,
        email: str,
    ):
        """Metodo para recuperar contraseña"""

        datos = {
            "email": email,
        }

        return await ApiService.post(
            page,
            "/autenticacion/resetear-contraseña",
            datos
        )

    @staticmethod
    async def restablecer_contrasena(
        page: ft.Page,
        token: str,
        nueva_contrasena: str
    ):
        """Método para restablecer la contraseña."""

        datos = {
            "nueva_contrasena": nueva_contrasena,
        }

        return await ApiService.put(
            page,
            f"/autenticacion/restablecer-contraseña?token={token}",
            datos
        )

    @staticmethod
    async def desactivar_usuario(
        page: ft.Page,
    ):
        """Metodo para que el usuario pueda desactivar su cuenta"""


        return await ApiService.put(
            page,
            endpoint="/autenticacion/desactivar-usuario"
        )