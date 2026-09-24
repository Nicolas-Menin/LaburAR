from typing import Literal
from frontend.src.services.api_service import ApiService



class AdministradorService:
    """Service de Administrador"""

    @staticmethod
    async def actualizar_reporte_estado(
        estado: Literal[
            "REVISADO",
            "PENDIENTE",
            "SANCIONADO"
        ],
        reporte_id: int
    ):
        """Metodo para actualizar el estado de un reporte"""

        datos = {
            "estado": estado,
            "reporte_id": reporte_id
        }


        return await ApiService.put(endpoint="/administrador/actualizar-reporte",datos=datos)


    @staticmethod
    async def buscar_reportes(

        busqueda: str | None = None,
        offset: int = 0
    ):
        """Metodo para que el administrador busque reportes"""

        params = {
            "busqueda": busqueda,
            "offset": offset
        }


        return await ApiService.get(endpoint="/administrador/buscar-reportes",params=params)


    @staticmethod
    async def buscar_usuarios(
        filtro: Literal[
            "POSTULANTE",
            "EMPLEADOR"
        ],
        busqueda: str | None = None,
        offset: int = 0
    ):
        """Metodo para que el administrador busque usuarios"""

        params = {
            "filtro": filtro,
            "busqueda": busqueda,
            "offset": offset
        }


        return await ApiService.get(endpoint="/administrador/buscar-usuarios",params=params)

    @staticmethod
    async def desactivar_usuario(
        desactivar_usuario_id: int
    ):
        """Metodo para desactivar usuario"""

        datos = {"desactivar_usuario_id": desactivar_usuario_id}


        return await ApiService.put(endpoint="/administrador/desactivar-usuario",datos=datos)

    @staticmethod
    async def banear_usuario(
        banear_usuario_id: int
    ):
        """Metodo para desactivar usuario"""

        datos = {"banear_usuario_id": banear_usuario_id}


        return await ApiService.put(endpoint="/administrador/banear-usuario",datos=datos)
