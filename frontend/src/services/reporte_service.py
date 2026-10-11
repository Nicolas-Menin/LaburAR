import flet as ft
from frontend.src.services.api_service import ApiService




class ReporteService:

    @staticmethod
    async def crear_reporte(
        page: ft.Page,
        usuario_reportado_id: int,
        motivo: str,
        descripcion: str
    ):
        """Metodo para reportar un usuario"""


        datos = {"motivo": motivo,
                 "descripcion": descripcion
                 }


        return await ApiService.post(page=page,
                                     endpoint=f"/reporte/crear-reporte?usuario_reportado_id={usuario_reportado_id}",
                                     datos=datos)