from typing import Literal

import flet as ft

from frontend.src.services.api_service import ApiService


class AdministradorService:
    """Service de Administrador"""

    @staticmethod
    async def actualizar_reporte_estado(
        page: ft.Page,
        estado: Literal[
            "REVISADO",
            "SANCIONADO"
        ],
        reporte_id: int
    ):
        """Metodo para actualizar el estado de un reporte"""

        datos = {
            "estado": estado,
        }

        return await ApiService.put(
            page=page,
            endpoint=f"/administrador/actualizar-reporte?reporte_id={reporte_id}",
            datos=datos
        )

    @staticmethod
    async def obtener_postulante_usuario_id(
        page: ft.Page,
        usuario_id: int
    ):
        """Metodo para obtener postulante mediante su id usuario"""

        params = {"usuario_id": usuario_id}

        return await ApiService.get(
            page=page,
            endpoint="/administrador/obtener-postulante-usuario-id?",
            params=params
        )

    @staticmethod
    async def obtener_empleador_usuario_id(
        page: ft.Page,
        usuario_id: int
    ):
        """Metodo para obtener empleador mediante su id usuario"""

        params = {"usuario_id": usuario_id}

        return await ApiService.get(
            page=page,
            endpoint="/administrador/obtener-empleador-usuario-id",
            params=params
        )

    @staticmethod
    async def buscar_reportes(
        page: ft.Page,
        filtros:  Literal["REVISADO","PENDIENTE","SANCIONADO"],
        busqueda: str | None = None,
        offset: int = 0
    ):
        """Metodo para que el administrador busque reportes"""

        params = {
            "filtro": filtros,
            "busqueda": busqueda,
            "offset": offset
        }

        return await ApiService.get(
            page=page,
            endpoint="/administrador/buscar-reportes",
            params=params
        )

    @staticmethod
    async def buscar_usuarios(
        page: ft.Page,
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

        return await ApiService.get(
            page=page,
            endpoint="/administrador/buscar-usuarios",
            params=params
        )

    @staticmethod
    async def desactivar_usuario(
        page: ft.Page,
        desactivar_usuario_id: int
    ):
        """Metodo para desactivar usuario"""

        return await ApiService.put(
            page=page,
            endpoint=f"/administrador/desactivar-usuario?desactivar_usuario_id={desactivar_usuario_id}",
        )

    @staticmethod
    async def banear_usuario(
        page: ft.Page,
        banear_usuario_id: int
    ):
        """Metodo para desactivar usuario"""



        return await ApiService.put(
            page=page,
            endpoint=f"/administrador/banear-usuario?banear_usuario_id={banear_usuario_id}",
        )

    @staticmethod
    async def activar_usuario(
        page: ft.Page,
        activar_usuario_id: int
    ):
        """Metodo para activar usuario"""



        return await ApiService.put(
            page=page,
            endpoint=f"/administrador/activar-usuario?activar_usuario_id={activar_usuario_id}",
        )