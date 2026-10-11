import flet as ft

from frontend.src.services.api_service import ApiService


class ConversacionService:
    """Service de Conversacion"""

    @staticmethod
    async def traer_conversaciones_postulante(page: ft.Page):
        """Metodo para traer las conversaciones de postulante"""

        return await ApiService.get(
            page=page,
            endpoint="/conversacion/traer-conversaciones-postulante"
        )

    @staticmethod
    async def traer_conversaciones_empleador(page: ft.Page,oferta_id:int | None = None):
        """Metodo para traer las conversaciones de empleador"""

        params = {"oferta_id": oferta_id}

        return await ApiService.get(
            page=page,
            endpoint="/conversacion/traer-conversaciones-empleador",
            params=params
        )