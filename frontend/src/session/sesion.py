import base64
import json
from datetime import datetime, timezone
import flet as ft



class Sesion:
    """Clase que almacena el estado de la sesion, aislado por cliente conectado"""

    @staticmethod
    def iniciar(
        page: ft.Page,
        token: str,
        rol: str,
        exp: datetime
    ):
        """Metodo para guardar los datos de la sesion recien iniciada"""

        page.session.store.set(
            "token",
            token
        )

        page.session.store.set(
            "rol",
            rol
        )

        page.session.store.set(
            "exp",
            exp.isoformat()
        )

    @staticmethod
    def token(page: ft.Page):
        """Metodo para obtener el token del cliente actual"""


        return page.session.store.get("token")

    @staticmethod
    def rol(page: ft.Page):
        """Metodo para obtener el rol del cliente actual"""

        return page.session.store.get("rol")

    @staticmethod
    def exp(page: ft.Page):
        """Metodo para obtener la fecha de expiracion del cliente actual"""

        valor = page.session.store.get("exp")

        if not valor:
            return None

        return datetime.fromisoformat(valor)

    @staticmethod
    def token_vencido(page: ft.Page) -> bool:
        """Metodo para verificar si el token del cliente actual ya vencio"""

        exp = Sesion.exp(page)

        if exp is None:
            return True

        return datetime.now(timezone.utc) >= exp

    @staticmethod
    def cerrar(page: ft.Page):
        """Metodo para cerrar la sesion del cliente actual"""

        if page.session.store.get("token") is not None:
            page.session.store.remove("token")

        if page.session.store.get("rol") is not None:
            page.session.store.remove("rol")

        if page.session.store.get("exp") is not None:
            page.session.store.remove("exp")

    @staticmethod
    def obtener_usuario_id(page: ft.Page):
        """Metodo para leer el id del usuario desde el payload del token, sin verificar firma"""

        token = Sesion.token(page)

        if not token:
            return None

        try:

            payload_codificado = token.split(".")[1]

            relleno = "=" * (-len(payload_codificado) % 4)

            payload_bytes = base64.urlsafe_b64decode(
                payload_codificado + relleno
            )

            payload = json.loads(payload_bytes)

        except (IndexError, ValueError):
            return None

        return payload.get("user")