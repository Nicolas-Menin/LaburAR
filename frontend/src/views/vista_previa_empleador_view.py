import asyncio
import math
import flet as ft
from frontend.src.services.empleador_service import EmpleadorService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion
)

from frontend.src.session.sesion import Sesion

# pylint: disable=E1121,E1123,E0401,E1101


class PerfilEmpleadorView(ft.View):
    ALTO_MINIMO = 110

    def __init__(self, perfil_oferta):
        super().__init__()
        self.perfil_oferta = perfil_oferta
        self.usuario_reportado_id = None
        self.navegando = False
        self.route = "/perfil-empleador"
        self.padding = 0
        self.spacing = 0
        self.expand = True
        self.bgcolor = ft.Colors.BLUE_GREY_50
        self.bg_image = ft.Image(
            src="images/LaburAR_bg6.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )
        self.avatar = ft.CircleAvatar(
            radius=35,
            bgcolor=ft.Colors.BLUE_GREY_100,
            content=ft.Icon(
                ft.Icons.BUSINESS,
                size=30,
                color=ft.Colors.BLUE_GREY_400
            ),
        )
        self.txt_nombre = ft.Text(
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK_87,
            font_family="Inter-Bold"
        )
        self.txt_ubicacion = ft.Text(
            size=13,
            color=ft.Colors.BLACK_54
        )
        self.txt_direccion = ft.Text(
            size=13,
            color=ft.Colors.BLACK_45
        )
        self.tarjeta_encabezado = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.with_opacity(
                    0.10,
                    ft.Colors.BLACK,
                ),
                offset=ft.Offset(0, 10),
            ),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    self.avatar,
                    ft.Column(
                        spacing=5,
                        controls=[
                            self.txt_nombre,
                            ft.Row(
                                spacing=10,
                                controls=[
                                    self.txt_ubicacion,
                                    self.txt_direccion
                                ]
                            ),
                        ]
                    ),
                ]
            )
        )
        self.txt_descripcion = ft.Text(
            color=ft.Colors.BLACK_87
        )
        self.tarjeta_descripcion = ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=15,
            padding=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.with_opacity(
                    0.10,
                    ft.Colors.BLACK,
                ),
                offset=ft.Offset(0, 10),
            ),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(
                        "SOBRE EL NEGOCIO",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12
                    ),
                    self.txt_descripcion,
                ]
            )
        )
        self.txt_rubro = ft.Text(
            color=ft.Colors.BLUE_900,
            weight=ft.FontWeight.W_500,
            size=13
        )
        self.tarjeta_rubro = ft.Container(
            width=180,
            height=self.ALTO_MINIMO,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=15,
            padding=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.with_opacity(
                    0.10,
                    ft.Colors.BLACK,
                ),
                offset=ft.Offset(0, 10),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Text(
                        "RUBRO",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12
                    ),
                    ft.Container(
                        bgcolor=ft.Colors.BLUE_50,
                        border=ft.Border.all(
                            1,
                            ft.Colors.BLUE_200
                        ),
                        border_radius=20,
                        padding=ft.Padding(
                            left=12,
                            top=6,
                            right=12,
                            bottom=6
                        ),
                        content=self.txt_rubro,
                    ),
                ]
            )
        )
        self.lista_ofertas = ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        )
        self.tarjeta_ofertas = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=15,
            padding=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.with_opacity(
                    0.10,
                    ft.Colors.BLACK,
                ),
                offset=ft.Offset(0, 10),
            ),
            content=ft.Column(
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Text(
                        "OFERTAS DE TRABAJO",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12
                    ),
                    self.lista_ofertas,
                ]
            )
        )
        self.boton_volver = ft.IconButton(
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
        )
        self.boton_reportar = ft.OutlinedButton(
            "REPORTAR",
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_500,
                side=ft.BorderSide(
                    1.5,
                    ft.Colors.BLUE_500
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=10
                )
            ),
            on_click=self.reportar,
        )
        self.overlay_carga = ft.Container(
            left=0,
            top=0,
            right=0,
            bottom=0,
            visible=False,
            alignment=ft.Alignment.TOP_CENTER,
            padding=ft.Padding(
                left=0,
                top=160,
                right=0,
                bottom=0
            ),
            bgcolor=ft.Colors.with_opacity(
                0.7,
                ft.Colors.BLUE_GREY_50
            ),
            content=ft.ProgressRing(
                width=40,
                height=40,
                stroke_width=4,
                color=ft.Colors.BLUE_500,
            ),
        )
        self.contenido = ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.tarjeta_encabezado,
                ft.Row(
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        self.tarjeta_descripcion,
                        self.tarjeta_rubro
                    ]
                ),
                self.tarjeta_ofertas,
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        self.boton_reportar
                    ]
                ),
            ],
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
                        left=0,
                        top=0,
                        right=0,
                        bottom=0,
                        padding=ft.Padding(
                            left=10,
                            top=70,
                            right=20,
                            bottom=30,
                        ),
                        content=ft.Column(
                            spacing=0,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    alignment=ft.Alignment.TOP_CENTER,
                                    content=ft.Column(
                                        horizontal_alignment=(
                                            ft.CrossAxisAlignment.CENTER
                                        ),
                                        scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            self.contenido,
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        left=10,
                        top=10,
                        content=self.boton_volver,
                    ),
                    self.overlay_carga,
                ],
            ),
        ]

    def _mostrar_carga(self, visible: bool):
        """Muestra u oculta el indicador de carga del perfil."""
        self.overlay_carga.visible = visible
        try:
            self.update()
        except RuntimeError:
            pass

    @staticmethod

    def _contenido_cargando(texto: str, color):
        """Spinner con texto para mostrar dentro de un botón."""
        return ft.Row(
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.ProgressRing(
                    width=16,
                    height=16,
                    stroke_width=2,
                    color=color,
                ),
                ft.Text(
                    texto,
                    color=color,
                ),
            ]
        )

    def _estado_boton_reportar(self, cargando: bool):
        """Cambia el botón REPORTAR entre normal y cargando."""
        self.boton_reportar.disabled = cargando
        if cargando:
            self.boton_reportar.content = self._contenido_cargando(
                "CARGANDO...",
                ft.Colors.BLUE_500,
            )
        else:
            self.boton_reportar.content = ft.Text(
                "REPORTAR",
                color=ft.Colors.BLUE_500,
            )
        try:
            self.boton_reportar.update()
        except RuntimeError:
            pass

    def _estado_cards_ofertas(self, card, cargando: bool):
        """Muestra el spinner en la oferta tocada y bloquea las demás."""
        indicador = getattr(card, "_indicador", None)
        flecha = getattr(card, "_flecha", None)
        if indicador:
            indicador.visible = cargando
        if flecha:
            flecha.visible = not cargando
        for item in self.lista_ofertas.controls:
            if isinstance(item, ft.Container):
                item.disabled = cargando
        try:
            self.lista_ofertas.update()
        except RuntimeError:
            pass

    async def cargar(
        self,
        page: ft.Page,
        empleador_id: int
    ):
        """Metodo para cargar el perfil del empleador por su id"""
        self._mostrar_carga(True)
        try:
            datos = await EmpleadorService.obtener_empleador(
                page=page,
                empleador_id=empleador_id
            )
            self.usuario_reportado_id = datos.get(
                "usuario_id"
            )
            self.mostrar_datos(datos)
        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await page.push_route("/login")
        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo cargar el perfil. Intente nuevamente"
            )
        finally:
            self._mostrar_carga(False)

    def mostrar_datos(self, datos: dict):
        """Metodo para mostrar los datos del empleador en pantalla"""
        self.txt_nombre.value = datos.get(
            "nombre_negocio",
            ""
        )
        self.txt_ubicacion.value = datos.get(
            "ubicacion",
            ""
        )
        self.txt_direccion.value = datos.get(
            "direccion",
            ""
        )
        self.txt_descripcion.value = (
            datos.get("descripcion")
            or "Sin descripción"
        )
        self.txt_rubro.value = datos.get(
            "rubro",
            ""
        )
        foto = datos.get("foto_perfil")
        if foto:
            self.avatar.foreground_image_src = foto
        ofertas = datos.get(
            "ofertas_laborales",
            []
        )
        if ofertas:
            self.lista_ofertas.controls = [
                self.crear_card_oferta(oferta)
                for oferta in ofertas
            ]
        else:
            self.lista_ofertas.controls = [
                ft.Text(
                    "Sin ofertas publicadas",
                    color=ft.Colors.BLACK_45
                )
            ]
        self._igualar_alturas()

    def _igualar_alturas(self):
        """Ajusta la altura de las tarjetas de descripción y rubro."""
        texto = self.txt_descripcion.value or ""
        lineas = sum(
            max(1, math.ceil(len(parte) / 100))
            for parte in texto.split("\n")
        )
        alto_descripcion = 57 + 20 * lineas
        self.tarjeta_descripcion.height = max(
            alto_descripcion,
            self.ALTO_MINIMO,
        )
        self.tarjeta_rubro.height = self.ALTO_MINIMO

    def crear_card_oferta(self, oferta: dict):
        """Metodo para crear una card de oferta laboral"""
        flecha = ft.Icon(
            ft.Icons.ARROW_FORWARD_IOS,
            size=16,
            color=ft.Colors.BLUE_GREY_400,
        )
        indicador = ft.Row(
            tight=True,
            spacing=8,
            visible=False,
            controls=[
                ft.ProgressRing(
                    width=16,
                    height=16,
                    stroke_width=2,
                    color=ft.Colors.BLUE_500,
                ),
                ft.Text(
                    "CARGANDO...",
                    size=12,
                    color=ft.Colors.BLUE_500,
                    weight=ft.FontWeight.W_500,
                ),
            ],
        )
        card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=12,
            padding=15,
            on_click=self.ver_oferta,
            data=oferta,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                oferta.get("titulo", ""),
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK_87,
                            ),
                            ft.Row(
                                tight=True,
                                controls=[
                                    indicador,
                                    flecha,
                                ],
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.Row(
                                spacing=5,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.LOCATION_ON_OUTLINED,
                                        size=16,
                                        color=ft.Colors.BLUE_GREY_500,
                                    ),
                                    ft.Text(
                                        oferta.get(
                                            "ubicacion",
                                            ""
                                        ),
                                        size=13,
                                        color=ft.Colors.BLACK_54,
                                    ),
                                ],
                            ),
                            ft.Row(
                                spacing=5,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.PIN_DROP_OUTLINED,
                                        size=16,
                                        color=ft.Colors.BLUE_GREY_500,
                                    ),
                                    ft.Text(
                                        oferta.get(
                                            "direccion",
                                            ""
                                        ),
                                        size=13,
                                        color=ft.Colors.BLACK_54,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Text(
                        oferta.get("descripcion")
                        or "Sin descripción",
                        size=13,
                        color=ft.Colors.BLACK_87,
                        max_lines=3,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
            ),
        )
        card._indicador = indicador
        card._flecha = flecha
        return card

    async def ver_oferta(self, e):
        """Metodo para navegar al perfil de una oferta publicada por el empleador"""
        if self.navegando:
            return
        card = e.control
        oferta = card.data
        self.navegando = True
        self._estado_cards_ofertas(card, True)
        try:
            await self.perfil_oferta.cargar(
                page=self.page,
                oferta_id=oferta["id"]
            )
            await self.page.push_route(
                "/perfil-oferta"
            )
        finally:
            self.navegando = False
            self._estado_cards_ofertas(card, False)

    async def volver(self, e):
        """Metodo para volver a la busqueda"""
        if self.navegando:
            return
        self.navegando = True
        self.boton_volver.disabled = True
        try:
            self.boton_volver.update()
        except RuntimeError:
            pass
        try:
            if Sesion.rol(self.page) == "ADMINISTRADOR":
                await self.page.push_route(
                    "/perfil-personal-administrador"
                )
            else:
                await self.page.push_route(
                    "/busqueda"
                )
        finally:
            self.navegando = False
            self.boton_volver.disabled = False
            try:
                self.boton_volver.update()
            except RuntimeError:
                pass

    async def reportar(self, e):
        """Metodo para reportar el negocio"""
        if self.navegando:
            return
        self.navegando = True
        self._estado_boton_reportar(True)
        try:
            await self.page.push_route(
                f"/reporte?usuario_reportado_id="
                f"{self.usuario_reportado_id}"
            )
        finally:
            self.navegando = False
            self._estado_boton_reportar(False)

    def mostrar_mensaje(self, mensaje):
        """Metodo para mostrar los mensajes de excepciones"""
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    mensaje
                )
            )
        )

    def mostrar_dialogo_sesion_expirada(self):
        """Metodo para mostrar el dialogo de sesion expirada"""
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
                        on_click=lambda e: self.page.pop_dialog()
                    )
                ],
            )
        )
