import asyncio
import flet as ft

from frontend.src.services.postulante_service import PostulanteService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion
)
from frontend.src.session.sesion import Sesion

# pylint: disable=E1121,E1123,E0401,E1101


class PerfilPersonalPostulanteView(ft.View):

    def __init__(
        self,
        editar_perfil_personal,
        postulaciones,
        solicitudes,
        vista_previa_perfil,
    ):
        super().__init__()

        self.editar_perfil_personal = editar_perfil_personal
        self.postulaciones = postulaciones
        self.solicitudes = solicitudes
        self.vista_previa_perfil = vista_previa_perfil

        self.postulante_id = None
        self.route = "/perfil-personal-postulante"
        self.padding = 0
        self.spacing = 0
        self.expand = True
        self.bgcolor = ft.Colors.BLUE_GREY_50

        self.bg_image = ft.Image(
            src="images/LaburAR_bg3.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.cargando_perfil = False
        self.cargando_mensajeria = False
        self.cargando_vista_previa = False
        self.cargando_edicion = False
        self.cargando_postulaciones = False
        self.cargando_solicitudes = False
        self.cargando_cierre_sesion = False

        self.foto_perfil = ft.CircleAvatar(
            radius=60,
            content=ft.Icon(
                ft.Icons.PERSON_OUTLINE,
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

        self.btn_editar_perfil = self._crear_boton_accion(
            icono=ft.Icons.EDIT_OUTLINED,
            color=ft.Colors.CYAN_600,
            tooltip="Editar perfil",
            on_click=self.ir_a_editar_perfil
        )

        self.btn_mensajeria = self._crear_boton_accion(
            icono=ft.Icons.CHAT_BUBBLE_OUTLINE,
            color=ft.Colors.GREEN_600,
            tooltip="Chat",
            on_click=self.ir_a_mensajeria
        )

        self.btn_vista_previa = self._crear_boton_accion(
            icono=ft.Icons.VISIBILITY_OUTLINED,
            color=ft.Colors.BLUE_600,
            tooltip="Vista previa del perfil",
            on_click=self.ir_a_vista_previa_perfil
        )

        self.fila_acciones_perfil = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=35,
            controls=[
                self._crear_accion_con_texto(
                    boton=self.btn_editar_perfil,
                    texto="Editar perfil",
                ),
                self._crear_accion_con_texto(
                    boton=self.btn_mensajeria,
                    texto="Chat",
                ),
                self._crear_accion_con_texto(
                    boton=self.btn_vista_previa,
                    texto="Vista previa",
                ),
            ]
        )

        self.btn_postulaciones = self._crear_boton_accion(
            icono=ft.Icons.WORK_OUTLINED,
            color=ft.Colors.AMBER_600,
            tooltip="Postulaciones",
            on_click=self.ir_a_postulaciones
        )

        self.btn_solicitudes = self._crear_boton_accion(
            icono=ft.Icons.PENDING_ACTIONS_OUTLINED,
            color=ft.Colors.PINK_600,
            tooltip="Solicitudes pendientes",
            on_click=self.ir_a_solicitudes
        )

        self.fila_acciones_postulante = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50,
            controls=[
                self._crear_accion_con_texto(
                    boton=self.btn_postulaciones,
                    texto="Postulaciones",
                ),
                self._crear_accion_con_texto(
                    boton=self.btn_solicitudes,
                    texto="Solicitudes pendientes",
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
                shape=ft.RoundedRectangleBorder(
                    radius=10,
                ),
                elevation=1,
            ),
            on_click=self.cerrar_sesion,
        )

        self.tarjeta_central = ft.Container(
            width=450,
            height=610,
            padding=40,
            bgcolor=ft.Colors.with_opacity(
                0.95,
                ft.Colors.WHITE
            ),
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
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                spacing=25,
                controls=[
                    self.foto_perfil,
                    self.txt_nombre,
                    ft.Divider(
                        color=ft.Colors.BLUE_GREY_100,
                        height=1
                    ),
                    self.fila_acciones_perfil,
                    self.fila_acciones_postulante,
                    ft.Container(
                        height=5,
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
                shadow_color=ft.Colors.BLACK_87,
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

    @staticmethod
    def _crear_accion_con_texto(
        boton,
        texto,
    ):
        """Crea un botón con su descripción debajo."""

        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            controls=[
                boton,
                ft.Text(
                    texto,
                    size=12,
                    color=ft.Colors.BLACK_54,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        )

    @staticmethod
    def _contenido_cargando(
        texto="Cargando..."
    ):
        """Contenido visual para indicar que se está cargando."""

        return ft.Row(
            tight=True,
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ProgressRing(
                    width=16,
                    height=16,
                    stroke_width=2,
                    color=ft.Colors.BLUE_500,
                ),
                ft.Text(
                    texto,
                    color=ft.Colors.BLUE_500,
                    size=13,
                ),
            ],
        )

    def _mostrar_cargando(self, texto):
        """Muestra un mensaje general de carga en el nombre."""

        self.txt_nombre.value = texto
        self.txt_nombre.update()

    async def cargar(self, page):
        """Obtiene el perfil del postulante autenticado."""

        if self.cargando_perfil:
            return

        self.cargando_perfil = True

        self.txt_nombre.value = "Cargando perfil..."
        page.update()

        try:
            datos = await PostulanteService.perfil(page)

            self.postulante_id = datos["id"]

            self.mostrar_datos(datos)

            page.update()

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await page.push_route(
                "/login"
            )

            return None

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo cargar el perfil. Intente nuevamente."
            )

        finally:
            self.cargando_perfil = False

            page.update()

    def mostrar_datos(self, datos: dict):
        """Muestra los datos obtenidos del perfil."""

        nombre = datos.get("nombre", "")
        apellido = datos.get("apellido", "")

        self.txt_nombre.value = (
            f"{nombre} {apellido}"
        ).strip()

        foto = datos.get("foto_perfil")

        if foto:
            self.foto_perfil.foreground_image_src = foto
            self.foto_perfil.content = None

        else:
            self.foto_perfil.foreground_image_src = None
            self.foto_perfil.content = ft.Icon(
                ft.Icons.PERSON_OUTLINE,
                size=50,
                color=ft.Colors.BLUE_900
            )

    async def accion_en_desarrollo(self, e):
        """Manejador temporal para las acciones de los botones."""

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    f"Acción '{e.control.tooltip}' en desarrollo..."
                ),
                duration=2000
            )
        )

    async def ir_a_mensajeria(self, e):
        """Metodo para navegar a la vista de mensajeria."""

        if self.cargando_mensajeria:
            return

        self.cargando_mensajeria = True

        boton = e.control
        boton.disabled = True

        self.page.show_dialog(
            ft.SnackBar(
                content=self._contenido_cargando(
                    "Cargando chat..."
                ),
                duration=2000
            )
        )

        self.page.update()

        try:
            await self.page.push_route(
                "/mensajes"
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        finally:
            self.cargando_mensajeria = False

            boton.disabled = False

            if boton.page is not None:
                boton.page.update()

    async def ir_a_vista_previa_perfil(self, e):
        """Metodo para navegar a la vista previa de perfil."""

        if self.cargando_vista_previa:
            return

        self.cargando_vista_previa = True

        boton = e.control
        boton.disabled = True

        self.page.show_dialog(
            ft.SnackBar(
                content=self._contenido_cargando(
                    "Cargando perfil..."
                ),
                duration=2000
            )
        )

        self.page.update()

        try:
            await self.vista_previa_perfil.cargar(
                self.page,
                self.postulante_id
            )

            await self.page.push_route(
                "/perfil-postulante"
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        finally:
            self.cargando_vista_previa = False

            boton.disabled = False

            if boton.page is not None:
                boton.page.update()

    async def ir_a_editar_perfil(self, e):
        """Metodo para navegar a la vista de edicion de perfil."""

        if self.cargando_edicion:
            return

        self.cargando_edicion = True

        boton = e.control
        boton.disabled = True

        self.page.show_dialog(
            ft.SnackBar(
                content=self._contenido_cargando(
                    "Cargando edición..."
                ),
                duration=2000
            )
        )

        self.page.update()

        try:
            await self.page.push_route(
                "/editar-perfil-postulante"
            )

            await self.editar_perfil_personal.cargar(
                self.page
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        finally:
            self.cargando_edicion = False

            boton.disabled = False

            if boton.page is not None:
                boton.page.update()

    async def ir_a_postulaciones(self, e):
        """Metodo para navegar a la vista de postulaciones."""

        if self.cargando_postulaciones:
            return

        self.cargando_postulaciones = True

        boton = e.control
        boton.disabled = True

        self.page.show_dialog(
            ft.SnackBar(
                content=self._contenido_cargando(
                    "Cargando postulaciones..."
                ),
                duration=2000
            )
        )

        self.page.update()

        try:
            await self.page.push_route(
                "/postulaciones"
            )

            await self.postulaciones.cargar(
                self.page
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        finally:
            self.cargando_postulaciones = False

            boton.disabled = False

            if boton.page is not None:
                boton.page.update()

    async def ir_a_solicitudes(self, e):
        """Metodo para navegar a la vista de solicitudes de contacto."""

        if self.cargando_solicitudes:
            return

        self.cargando_solicitudes = True

        boton = e.control
        boton.disabled = True

        self.page.show_dialog(
            ft.SnackBar(
                content=self._contenido_cargando(
                    "Cargando solicitudes..."
                ),
                duration=2000
            )
        )

        self.page.update()

        try:
            await self.page.push_route(
                "/solicitudes"
            )

            await self.solicitudes.cargar(
                self.page
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        finally:
            self.cargando_solicitudes = False

            boton.disabled = False

            if boton.page is not None:
                boton.page.update()

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
                                radius=8,
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
            Sesion.cerrar(
                self.page
            )

            await self.page.push_route(
                "/login"
            )

        finally:
            self.cargando_cierre_sesion = False

            self.btn_cerrar_sesion.disabled = False
            self.btn_cerrar_sesion.text = "Cerrar sesión"

            if self.btn_cerrar_sesion.page is not None:
                self.btn_cerrar_sesion.page.update()

    async def volver(self, e):
        """Método para volver a la búsqueda."""

        await self.page.push_route(
            "/busqueda"
        )

    def mostrar_mensaje(self, mensaje):
        """Muestra un mensaje al usuario."""

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje)
            )
        )

    def mostrar_dialogo_sesion_expirada(self):
        """Metodo para mostrar el dialogo de sesion expirada."""

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