import asyncio
from datetime import datetime

import flet as ft

from frontend.src.services.postulante_service import PostulanteService
from frontend.src.excepciones.api_excepciones import (
    ErrorAutenticacion,
    ErrorNoEncontrado,
    ErrorServidor,
)

# pylint: disable=E1121,E1123,E0401, E1101


class PostulacionesView(ft.View):

    def __init__(self, perfil_empleador, perfil_oferta):
        """Metodo constructor de la vista de mis postulaciones"""

        super().__init__()

        self.perfil_empleador = perfil_empleador
        self.perfil_oferta = perfil_oferta

        self.postulaciones = []
        self.busqueda_actual = None
        self.offset = 0

        self.route = "/mis-postulaciones"
        self.padding = 0
        self.spacing = 0
        self.expand = True
        self.bgcolor = ft.Colors.BLUE_GREY_50

        self.bg_image = ft.Image(
            src="images/LaburAR_bg3.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.ESTADOS = {
            "ACEPTADA": (
                "ACEPTADA",
                ft.Colors.GREEN_700,
                ft.Colors.GREEN_50,
                ft.Colors.GREEN_200,
            ),
            "PENDIENTE": (
                "PENDIENTE",
                ft.Colors.BLUE_700,
                ft.Colors.BLUE_50,
                ft.Colors.BLUE_200,
            ),
            "RECHAZADA": (
                "RECHAZADA",
                ft.Colors.RED_700,
                ft.Colors.RED_50,
                ft.Colors.RED_200,
            ),
        }

        self.ANCHO_CONTENIDO = 760
        self.TAMANO_PAGINA = 10

        self.campo_busqueda = ft.TextField(
            label="Buscar postulación",
            hint_text="Nombre del empleo o del negocio",
            expand=True,
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
            on_submit=self.buscar,
        )

        self.boton_buscar = ft.Button(
            "BUSCAR",
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(
                    radius=15
                ),
            ),
            on_click=self.buscar,
        )

        self.tarjeta_encabezado = ft.Container(
            width=self.ANCHO_CONTENIDO,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            border_radius=20,
            padding=25,
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
                spacing=20,
                controls=[
                    ft.Text(
                        "MIS POSTULACIONES",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_87,
                        font_family="Inter-Bold",
                    ),
                    ft.Row(
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.campo_busqueda,
                            self.boton_buscar,
                        ],
                    ),
                ],
            ),
        )

        self.lista_postulaciones = ft.Column(
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.boton_ver_mas = ft.OutlinedButton(
            "VER MÁS",
            visible=False,
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_500,
                side=ft.BorderSide(
                    1.5,
                    ft.Colors.BLUE_500,
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=10,
                ),
            ),
            on_click=self.ver_mas,
        )

        self.contenido = ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
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
                    ],
                ),
                self.tarjeta_encabezado,
                self.lista_postulaciones,
                self.boton_ver_mas,
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
            ),
        ]

    async def cargar(self, page: ft.Page):
        """Metodo para cargar las postulaciones del postulante"""

        self.campo_busqueda.value = ""
        self.busqueda_actual = None

        await self.consultar(
            page=page,
            reiniciar=True,
        )

    async def consultar(
        self,
        page: ft.Page,
        reiniciar: bool,
    ):
        """Metodo para pedir las postulaciones al backend.

        reiniciar=True empieza de cero (carga inicial o nueva busqueda).
        reiniciar=False trae la pagina siguiente (VER MAS).
        """

        if reiniciar:
            self.offset = 0
            self.postulaciones = []

            self.lista_postulaciones.controls = [
                self.crear_indicador_carga()
            ]
            self.boton_ver_mas.visible = False

            page.update()

        try:
            resultados = (
                await PostulanteService.filtrar_postulaciones(
                    page=page,
                    busqueda=self.busqueda_actual,
                    offset=self.offset,
                )
            ) or []

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await page.push_route("/login")
            return

        except ErrorNoEncontrado:
            resultados = []

        except ErrorServidor:
            self.mostrar_postulaciones()
            page.update()

            self.mostrar_mensaje(
                "No se pudieron cargar las postulaciones. "
                "Intente nuevamente"
            )
            return

        self.postulaciones.extend(resultados)
        self.offset += len(resultados)

        self.mostrar_postulaciones()

        self.boton_ver_mas.visible = (
            len(resultados) >= self.TAMANO_PAGINA
        )

        page.update()

    def mostrar_postulaciones(self):
        """Metodo para mostrar la lista de postulaciones"""

        if not self.postulaciones:
            self.lista_postulaciones.controls = [
                self.crear_mensaje_sin_postulaciones()
            ]
            return

        self.lista_postulaciones.controls = [
            self.crear_card_postulacion(postulacion)
            for postulacion in self.postulaciones
        ]

    def crear_indicador_carga(self):
        """Metodo para mostrar un indicador mientras se cargan los datos"""

        return ft.Container(
            width=self.ANCHO_CONTENIDO,
            padding=40,
            alignment=ft.Alignment.CENTER,
            content=ft.ProgressRing(
                color=ft.Colors.BLUE_500,
            ),
        )

    def crear_mensaje_sin_postulaciones(self):
        """Metodo para mostrar que no hay postulaciones para mostrar"""

        return ft.Container(
            width=self.ANCHO_CONTENIDO,
            padding=40,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Icon(
                        ft.Icons.WORK_OFF,
                        size=45,
                        color=ft.Colors.BLUE_GREY_300,
                    ),
                    ft.Text(
                        "No hay postulaciones",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                    ),
                    ft.Text(
                        "No se encontraron postulaciones para mostrar.",
                        size=13,
                        color=ft.Colors.BLACK_45,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    def crear_chip_estado(self, estado: str):
        """Metodo para crear el chip de estado de la postulacion"""

        texto, color_texto, color_fondo, color_borde = self.ESTADOS.get(
            estado,
            (
                (estado or "SIN ESTADO").replace("_", " "),
                ft.Colors.BLUE_GREY_700,
                ft.Colors.BLUE_GREY_50,
                ft.Colors.BLUE_GREY_200,
            ),
        )

        return ft.Container(
            bgcolor=color_fondo,
            border=ft.Border.all(
                1,
                color_borde,
            ),
            border_radius=20,
            padding=ft.Padding(
                left=12,
                top=6,
                right=12,
                bottom=6,
            ),
            content=ft.Text(
                texto,
                color=color_texto,
                weight=ft.FontWeight.W_500,
                size=12,
            ),
        )

    @staticmethod
    def formatear_fecha(fecha) -> str:
        """Metodo para formatear la fecha de postulacion (dd/mm/aaaa)"""

        if not fecha:
            return "Sin fecha"

        try:
            return datetime.fromisoformat(
                str(fecha).replace("Z", "+00:00")
            ).strftime("%d/%m/%Y")

        except ValueError:
            return str(fecha)

    def crear_card_postulacion(self, postulacion: dict):
        """Metodo para crear una card de postulacion"""

        avatar = ft.CircleAvatar(
            radius=30,
            bgcolor=ft.Colors.BLUE_GREY_100,
            content=ft.Icon(
                ft.Icons.BUSINESS,
                size=26,
                color=ft.Colors.BLUE_GREY_400,
            ),
        )

        foto = postulacion.get("foto_empleador")

        if foto:
            avatar.foreground_image_src = foto
            avatar.content = None

        boton_ver_oferta = ft.OutlinedButton(
            content=ft.Text(
                "VER OFERTA",
                color=ft.Colors.BLUE_500,
            ),
            data=postulacion,
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_500,
                side=ft.BorderSide(
                    1.5,
                    ft.Colors.BLUE_500,
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=10,
                ),
            ),
            on_click=self.ver_oferta,
        )

        boton_ver_empleador = ft.TextButton(
            content=ft.Text(
                postulacion.get(
                    "nombre_empleador",
                    "Sin negocio",
                ),
                color=ft.Colors.BLUE_600,
            ),
            data=postulacion,
            tooltip="Ver perfil del empleador",
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_600,
                padding=ft.Padding(0, 0, 0, 0),
            ),
            on_click=self.ver_perfil_empleador,
        )

        return ft.Container(
            width=self.ANCHO_CONTENIDO,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
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
                    avatar,
                    ft.Column(
                        expand=True,
                        spacing=4,
                        controls=[
                            ft.Text(
                                postulacion.get(
                                    "titulo_oferta",
                                    "Sin título",
                                ),
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK_87,
                                font_family="Inter-Bold",
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            boton_ver_empleador,
                        ],
                    ),
                    ft.Column(
                        spacing=8,
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.END
                        ),
                        controls=[
                            self.crear_chip_estado(
                                postulacion.get("estado")
                            ),
                            ft.Text(
                                self.formatear_fecha(
                                    postulacion.get(
                                        "fecha_postulacion"
                                    )
                                ),
                                size=12,
                                color=ft.Colors.BLACK_54,
                            ),
                            boton_ver_oferta,
                        ],
                    ),
                ],
            ),
        )

    def cambiar_estado_boton(
        self,
        boton,
        texto_original,
        cargando,
    ):
        """Cambia el contenido del boton mientras se realiza una carga."""

        boton.disabled = cargando

        if cargando:
            boton.content = ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.ProgressRing(
                        width=16,
                        height=16,
                        stroke_width=2,
                        color=ft.Colors.BLUE_500,
                    ),
                    ft.Text(
                        "CARGANDO...",
                        color=ft.Colors.BLUE_500,
                    ),
                ],
            )

        else:
            boton.content = ft.Text(
                texto_original,
                color=ft.Colors.BLUE_500,
            )

        self.page.update()

    async def buscar(self, e):
        """Metodo para buscar postulaciones por el texto ingresado"""

        texto = (self.campo_busqueda.value or "").strip()

        self.busqueda_actual = texto or None

        await self.consultar(
            page=self.page,
            reiniciar=True,
        )

        self.update()

    async def ver_mas(self, e):
        """Metodo para traer la pagina siguiente de postulaciones"""

        await self.consultar(
            page=self.page,
            reiniciar=False,
        )

        self.update()

    async def ver_perfil_empleador(self, e):
        """Metodo para navegar al perfil del empleador de la postulacion"""

        boton = e.control
        postulacion = boton.data

        self.cambiar_estado_boton(
            boton=boton,
            texto_original=postulacion.get(
                "nombre_empleador",
                "Sin negocio",
            ),
            cargando=True,
        )

        try:
            await self.perfil_empleador.cargar(
                page=self.page,
                empleador_id=postulacion["empleador_id"],
            )

            await self.page.push_route(
                "/perfil-empleador"
            )

        except (
            ErrorAutenticacion,
            ErrorNoEncontrado,
            ErrorServidor,
        ):
            self.cambiar_estado_boton(
                boton=boton,
                texto_original=postulacion.get(
                    "nombre_empleador",
                    "Sin negocio",
                ),
                cargando=False,
            )

    async def ver_oferta(self, e):
        """Metodo para navegar a la oferta laboral de la postulacion"""

        boton = e.control
        postulacion = boton.data

        self.cambiar_estado_boton(
            boton=boton,
            texto_original="VER OFERTA",
            cargando=True,
        )

        try:
            await self.perfil_oferta.cargar(
                page=self.page,
                oferta_id=postulacion["oferta_id"],
            )

            await self.page.push_route(
                "/perfil-oferta"
            )

        except (
            ErrorAutenticacion,
            ErrorNoEncontrado,
            ErrorServidor,
        ):
            self.cambiar_estado_boton(
                boton=boton,
                texto_original="VER OFERTA",
                cargando=False,
            )

    async def volver(self, e):
        """Metodo para volver a la pantalla anterior"""

        await self.page.push_route(
            "/perfil-personal-postulante"
        )

    def mostrar_mensaje(self, mensaje):
        """Metodo para mostrar mensajes"""

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje)
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
                        on_click=lambda e: self.page.pop_dialog(),
                    ),
                ],
            )
        )