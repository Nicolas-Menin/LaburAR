import asyncio
import flet as ft

from frontend.src.services.administrador_service import AdministradorService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion
)
from frontend.src.session.sesion import Sesion

# pylint: disable=E1121,E1123,E0401,E1101


class PerfilPersonalAdministradorView(ft.View):

    def __init__(self, gestion_usuarios, gestion_reportes):
        super().__init__()

        self.route = "/perfil-personal-administrador"
        self.bgcolor = ft.Colors.BLUE_GREY_50
        self.padding = 0
        self.spacing = 0
        self.expand = True
        self.administrador_id = None

        self.gestion_usuarios = gestion_usuarios
        self.gestion_reportes = gestion_reportes

        self.cargando_cierre_sesion = False

        self.bg_image = ft.Image(
            src="images/LaburAR_bg3.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.foto_perfil = ft.CircleAvatar(
            radius=60,
            content=ft.Icon(
                ft.Icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                size=50,
                color=ft.Colors.BLUE_900
            ),
            bgcolor=ft.Colors.BLUE_50,
        )

        self.txt_nombre = ft.Text(
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
            font_family="Inter-Bold",
            text_align=ft.TextAlign.CENTER,
        )

        self.btn_gestion_usuarios = self._crear_boton_accion(
            icono=ft.Icons.PEOPLE_ALT_OUTLINED,
            color=ft.Colors.ORANGE_600,
            tooltip="Gestión de usuarios",
            on_click=self.ir_a_gestion_usuarios
        )

        self.btn_gestion_reportes = self._crear_boton_accion(
            icono=ft.Icons.REPORT_OUTLINED,
            color=ft.Colors.BLUE_600,
            tooltip="Gestión de reportes",
            on_click=self.ir_a_gestion_reportes
        )

        self.fila_acciones_administrador = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50,
            controls=[
                self._crear_accion_con_texto(
                    boton=self.btn_gestion_usuarios,
                    texto="Gestión de usuarios",
                ),
                self._crear_accion_con_texto(
                    boton=self.btn_gestion_reportes,
                    texto="Gestión de reportes",
                ),
            ]
        )

        self.btn_cerrar_sesion = ft.Button(
            "Cerrar sesión",
            icon=ft.Icons.LOGOUT,
            icon_color=ft.Colors.RED_600,
            color=ft.Colors.RED_600,
            bgcolor=ft.Colors.RED_50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=1,
            ),
            on_click=self.cerrar_sesion,
        )

        self.tarjeta_central = ft.Container(
            width=450,
            height=500,
            padding=40,
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
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
                spacing=25,
                controls=[
                    self.foto_perfil,

                    self.txt_nombre,

                    ft.Divider(
                        color=ft.Colors.BLUE_GREY_100,
                        height=1
                    ),

                    self.fila_acciones_administrador,

                    ft.Container(
                        height=5
                    ),

                    self.btn_cerrar_sesion,
                ],
            ),
        )

        self.controls = [
            ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        left=0,
                        top=0,
                        right=0,
                        bottom=0,
                        content=self.bg_image,
                    ),

                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                        content=self.tarjeta_central,
                    ),
                ],
            )
        ]

    async def ir_a_gestion_usuarios(self, e):
        """Método para navegar a la vista de gestión de usuarios."""

        await self.page.push_route("/gestion-usuarios")
        await self.gestion_usuarios.cargar(self.page)

    async def ir_a_gestion_reportes(self, e):
        """Método para navegar a la vista de gestión de reportes."""

        await self.page.push_route("/gestion-reportes")
        await self.gestion_reportes.cargar(self.page)

    async def cargar(self, page):
        """Método para cargar el perfil personal del administrador."""

        try:
            datos = await AdministradorService.perfil(page)

            self.administrador_id = datos.get("id")

            self.mostrar_datos(datos)

        except ErrorAutenticacion:

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except ErrorServidor:

            self.mostrar_mensaje(
                "No se pudo cargar el perfil. Intente nuevamente."
            )

    def mostrar_datos(self, datos: dict):
        """Método para mostrar los datos del perfil."""

        self.txt_nombre.value = datos.get(
            "nombre_completo",
            "Administrador"
        )

        foto = datos.get("foto_perfil")

        if foto:
            self.foto_perfil.foreground_image_src = foto

    def _crear_boton_accion(
        self,
        icono,
        color,
        tooltip,
        on_click
    ):
        """Método auxiliar para generar botones circulares de acción uniformes."""

        return ft.IconButton(
            icon=icono,
            icon_color=color,
            icon_size=28,
            bgcolor=ft.Colors.WHITE,
            tooltip=tooltip,
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                elevation=2,
                shadow_color=ft.Colors.BLACK_12,
                side=ft.BorderSide(
                    1,
                    color
                ),
                padding=ft.Padding(
                    15,
                    15,
                    15,
                    15
                )
            ),
            on_click=on_click
        )

    def _crear_accion_con_texto(
        self,
        boton,
        texto
    ):
        """Método auxiliar para mostrar un botón con su texto descriptivo."""

        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                boton,

                ft.Text(
                    texto,
                    size=13,
                    color=ft.Colors.BLUE_GREY_700,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        )

    async def cerrar_sesion(self, e):
        """Muestra el diálogo de confirmación para cerrar sesión."""

        if self.cargando_cierre_sesion:
            return

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,

                title=ft.Text(
                    "Cerrar sesión",
                    color=ft.Colors.BLACK_87,
                    weight=ft.FontWeight.BOLD,
                ),

                content=ft.Text(
                    "¿Estás seguro de que querés cerrar sesión?",
                    color=ft.Colors.BLACK_87,
                ),

                actions=[
                    ft.TextButton(
                        "Cancelar",
                        on_click=lambda e: self.page.pop_dialog(),
                    ),

                    ft.Button(
                        "Cerrar sesión",
                        icon=ft.Icons.LOGOUT,
                        icon_color=ft.Colors.RED_600,
                        color=ft.Colors.RED_600,
                        bgcolor=ft.Colors.RED_50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(
                                radius=8
                            ),
                        ),
                        on_click=self.confirmar_cierre_sesion,
                    ),
                ],
            )
        )

        self.page.update()

    async def confirmar_cierre_sesion(self, e):
        """Cierra definitivamente la sesión."""

        if self.cargando_cierre_sesion:
            return

        self.cargando_cierre_sesion = True

        self.page.pop_dialog()

        self.btn_cerrar_sesion.disabled = True
        self.btn_cerrar_sesion.text = "Cerrando sesión..."

        self.page.update()

        try:
            Sesion.cerrar(self.page)

            await self.page.push_route("/login")

        finally:
            self.cargando_cierre_sesion = False

            self.btn_cerrar_sesion.disabled = False
            self.btn_cerrar_sesion.text = "Cerrar sesión"

            if self.btn_cerrar_sesion.page is not None:
                self.btn_cerrar_sesion.page.update()

    async def volver(self, e):
        """Método para volver atrás."""

        if len(self.page.views) > 1:

            self.page.views.pop()

            top_view = self.page.views[-1]

            self.page.go(top_view.route)

        else:

            self.page.go("/")

    def mostrar_mensaje(self, mensaje):
        """Método para mostrar mensajes de error."""

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje)
            )
        )

    def mostrar_dialogo_sesion_expirada(self):
        """Método para mostrar el diálogo de sesión expirada."""

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,

                title=ft.Text(
                    "Sesión expirada"
                ),

                content=ft.Text(
                    "Tu sesión expiró. Iniciá sesión nuevamente."
                ),

                actions=[
                    ft.TextButton(
                        "Aceptar",
                        on_click=lambda e: (
                            self.page.pop_dialog()
                        )
                    )
                ],
            )
        )