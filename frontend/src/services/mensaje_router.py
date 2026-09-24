from frontend.src.services.api_service import ApiService




class MensajeService:
    """Service de Mensaje"""

    @staticmethod
    async def listar_mensajes(
        conversacion_id: int
    ):
        """Metodo para listar mensajes de conversacion"""

        return await ApiService.get(endpoint=f"/mensajes/listar-mensajes/{conversacion_id}")

    @staticmethod
    async def actualizar_estado_mensajes(
        conversacion_id: int,
    ):
        """Metodo para actualizar el estado de mensajes"""

        datos = {"conversacion_id": conversacion_id}


        return await ApiService.put("/mensajes/actualizar-estado-mensajes",datos=datos)



    @staticmethod
    async def verificar_mensajes_no_leidos():
        """Metodo para verificar si tiene mensajes no leidos"""

        return await ApiService.get(endpoint="/mensajes/mensajes-no-leidos")