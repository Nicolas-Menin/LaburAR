import asyncio
from datetime import datetime

import flet as ft

from frontend.src.services.postulante_service import PostulanteService
from frontend.src.excepciones.api_excepciones import (
    ErrorAutenticacion,
    ErrorNoEncontrado,
    ErrorServidor,
)

# pylint: disable=E1121,E1123,E0401,E1101


class SolicitudesView(ft.View):

    ESTADOS = {
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

    ANCHO_CONTENIDO = 760
    TAMANO_PAGINA = 10

    def __init__(self, perfil_empleador):
        super().__init__()

        self.perfil_empleador = perfil_empleador

        self.solicitudes = []
        self.busqueda_actual = None
        self.offset = 0

        self.route = "/solicitudes"
        self.padding = 0
        self.spacing = 0
        self.expand = True
        self.bgcolor = ft.Colors.BLUE_GREY_50

        self.bg_image = ft.Image(
            src="images/LaburAR_bg3.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )


        self.campo_busqueda = ft.TextField(
            label="Buscar solicitud",
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
                        "SOLICITUDES DE CONTACTO",
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

        self.lista_solicitudes = ft.Column(
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.boton_ver_mas = ft.OutlinedButton(
            content=ft.Text(
                "VER MÁS",
                color=ft.Colors.BLUE_500,
            ),
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
                self.lista_solicitudes,
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

    def cambiar_estado_boton(
        self,
        boton,
        texto_original,
        cargando,
        color=ft.Colors.BLUE_500,
    ):
        """Metodo para mostrar el estado de carga de un boton"""

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

        self.page.update()

    async def cargar(self, page: ft.Page):
        """Metodo para cargar las solicitudes de contacto del postulante"""

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
        """Metodo para pedir las solicitudes al backend.

        reiniciar=True empieza de cero.
        reiniciar=False trae la pagina siguiente.
        """

        if reiniciar:
            self.offset = 0
            self.solicitudes = []

            self.lista_solicitudes.controls = [
                self.crear_indicador_carga()
            ]

            self.boton_ver_mas.visible = False

            page.update()

        try:
            resultados = (
                await PostulanteService.buscar_conexiones_laborales(
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
            self.mostrar_solicitudes()
            page.update()

            self.mostrar_mensaje(
                "No se pudieron cargar las solicitudes. "
                "Intente nuevamente"
            )
            return

        self.solicitudes.extend(resultados)
        self.offset += len(resultados)

        self.mostrar_solicitudes()

        self.boton_ver_mas.visible = (
            len(resultados) >= self.TAMANO_PAGINA
        )

        page.update()

    def mostrar_solicitudes(self):
        """Metodo para mostrar la lista de solicitudes"""

        if not self.solicitudes:
            self.lista_solicitudes.controls = [
                self.crear_mensaje_sin_solicitudes()
            ]
            return

        self.lista_solicitudes.controls = [
            self.crear_card_solicitud(solicitud)
            for solicitud in self.solicitudes
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

    def crear_mensaje_sin_solicitudes(self):
        """Metodo para mostrar que no hay solicitudes para mostrar"""

        return ft.Container(
            width=self.ANCHO_CONTENIDO,
            padding=40,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Icon(
                        ft.Icons.MARK_EMAIL_UNREAD_OUTLINED,
                        size=45,
                        color=ft.Colors.BLUE_GREY_300,
                    ),
                    ft.Text(
                        "No hay solicitudes de contacto",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                    ),
                    ft.Text(
                        "No se encontraron solicitudes para mostrar.",
                        size=13,
                        color=ft.Colors.BLACK_45,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    def crear_chip_estado(self, estado: str):
        """Metodo para crear el chip de estado de la solicitud"""

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
        """Metodo para formatear la fecha de solicitud"""

        if not fecha:
            return "Sin fecha"

        try:
            return datetime.fromisoformat(
                str(fecha).replace("Z", "+00:00")
            ).strftime("%d/%m/%Y")

        except ValueError:
            return str(fecha)

    @staticmethod
    def obtener_fecha(solicitud: dict):
        """Metodo para obtener la fecha de la solicitud"""

        return (
            solicitud.get("fecha_solicitud")
            or solicitud.get("fecha_conexion")
            or solicitud.get("fecha_creacion")
        )

    def crear_botones_solicitud(self, solicitud: dict):
        """Metodo para crear los botones de accion de una solicitud"""

        boton_ver_perfil = ft.OutlinedButton(
            content=ft.Text(
                "VER PERFIL DE NEGOCIO",
                color=ft.Colors.BLUE_500,
            ),
            data=solicitud,
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
            on_click=self.ver_perfil_empleador,
        )

        botones = [
            boton_ver_perfil,
        ]

        if solicitud.get("estado") == "PENDIENTE":
            boton_aceptar = ft.Button(
                content=ft.Text(
                    "ACEPTAR CONTACTO",
                    color=ft.Colors.WHITE,
                ),
                data=solicitud,
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_500,
                    shape=ft.RoundedRectangleBorder(
                        radius=10,
                    ),
                ),
                on_click=self.confirmar_aceptar,
            )

            boton_rechazar = ft.OutlinedButton(
                content=ft.Text(
                    "RECHAZAR",
                    color=ft.Colors.RED_500,
                ),
                data=solicitud,
                style=ft.ButtonStyle(
                    color=ft.Colors.RED_500,
                    side=ft.BorderSide(
                        1.5,
                        ft.Colors.RED_500,
                    ),
                    shape=ft.RoundedRectangleBorder(
                        radius=10,
                    ),
                ),
                on_click=self.confirmar_rechazar,
            )

            botones.extend(
                [
                    boton_aceptar,
                    boton_rechazar,
                ]
            )

        return ft.Row(
            spacing=10,
            run_spacing=10,
            wrap=True,
            controls=botones,
        )

    def crear_card_solicitud(self, solicitud: dict):
        """Metodo para crear una card de solicitud de contacto"""

        avatar = ft.CircleAvatar(
            radius=30,
            bgcolor=ft.Colors.BLUE_GREY_100,
            content=ft.Icon(
                ft.Icons.BUSINESS,
                size=26,
                color=ft.Colors.BLUE_GREY_400,
            ),
        )

        foto = solicitud.get("foto_perfil_empleador")

        if foto:
            avatar.foreground_image_src = foto
            avatar.content = None

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
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=15,
                controls=[
                    avatar,
                    ft.Column(
                        expand=True,
                        spacing=6,
                        controls=[
                            ft.Text(
                                "Te han solicitado para el puesto de "
                                f"{solicitud.get('nombre_oferta', '')}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK_87,
                                font_family="Inter-Bold",
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                solicitud.get(
                                    "nombre_empleador",
                                    "Sin negocio",
                                ),
                                size=13,
                                color=ft.Colors.BLACK_54,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            self.crear_botones_solicitud(solicitud),
                        ],
                    ),
                    ft.Column(
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        controls=[
                            self.crear_chip_estado(
                                solicitud.get("estado")
                            ),
                            ft.Text(
                                "Solicitado el "
                                f"{self.formatear_fecha(self.obtener_fecha(solicitud))}",
                                size=12,
                                color=ft.Colors.BLACK_54,
                            ),
                        ],
                    ),
                ],
            ),
        )

    async def buscar(self, e):
        """Metodo para buscar solicitudes por el texto ingresado"""

        texto = (self.campo_busqueda.value or "").strip()

        self.busqueda_actual = texto or None

        await self.consultar(
            page=self.page,
            reiniciar=True,
        )

        self.update()

    async def ver_mas(self, e):
        """Metodo para traer la pagina siguiente de solicitudes"""

        boton = e.control

        self.cambiar_estado_boton(
            boton=boton,
            texto_original="VER MÁS",
            cargando=True,
        )

        try:
            await self.consultar(
                page=self.page,
                reiniciar=False,
            )

        except Exception:
            self.cambiar_estado_boton(
                boton=boton,
                texto_original="VER MÁS",
                cargando=False,
            )
            raise

        if self.boton_ver_mas.visible:
            self.cambiar_estado_boton(
                boton=boton,
                texto_original="VER MÁS",
                cargando=False,
            )

        self.update()

    async def ver_perfil_empleador(self, e):
        """Metodo para navegar al perfil del empleador"""

        boton = e.control
        solicitud = boton.data

        self.cambiar_estado_boton(
            boton=boton,
            texto_original="VER PERFIL DE NEGOCIO",
            cargando=True,
        )

        try:
            await self.perfil_empleador.cargar(
                page=self.page,
                empleador_id=solicitud["empleador_id"],
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
                texto_original="VER PERFIL DE NEGOCIO",
                cargando=False,
            )

    def confirmar_aceptar(self, e):
        """Metodo para mostrar la confirmacion de aceptar"""

        self.mostrar_confirmacion(
            solicitud=e.control.data,
            estado="ACEPTADA",
        )

    def confirmar_rechazar(self, e):
        """Metodo para mostrar la confirmacion de rechazar"""

        self.mostrar_confirmacion(
            solicitud=e.control.data,
            estado="RECHAZADA",
        )

    def mostrar_confirmacion(
        self,
        solicitud: dict,
        estado: str,
    ):
        """Metodo para confirmar la respuesta a una solicitud"""

        nombre_empleador = solicitud.get(
            "nombre_empleador",
            "el empleador",
        )

        nombre_oferta = solicitud.get(
            "nombre_oferta",
            "",
        )

        if estado == "ACEPTADA":
            titulo = "Aceptar solicitud de contacto"
            accion = "aceptando"
            texto_boton = "ACEPTAR"
            color_boton = ft.Colors.BLUE_500
            color_texto = ft.Colors.WHITE
            fondo_boton = ft.Colors.BLUE_500

        else:
            titulo = "Rechazar solicitud de contacto"
            accion = "rechazando"
            texto_boton = "RECHAZAR"
            color_boton = ft.Colors.RED_500
            color_texto = ft.Colors.RED_500
            fondo_boton = ft.Colors.WHITE

        async def confirmar(e):
            boton = e.control

            boton.disabled = True

            boton.content = ft.Container(
                width=130,
                alignment=ft.Alignment.CENTER,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        ft.ProgressRing(
                            width=14,
                            height=14,
                            stroke_width=2,
                            color=color_boton,
                        ),
                        ft.Text(
                            "CARGANDO...",
                            size=12,
                            color=color_boton,
                            no_wrap=True,
                        ),
                    ],
                ),
            )

            self.page.update()

            await self.responder_solicitud(
                solicitud=solicitud,
                estado=estado,
            )

        boton_confirmar = ft.Button(
            width=140,
            height=40,
            content=ft.Container(
                width=140,
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    texto_boton,
                    color=color_texto,
                    size=13,
                ),
            ),
            on_click=confirmar,
            style=ft.ButtonStyle(
                color=color_texto,
                bgcolor=fondo_boton,
                shape=ft.RoundedRectangleBorder(
                    radius=10,
                ),
                side=ft.BorderSide(
                    1.5,
                    color_boton,
                ),
            ),
        )

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    titulo,
                    color=ft.Colors.BLACK,
                ),
                content=ft.Text(
                    f"Estarías {accion} la solicitud de contacto de "
                    f"{nombre_empleador} para la oferta "
                    f"{nombre_oferta}. ¿Estás seguro?",
                    color=ft.Colors.BLACK,
                ),
                actions=[
                    ft.TextButton(
                        "CANCELAR",
                        on_click=lambda e: self.page.pop_dialog(),
                    ),
                    boton_confirmar,
                ],
            )
        )

    async def responder_solicitud(
        self,
        solicitud: dict,
        estado: str,
    ):
        """Metodo para aceptar o rechazar una solicitud"""

        try:
            await PostulanteService.actualizar_conexion_laboral(
                page=self.page,
                conexion_laboral_id=solicitud["id"],
                estado=estado,
            )

            self.page.pop_dialog()

            solicitud["estado"] = estado

            self.mostrar_solicitudes()

            self.update()

            self.mostrar_mensaje(
                "Contacto aceptado correctamente"
                if estado == "ACEPTADA"
                else "Solicitud rechazada correctamente"
            )

        except ErrorAutenticacion:
            self.page.pop_dialog()
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await self.page.push_route("/login")

        except ErrorNoEncontrado:
            self.page.pop_dialog()
            self.mostrar_mensaje(
                "No se encontró la solicitud de contacto"
            )

        except ErrorServidor:
            self.page.pop_dialog()
            self.mostrar_mensaje(
                "No se pudo responder la solicitud. Intente nuevamente"
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