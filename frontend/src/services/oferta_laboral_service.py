from typing import List, Literal

import flet as ft

from frontend.src.services.api_service import ApiService


class OfertaLaboralService:
    """Service de Oferta Laboral"""

    @staticmethod
    async def buscar_ofertas_laborales(
        page: ft.Page,
        busqueda: str | None = None,
        rubro: str | None = None,
        jornada: Literal[
            "COMPLETA",
            "MEDIA_JORNADA",
            "TEMPORAL",
            "A_CONVENIR"
        ] | None = None,
        dias_laborales: List[str] | None = None,
        offset: int = 0
    ):
        """Metodo para buscar ofertas laborales"""

        params = {
            "busqueda": busqueda,
            "rubro": rubro,
            "jornada": jornada,
            "dias_laborales": dias_laborales,
            "offset": offset
        }

        return await ApiService.get(
            page=page,
            endpoint="/oferta-laboral/buscar-ofertas-laborales",
            params=params
        )

    @staticmethod
    async def obtener_oferta_laboral(
        page: ft.Page,
        oferta_laboral_id: int
    ):
        """Metodo para obtener el detalle de una oferta laboral por su id"""

        return await ApiService.get(
            page=page,
            endpoint=f"/oferta-laboral/{oferta_laboral_id}"
        )