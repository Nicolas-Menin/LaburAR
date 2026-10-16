import httpx
import flet as ft

from frontend.src.core.config import API_URL
from frontend.src.session.sesion import Sesion
from frontend.src.excepciones.api_excepciones import (
    ErrorAutenticacion,
    ErrorValidacion,
    ErrorNoEncontrado,
    ErrorServidor,
    ApiException,
)


class ApiService:
    """Service de API"""

    @staticmethod
    async def post(
        page: ft.Page,
        endpoint: str,
        datos: dict
    ):
        """Metodo para realizar solicitudes POST"""

        headers = await ApiService._obtener_headers(page)

        try:

            async with httpx.AsyncClient(timeout=31) as cliente:

                response = await cliente.post(
                    f"{API_URL}{endpoint}",
                    json=datos,
                    headers=headers
                )

            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as error:

            await ApiService._manejar_error(error)


        except httpx.TimeoutException as error:
            ApiService._manejar_timeout(error)

        except httpx.RequestError as error:
            raise ErrorServidor(
                "No se pudo establecer comunicación con el servidor."
                    ) from error



    @staticmethod
    async def put(
        page: ft.Page,
        endpoint: str,
        datos: dict | None = None
    ):
        """Metodo para realizar solicitudes PUT"""

        headers = await ApiService._obtener_headers(page)

        try:

            async with httpx.AsyncClient(timeout=31) as cliente:

                response = await cliente.put(
                    f"{API_URL}{endpoint}",
                    json=datos,
                    headers=headers
                    )

            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as error:

            await ApiService._manejar_error(error)

        except httpx.TimeoutException as error:
            ApiService._manejar_timeout(error)

        except httpx.RequestError as error:
            raise ErrorServidor(
                "No se pudo establecer comunicación con el servidor."
                    ) from error

    @staticmethod
    async def get(
        page: ft.Page,
        endpoint: str,
        params: dict | None = None
    ):
        """Metodo para realizar solicitudes GET"""

        params = {
            k: v
            for k, v in (params or {}).items()
            if v not in (None, "", [])
        }

        headers = await ApiService._obtener_headers(page)

        try:

            async with httpx.AsyncClient(timeout=31) as cliente:

                response = await cliente.get(
                    f"{API_URL}{endpoint}",
                    params=params,
                    headers=headers
                )

            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as error:
            await ApiService._manejar_error(error)

        except httpx.TimeoutException as error:
            ApiService._manejar_timeout(error)

        except httpx.RequestError as error:
            raise ErrorServidor(
                "No se pudo establecer comunicación con el servidor."
                    ) from error



    @staticmethod
    async def delete(
        page: ft.Page,
        endpoint: str,
        params: dict | None = None
    ):
        """Metodo para realizar solicitudes DELETE"""

        headers = await ApiService._obtener_headers(page)

        try:

            async with httpx.AsyncClient(timeout=31) as cliente:

                response = await cliente.delete(
                    f"{API_URL}{endpoint}",
                    params=params,
                    headers=headers
                )

            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as error:

            await ApiService._manejar_error(error)

        except httpx.TimeoutException as error:
            ApiService._manejar_timeout(error)

        except httpx.RequestError as error:
            raise ErrorServidor(
                "No se pudo establecer comunicación con el servidor."
                    ) from error


    @staticmethod
    async def _obtener_headers(page: ft.Page):
        """Metodo para obtener los headers de autenticacion"""

        token = Sesion.token(page)

        if token:

            if Sesion.token_vencido(page):
                Sesion.cerrar(page)
                raise ErrorAutenticacion("La sesion expiro")

            return {
                "Authorization": f"Bearer {token}"
            }

        return {}

    @staticmethod
    async def _manejar_error(error):
        status_code = error.response.status_code

        try:
            detalle = error.response.json().get("detail")
        except ValueError:
            detalle = error.response.text

        if status_code in (401, 403):
            raise ErrorAutenticacion(detalle)
        elif status_code == 422:
            raise ErrorValidacion(detalle)
        elif status_code == 404:
            raise ErrorNoEncontrado(detalle)
        elif status_code >= 500:
            raise ErrorServidor(detalle)
        else:
            raise ApiException(detalle)

    @staticmethod
    def _manejar_timeout(error):
        raise ErrorServidor(
            "El servidor tardó demasiado en responder. "
            "Intentá nuevamente."
        ) from error
