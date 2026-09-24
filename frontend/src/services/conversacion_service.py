from frontend.src.services.api_service import ApiService



class ConversacionService:
    """Service de Conversacion"""

    @staticmethod
    async def traer_conversaciones_postulante():
        """Metodo para traer las conversaciones de postulante"""

        return await ApiService.get(endpoint="/conversacion/traer-conversacion-postulante")

    @staticmethod
    async def traer_conversaciones_empleador():
        """Metodo para traer las conversaciones de empleador"""

        return await ApiService.get(endpoint="/conversacion/traer-conversaciones-empleador")