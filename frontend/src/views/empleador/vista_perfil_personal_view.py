import asyncio

import flet as ft

from frontend.src.services.empleador_service import EmpleadorService
from frontend.src.services.autenticacion_service import AutenticacionService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
)
from frontend.src.session.sesion import Sesion

# pylint: disable=E1121,E1123,E0401,E1101


class PerfilPersonalEmpleadorView(ft.View):

    def __init__(
        self,
        editar_perfil,
        gestion_solicitudes,
        postulaciones,
        ofertas,
        vista_previa_perfil,
    ):
        """Método constructor de la vista de perfil personal del empleador."""

        super().__init__()

        self.route = "/perfil-personal-empleador"
        self.bgcolor = ft.Colors.BLUE_GREY_50
        self.padding = 0
        self.spacing = 0

        self.empleador_id = None

        self.editar_perfil = editar_perfil
        self.gestion_solicitudes = gestion_solicitudes
        self.gestion_postulaciones = postulaciones
        self.gestion_ofertas = ofertas
        self.vista_previa_perfil = vista_previa_perfil

        self.bg_image = ft.Image(
            src="images/LaburAR_bg3.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.cargando_perfil = False
        self.cargando_edicion = False
        self.cargando_mensajeria = False
        self.cargando_vista_previa = False
        self.cargando_ofertas = False
        self.cargando_postulantes = False
        self.cargando_solicitudes = False
        self.cargando_cierre_sesion = False
        self.cargando_desactivacion = False

        self.foto_perfil = ft.CircleAvatar(
            radius=60,
            content=ft.Icon(
                ft.Icons.STOREFRONT_OUTLINED,
                size=50,
                color=ft.Colors.BLUE_900,
            ),
            bgcolor=ft.Colors.BLUE_50,
        )

        self.txt_nombre = ft.Text(
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
            text_align=ft.TextAlign.CENTER,
        )

        self.btn_editar_perfil = self._crear_boton_accion(
            icono=ft.Icons.EDIT_OUTLINED,
            color=ft.Colors.CYAN_600,
            tooltip="Editar perfil",
            on_click=self.ir_a_editar_perfil,
        )

        self.btn_mensajeria = self._crear_boton_accion(
            icono=ft.Icons.CHAT_BUBBLE_OUTLINE,
            color=ft.Colors.GREEN_600,
            tooltip="Chat",
            on_click=self.ir_a_mensajeria,
        )

        self.btn_vista_previa = self._crear_boton_accion(
            icono=ft.Icons.VISIBILITY_OUTLINED,
            color=ft.Colors.BLUE_600,
            tooltip="Vista previa",
            on_click=self.ir_a_vista_previa_perfil,
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
            ],
        )

        self.btn_gestion_ofertas = self._crear_boton_accion(
            icono=ft.Icons.BUSINESS_CENTER_OUTLINED,
            color=ft.Colors.AMBER_600,
            tooltip="Mis ofertas",
            on_click=self.ir_a_gestion_ofertas,
        )

        self.btn_gestion_postulantes = self._crear_boton_accion(
            icono=ft.Icons.PEOPLE_OUTLINED,
            color=ft.Colors.PINK_600,
            tooltip="Postulantes",
            on_click=self.ir_a_gestion_postulantes,
        )

        self.btn_gestion_solicitudes = self._crear_boton_accion(
            icono=ft.Icons.CONTACT_MAIL_OUTLINED,
            color=ft.Colors.BROWN_600,
            tooltip="Solicitudes",
            on_click=self.ir_a_gestion_solicitudes,
        )

        self.fila_acciones_empleador = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=35,
            controls=[
                self._crear_accion_con_texto(
                    boton=self.btn_gestion_ofertas,
                    texto="Mis ofertas",
                ),
                self._crear_accion_con_texto(
                    boton=self.btn_gestion_postulantes,
                    texto="Postulantes",
                ),
                self._crear_accion_con_texto(
                    boton=self.btn_gestion_solicitudes,
                    texto="Solicitudes",
                ),
            ],
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

        self.btn_desactivar_cuenta = ft.OutlinedButton(
            "Desactivar cuenta",
            icon=ft.Icons.PERSON_OFF_OUTLINED,
            icon_color=ft.Colors.RED_600,
            style=ft.ButtonStyle(
                color=ft.Colors.RED_600,
                bgcolor=ft.Colors.with_opacity(
                    0.9,
                    ft.Colors.WHITE,
                ),
                side=ft.BorderSide(
                    1,
                    ft.Colors.RED_600,
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=10,
                ),
            ),
            on_click=self.desactivar_cuenta,
        )

        self.tarjeta_central = ft.Container(
            width=450,
            height=610,
            padding=40,
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.with_opacity(
                    0.12,
                    ft.Colors.BLACK,
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
                        height=1,
                    ),
                    self.fila_acciones_perfil,
                    self.fila_acciones_empleador,
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
                    ft.Container(
                        right=20,
                        bottom=20,
                        content=self.btn_desactivar_cuenta,
                    ),
                ],
            ),
        ]

    def _crear_boton_accion(
        self,
        icono,
        color,
        tooltip,
        on_click,
    ):
        """Crea un botón circular de acción."""

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
                    color,
                ),
                padding=ft.Padding(
                    15,
                    15,
                    15,
                    15,
                ),
            ),
            on_click=on_click,
        )

    @staticmethod
    def _crear_accion_con_texto(
        boton,
        texto,
    ):
        """Crea un botón acompañado de un texto descriptivo."""

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
        texto="Cargando...",
    ):
        """Crea el contenido visual para indicar una carga."""

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

    async def cargar(self, page):
        """Carga los datos del perfil del empleador."""

        if self.cargando_perfil:
            return

        self.cargando_perfil = True

        self.txt_nombre.value = "Cargando perfil..."

        page.update()

        try:

            datos = await EmpleadorService.perfil(page)

            self.empleador_id = datos["id"]

            self.mostrar_datos(datos)

            page.update()

        except ErrorAutenticacion:

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await page.push_route(
                "/login"
            )

        except ErrorServidor:

            self.mostrar_mensaje(
                "No se pudo cargar el perfil. Intente nuevamente."
            )

        finally:

            self.cargando_perfil = False

            page.update()

    def mostrar_datos(self, datos: dict):
        """Muestra los datos recibidos del empleador."""

        self.txt_nombre.value = datos.get(
            "nombre_negocio",
            "",
        )

        foto = datos.get("foto_perfil")

        if foto:

            self.foto_perfil.foreground_image_src = foto
            self.foto_perfil.content = None

        else:

            self.foto_perfil.foreground_image_src = None

            self.foto_perfil.content = ft.Icon(
                ft.Icons.STOREFRONT_OUTLINED,
                size=50,
                color=ft.Colors.BLUE_900,
            )

    async def ir_a_editar_perfil(self, e):
        """Navega a la vista de edición del perfil."""

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
                duration=2000,
            )
        )

        self.page.update()

        try:

            await self.page.push_route(
                "/editar-perfil-empleador"
            )

            await self.editar_perfil.cargar(
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

    async def ir_a_mensajeria(self, e):
        """Navega a la vista de mensajería."""

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
                duration=2000,
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
        """Navega a la vista previa del perfil."""

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
                duration=2000,
            )
        )

        self.page.update()

        try:

            await self.vista_previa_perfil.cargar(
                self.page,
                self.empleador_id,
            )

            await self.page.push_route(
                "/perfil-empleador"
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

    async def ir_a_gestion_ofertas(self, e):
        """Navega a la gestión de ofertas."""

        if self.cargando_ofertas:
            return

        self.cargando_ofertas = True

        boton = e.control
        boton.disabled = True

        self.page.show_dialog(
            ft.SnackBar(
                content=self._contenido_cargando(
                    "Cargando ofertas..."
                ),
                duration=2000,
            )
        )

        self.page.update()

        try:

            await self.page.push_route(
                "/gestion-ofertas"
            )

            await self.gestion_ofertas.cargar(
                self.page
            )

        except ErrorAutenticacion:

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        finally:

            self.cargando_ofertas = False

            boton.disabled = False

            if boton.page is not None:
                boton.page.update()

    async def ir_a_gestion_postulantes(self, e):
        """Navega a la gestión de postulantes."""

        if self.cargando_postulantes:
            return

        self.cargando_postulantes = True

        boton = e.control
        boton.disabled = True

        self.page.show_dialog(
            ft.SnackBar(
                content=self._contenido_cargando(
                    "Cargando postulantes..."
                ),
                duration=2000,
            )
        )

        self.page.update()

        try:

            await self.page.push_route(
                "/gestion-postulantes"
            )

            await self.gestion_postulaciones.cargar(
                self.page
            )

        except ErrorAutenticacion:

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        finally:

            self.cargando_postulantes = False

            boton.disabled = False

            if boton.page is not None:
                boton.page.update()

    async def ir_a_gestion_solicitudes(self, e):
        """Navega a la gestión de solicitudes."""

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
                duration=2000,
            )
        )

        self.page.update()

        try:

            await self.page.push_route(
                "/gestion-solicitudes"
            )

            await self.gestion_solicitudes.cargar(
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

            await Sesion.cerrar_async(self.page)

            await self.page.push_route(
                "/login"
            )

        finally:

            self.cargando_cierre_sesion = False

            self.btn_cerrar_sesion.disabled = False
            self.btn_cerrar_sesion.text = "Cerrar sesión"

            if self.btn_cerrar_sesion.page is not None:
                self.btn_cerrar_sesion.page.update()

    async def desactivar_cuenta(self, e):
        """Muestra el diálogo de confirmación para desactivar la cuenta."""

        if self.cargando_desactivacion:
            return

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    "Desactivar cuenta",
                    color=ft.Colors.BLACK_87,
                    weight=ft.FontWeight.BOLD,
                ),
                content=ft.Text(
                    "Si desactivás tu cuenta vas a cerrar sesión y "
                    "no vas a poder volver a ingresar. ¿Estás seguro "
                    "de que querés continuar?",
                    color=ft.Colors.BLACK_87,
                ),
                actions=[
                    ft.TextButton(
                        "Cancelar",
                        on_click=lambda e: self.page.pop_dialog(),
                    ),
                    ft.Button(
                        "Desactivar cuenta",
                        icon=ft.Icons.PERSON_OFF_OUTLINED,
                        icon_color=ft.Colors.RED_600,
                        color=ft.Colors.RED_600,
                        bgcolor=ft.Colors.RED_50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(
                                radius=8,
                            ),
                        ),
                        on_click=self.confirmar_desactivacion,
                    ),
                ],
            )
        )

        self.page.update()

    async def confirmar_desactivacion(self, e):
        """Desactiva definitivamente la cuenta del usuario logueado."""

        if self.cargando_desactivacion:
            return

        self.cargando_desactivacion = True

        self.page.pop_dialog()

        self.btn_desactivar_cuenta.disabled = True
        self.btn_desactivar_cuenta.content = self._contenido_cargando(
            "Desactivando cuenta..."
        )

        self.page.update()

        try:

            await AutenticacionService.desactivar_usuario(
                page=self.page
            )

            await Sesion.cerrar_async(self.page)

            await self.page.push_route(
                "/login"
            )

            self.mostrar_mensaje(
                "Tu cuenta fue desactivada"
            )

        except ErrorAutenticacion:

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except ErrorServidor:

            self.mostrar_mensaje(
                "No se pudo desactivar la cuenta. Intente nuevamente."
            )

        finally:

            self.cargando_desactivacion = False

            self.btn_desactivar_cuenta.disabled = False
            self.btn_desactivar_cuenta.content = ft.Text(
                "Desactivar cuenta",
                color=ft.Colors.RED_600,
            )

            if self.btn_desactivar_cuenta.page is not None:
                self.btn_desactivar_cuenta.page.update()

    async def volver(self, e):
        """Vuelve a la vista de búsqueda."""

        await self.page.push_route(
            "/busqueda"
        )

    def mostrar_mensaje(self, mensaje):
        """Muestra un mensaje mediante SnackBar."""

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    mensaje
                )
            )
        )

    def mostrar_dialogo_sesion_expirada(self):
        """Muestra un diálogo indicando que la sesión expiró."""

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