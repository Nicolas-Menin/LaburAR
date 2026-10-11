import asyncio
import flet as ft
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
    ErrorNoEncontrado,
)
from frontend.src.services.reporte_service import ReporteService

# pylint: disable=E1121,E1123,E0401,E1101

class ReporteView(ft.View):

    def __init__(self, usuario_reportado_id: int):

        super().__init__()

        self.route = "/reporte"
        self.padding = 0
        self.spacing = 0
        self.usuario_reportado_id = usuario_reportado_id

        self.bg_image = ft.Image(
            src="images/LaburAR_bg1.png",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.txt_encabezado = ft.Text(
            "REPORTE",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
            font_family="Inter-Bold",
            text_align=ft.TextAlign.CENTER,
        )

        self.txt_explicativo = ft.Text(
            "Describí el problema o la irregularidad detectada. "
            "El reporte será enviado directamente al administrador.",
            size=13,
            color=ft.Colors.BLACK_54,
            text_align=ft.TextAlign.CENTER,
        )

        self.txt_titulo = ft.TextField(
            label="Título del reporte",
            hint_text="Ej. Error al cargar perfil / Usuario sospechoso",
            prefix_icon=ft.Icons.TITLE_OUTLINED,
            color=ft.Colors.BLACK,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            focused_border_color=ft.Colors.BLUE_500,
        )

        self.txt_descripcion = ft.TextField(
            label="Descripción",
            hint_text="Detallá los motivos o el inconveniente sucedido...",
            color=ft.Colors.BLACK,
            multiline=True,
            height=130,
            prefix_icon=ft.Icons.DESCRIPTION_OUTLINED,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            focused_border_color=ft.Colors.BLUE_500,
        )

        self.btn_enviar = ft.FilledButton(
            "ENVIAR REPORTE",
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(
                    left=20,
                    top=15,
                    right=20,
                    bottom=15
                ),
            ),
            width=360,
            on_click=self.enviar_reporte,
        )

        self.tarjeta_central = ft.Container(
            width=450,
            height=500,
            padding=30,
            bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.WHITE),
            border_radius=15,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.with_opacity(
                    0.12,
                    ft.Colors.BLACK
                ),
                offset=ft.Offset(0, 8),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=18,
                controls=[
                    ft.Icon(
                        ft.Icons.REPORT_PROBLEM_OUTLINED,
                        size=48,
                        color=ft.Colors.AMBER_700,
                    ),
                    self.txt_encabezado,
                    self.txt_explicativo,
                    self.txt_titulo,
                    self.txt_descripcion,
                    ft.Container(height=5),
                    self.btn_enviar,
                ],
            ),
        )

        self.controls = [
            ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        content=self.bg_image,
                    ),
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                        content=self.tarjeta_central,
                    ),
                    ft.Container(
                        top=20,
                        left=20,
                        content=ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_size=24,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_500,
                            style=ft.ButtonStyle(
                                shape=ft.CircleBorder(),
                                elevation=4,
                                shadow_color=ft.Colors.BLACK,
                            ),
                            tooltip="Volver",
                            on_click=self.volver,
                        ),
                    ),
                ],
            )
        ]

    async def enviar_reporte(self, e):
        """Método para procesar el envío del reporte al administrador."""

        motivo = (self.txt_titulo.value or "").strip()
        descripcion = (self.txt_descripcion.value or "").strip()

        if not motivo:
            self.mostrar_mensaje(
                "Por favor, ingresá un motivo para el reporte"
            )
            return

        if not descripcion:
            self.mostrar_mensaje(
                "Por favor, ingresá la descripción del reporte"
            )
            return

        self.btn_enviar.disabled = True
        self.page.update()

        try:
            await ReporteService.crear_reporte(
                page=self.page,
                usuario_reportado_id=self.usuario_reportado_id,
                motivo=motivo,
                descripcion=descripcion
            )

            self.mostrar_mensaje(
                "Reporte enviado con éxito al administrador"
            )

            await asyncio.sleep(1.5)
            await self.page.push_route("/busqueda")

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await self.page.push_route("/login")

        except ErrorServidor:
            self.mostrar_mensaje(
                "Error en el servidor. Intente más tarde"
            )

        except ErrorNoEncontrado:
            self.mostrar_mensaje(
                "Ocurrió un error inesperado al enviar el reporte"
            )

        finally:
            self.btn_enviar.disabled = False
            self.page.update()

    async def volver(self, e):
        """Método para volver a la pantalla anterior."""

        await self.page.push_route("/busqueda")

    def mostrar_mensaje(self, mensaje: str):
        """Método auxiliar para mostrar notificaciones SnackBar."""

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje)
            )
        )

    def mostrar_dialogo_sesion_expirada(self):

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,

                title=ft.Text(
                    "Sesión expirada",
                    color=ft.Colors.BLACK_87,
                ),

                content=ft.Text(
                    "Tu sesión expiró. "
                    "Iniciá sesión nuevamente.",
                    color=ft.Colors.BLACK_87,
                ),

                actions=[
                    ft.TextButton(
                        "Aceptar",
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_500,
                        ),
                        on_click=lambda e:
                        self.page.pop_dialog(),
                    )
                ],
            )
        )
