import asyncio
from datetime import datetime

import flet as ft

from frontend.src.services.empleador_service import EmpleadorService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
    ErrorNoEncontrado,
)

# pylint: disable=E1121,E1123,E0401,E1101


class GestionOfertasView(ft.View):

    def __init__(self, vista_previa_oferta):
        super().__init__()

        self.vista_previa_oferta = vista_previa_oferta

        self.route = "/gestion-ofertas"
        self.padding = 0
        self.spacing = 0
        self.bgcolor = ft.Colors.BLUE_GREY_50

        self.bg_image = ft.Image(
            src="images/LaburAR_bg3.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.ofertas = []
        self.cargando = False
        self.navegando = False
        self.consulta_actual = ""

        self.ESTADOS_OFERTA = {
            "ACTIVA": (
                "Activa",
                ft.Colors.GREEN_600,
                ft.Colors.GREEN_50,
            ),
            "PAUSADA": (
                "Pausada",
                ft.Colors.BLUE_500,
                ft.Colors.BLUE_50,
            ),
            "CERRADA": (
                "Cerrada",
                ft.Colors.RED_500,
                ft.Colors.RED_50,
            ),
        }

        self.btn_volver = ft.IconButton(
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

        self.titulo = ft.Text(
            "GESTIÓN DE OFERTAS DE TRABAJO",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK_87,
            text_align=ft.TextAlign.CENTER,
            font_family="Inter-Bold",
        )

        self.txt_busqueda = ft.TextField(
            hint_text="Buscar oferta de trabajo",
            expand=True,
            height=50,
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
            on_submit=self.buscar,
        )

        self.btn_buscar = ft.Button(
            "BUSCAR",
            width=120,
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(
                    radius=15,
                ),
            ),
            on_click=self.buscar,
        )

        self.barra_busqueda = ft.Row(
            width=730,
            spacing=10,
            controls=[
                self.txt_busqueda,
                self.btn_buscar,
            ],
        )

        self.encabezado = ft.Container(
            width=760,
            padding=25,
            border_radius=20,
            bgcolor=ft.Colors.WHITE,
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
                spacing=20,
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                controls=[
                    self.titulo,
                    self.barra_busqueda,
                ],
            ),
        )

        self.lista_ofertas = ft.Column(
            width=760,
            spacing=15,
            horizontal_alignment=(
                ft.CrossAxisAlignment.STRETCH
            ),
        )

        self.indicador_carga = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ProgressRing(
                    width=32,
                    height=32,
                    stroke_width=3,
                    color=ft.Colors.BLUE_500,
                ),
            ],
        )

        self.contenido = ft.Column(
            width=760,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.encabezado,
                self.lista_ofertas,
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
                            top=10,
                            right=20,
                            bottom=30,
                        ),
                        content=ft.Column(
                            spacing=0,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.START,
                                    controls=[
                                        self.btn_volver,
                                    ],
                                ),
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
                ],
            )
        ]

    async def cargar(self, page):
        """Método para la carga inicial de la vista."""

        self.consulta_actual = ""
        self.txt_busqueda.value = ""

        await self.cargar_resultados(page)

    async def buscar(self, e):
        """Método para realizar una búsqueda."""

        if self.cargando:
            return

        self.consulta_actual = (
            self.txt_busqueda.value
        )

        await self.cargar_resultados(self.page)

    async def cargar_resultados(self, page):
        """Método para traer las ofertas laborales."""

        self.cargando = True

        self.lista_ofertas.controls = [
            self.indicador_carga
        ]

        self.update()

        try:
            resultados = (
                await EmpleadorService.filtrar_ofertas_laborales(
                    page,
                    busqueda=(
                        self.consulta_actual or None
                    ),
                )
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

            self.cargando = False

            return False

        except ErrorServidor:
            self.lista_ofertas.controls = [
                ft.Container(
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No se pudieron cargar las "
                        "ofertas. Intentá nuevamente",
                        color=ft.Colors.BLACK_54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]

            self.update()

            self.cargando = False

            return False

        self.ofertas = resultados or []

        self.mostrar_ofertas()

        self.cargando = False

        return True

    def mostrar_ofertas(self):
        """Método para mostrar las ofertas."""

        if not self.ofertas:
            self.lista_ofertas.controls = [
                ft.Container(
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No se encontraron ofertas de trabajo",
                        color=ft.Colors.BLACK_54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]

        else:
            self.lista_ofertas.controls = [
                self._tarjeta_oferta(oferta)
                for oferta in self.ofertas
            ]

        self.update()

    @staticmethod
    def _formatear_fecha(valor):
        """Método para formatear la fecha."""

        if not valor:
            return ""

        try:
            return datetime.fromisoformat(
                str(valor)
            ).strftime("%d/%m/%Y")

        except ValueError:
            return str(valor)

    def _tarjeta_oferta(
        self,
        oferta: dict,
    ):
        """Método para armar una card de oferta."""

        titulo_oferta = oferta.get(
            "titulo",
            "",
        )

        foto = oferta.get(
            "foto_perfil_empleador"
        )

        fecha = self._formatear_fecha(
            oferta.get(
                "fecha_creacion"
            )
        )

        estado = oferta.get(
            "estado"
        )

        (
            texto_estado,
            color_estado,
            fondo_estado,
        ) = self.ESTADOS_OFERTA.get(
            estado,
            (
                estado or "—",
                ft.Colors.BLUE_GREY_400,
                ft.Colors.BLUE_GREY_50,
            ),
        )

        boton_vista_previa = ft.OutlinedButton(
            "VER VISTA PREVIA",
            data={
                "oferta": oferta,
                "texto": "VER VISTA PREVIA",
                "color": ft.Colors.BLUE_500,
            },
            on_click=self.ver_vista_previa,
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_500,
                side=ft.BorderSide(
                    1.5,
                    ft.Colors.BLUE_500,
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=12,
                ),
            ),
        )

        return ft.Container(
            width=760,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
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
                spacing=12,
                controls=[
                    ft.Row(
                        vertical_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        spacing=15,
                        controls=[
                            ft.CircleAvatar(
                                radius=32,
                                bgcolor=(
                                    ft.Colors.BLUE_GREY_100
                                ),
                                foreground_image_src=(
                                    foto
                                    if foto
                                    else None
                                ),
                                content=(
                                    None
                                    if foto
                                    else ft.Icon(
                                        ft.Icons.STOREFRONT,
                                        size=28,
                                        color=(
                                            ft.Colors
                                            .BLUE_GREY_400
                                        ),
                                    )
                                ),
                            ),
                            ft.Column(
                                expand=True,
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        titulo_oferta,
                                        size=16,
                                        weight=(
                                            ft.FontWeight.BOLD
                                        ),
                                        color=(
                                            ft.Colors.BLACK_87
                                        ),
                                    ),
                                ],
                            ),
                            ft.Column(
                                horizontal_alignment=(
                                    ft.CrossAxisAlignment.END
                                ),
                                spacing=8,
                                controls=[
                                    ft.Container(
                                        bgcolor=fondo_estado,
                                        border=ft.Border.all(
                                            1,
                                            color_estado,
                                        ),
                                        border_radius=20,
                                        padding=ft.Padding(
                                            left=12,
                                            top=5,
                                            right=12,
                                            bottom=5,
                                        ),
                                        content=ft.Text(
                                            texto_estado,
                                            size=12,
                                            color=color_estado,
                                            weight=(
                                                ft.FontWeight.W_500
                                            ),
                                        ),
                                    ),
                                    ft.Text(
                                        (
                                            "Creada el "
                                            f"{fecha}"
                                        ),
                                        size=11,
                                        color=(
                                            ft.Colors.BLACK_45
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            boton_vista_previa,
                        ],
                    ),
                ],
            ),
        )

    @staticmethod
    def _estado_boton(
        boton,
        cargando: bool,
        texto_original: str,
        color,
    ):
        """Cambia un botón entre normal y cargando."""

        boton.disabled = cargando

        if cargando:
            boton.content = ft.Row(
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
                        "CARGANDO...",
                        color=color,
                    ),
                ],
            )
        else:
            boton.content = ft.Text(
                texto_original,
                color=color,
            )

        try:
            boton.update()
        except RuntimeError:
            pass

    async def ver_vista_previa(self, e):
        """Carga la vista previa de la oferta y recién ahí navega."""

        if self.navegando:
            return

        boton = e.control
        datos = boton.data
        oferta = datos["oferta"]

        self.navegando = True

        self._estado_boton(
            boton,
            True,
            datos["texto"],
            datos["color"],
        )

        try:
            await self.vista_previa_oferta.cargar(
                self.page,
                oferta["id"],
            )

            await self.page.push_route(
                "/perfil-oferta"
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route("/login")

        except ErrorNoEncontrado:
            self.mostrar_mensaje(
                "No se encontró la oferta solicitada"
            )

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo cargar la vista previa. "
                "Intentá nuevamente"
            )

        finally:
            self.navegando = False

            self._estado_boton(
                boton,
                False,
                datos["texto"],
                datos["color"],
            )

    async def volver(self, e):
        """Método para volver al perfil personal."""

        await self.page.push_route(
            "/perfil-personal-empleador"
        )

    def mostrar_mensaje(self, mensaje):
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje)
            )
        )

    def mostrar_dialogo_sesion_expirada(self):
        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text(
                    "Sesión expirada"
                ),
                content=ft.Text(
                    "Tu sesión expiró. "
                    "Iniciá sesión nuevamente."
                ),
                actions=[
                    ft.TextButton(
                        "Aceptar",
                        on_click=(
                            lambda e:
                            self.page.pop_dialog()
                        ),
                    )
                ],
            )
        )