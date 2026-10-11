import flet as ft

from frontend.src.services.api_service import ApiService


class MensajeService:
    """Service de Mensaje"""

    @staticmethod
    async def listar_mensajes(
        page: ft.Page,
        conversacion_id: int
    ):
        """Metodo para listar mensajes de conversacion"""

        return await ApiService.get(
            page=page,
            endpoint=f"/mensajes/listar-mensajes/{conversacion_id}"
        )

    @staticmethod
    async def actualizar_estado_mensajes(
        page: ft.Page,
        conversacion_id: int,
    ):
        """Metodo para actualizar el estado de mensajes"""

        datos = {
            "conversacion_id": conversacion_id
        }

        return await ApiService.put(
            page=page,
            endpoint="/mensajes/actualizar-estado-mensajes",
            datos=datos
        )

    @staticmethod
    async def verificar_mensajes_no_leidos(page: ft.Page):
        """Metodo para verificar si tiene mensajes no leidos"""

        return await ApiService.get(
            page=page,
            endpoint="/mensajes/mensajes-no-leidos"
        )