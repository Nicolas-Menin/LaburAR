import asyncio
import math
import flet as ft
from frontend.src.session.sesion import Sesion
from frontend.src.services.postulante_service import PostulanteService
from frontend.src.services.empleador_service import EmpleadorService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
    ErrorNoEncontrado,
)

# pylint: disable=E1121,E1123,E0401, E1101

class PerfilPostulanteView(ft.View):

    DISPONIBILIDADES = {
        "JORNADA_COMPLETA": "Jornada Completa",
        "MEDIA_JORNADA": "Media Jornada",
        "FINES_SEMANA": "Fines de Semana",
        "A_CONVENIR": "A Convenir",
    }
    ALTO_EXPERIENCIA_VACIA = 110

    def __init__(self):
        super().__init__()
        self.route = "/perfil-postulante"
        self.padding = 0
        self.spacing = 0
        self.expand = True
        self.bgcolor = ft.Colors.BLUE_GREY_50
        self.postulante_id = None
        self.usuario_reportado_id = None
        self.cv_url = None
        self.oferta_seleccionada = None
        self.cards_ofertas = []
        self.cargando_ofertas_contacto = False
        self.cargando_contacto = False
        self.bg_image = ft.Image(
            src="images/LaburAR_bg6.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )
        self.avatar = ft.CircleAvatar(
            radius=35,
            bgcolor=ft.Colors.BLUE_GREY_100,
            content=ft.Icon(
                ft.Icons.PERSON,
                size=30,
                color=ft.Colors.BLUE_GREY_400,
            ),
        )
        self.txt_nombre = ft.Text(
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK_87,
            font_family="Inter-Bold",
        )
        self.txt_ubicacion = ft.Text(
            size=13,
            color=ft.Colors.BLACK_54,
        )
        self.btn_ver_cv = ft.OutlinedButton(
            "VER CV",
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
            on_click=self.ver_cv,
        )
        self.btn_contactar = ft.OutlinedButton(
            "CONTACTAR",
            style=ft.ButtonStyle(
                color=ft.Colors.GREEN_600,
                side=ft.BorderSide(
                    1.5,
                    ft.Colors.GREEN_600,
                ),
                shape=ft.RoundedRectangleBorder(
                    radius=10,
                ),
            ),
            on_click=self.contactar,
        )
        self.tarjeta_encabezado = ft.Container(
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
                controls=[
                    ft.Row(
                        expand=True,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                        controls=[
                            self.avatar,
                            ft.Column(
                                spacing=5,
                                controls=[
                                    self.txt_nombre,
                                    self.txt_ubicacion,
                                ],
                            ),
                        ],
                    ),
                    ft.Column(
                        spacing=10,
                        controls=[
                            self.btn_ver_cv,
                            self.btn_contactar,
                        ],
                    ),
                ],
            ),
        )
        self.txt_descripcion = ft.Text(
            color=ft.Colors.BLACK_87,
        )
        self.tarjeta_descripcion = ft.Container(
            expand=True,
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
                spacing=10,
                controls=[
                    ft.Text(
                        "DESCRIPCIÓN GENERAL",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12,
                    ),
                    self.txt_descripcion,
                ],
            ),
        )
        self.lista_experiencias = ft.Column(
            spacing=10,
        )
        self.tarjeta_experiencia = ft.Container(
            padding=15,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            border_radius=15,
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
                        "EXPERIENCIA LABORAL",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12,
                    ),
                    self.lista_experiencias,
                ],
            ),
        )
        self.txt_disponibilidad = ft.Text(
            color=ft.Colors.BLUE_900,
            weight=ft.FontWeight.W_500,
            size=13,
        )
        self.tarjeta_disponibilidad = ft.Container(
            padding=25,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            border_radius=15,
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
                spacing=15,
                controls=[
                    ft.Text(
                        "DISPONIBILIDAD LABORAL",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12,
                    ),
                    ft.Container(
                        bgcolor=ft.Colors.BLUE_50,
                        border=ft.Border.all(
                            1,
                            ft.Colors.BLUE_200,
                        ),
                        border_radius=20,
                        padding=ft.Padding(
                            left=12,
                            top=6,
                            right=12,
                            bottom=6,
                        ),
                        content=self.txt_disponibilidad,
                    ),
                ],
            ),
        )
        self.fila_habilidades = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8,
        )
        self.tarjeta_habilidades = ft.Container(
            expand=True,
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
                spacing=10,
                controls=[
                    ft.Text(
                        "HABILIDADES",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12,
                    ),
                    self.fila_habilidades,
                ],
            ),
        )
        self.lista_estudios = ft.Column(
            spacing=10,
        )
        self.tarjeta_estudios = ft.Container(
            expand=True,
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
                spacing=10,
                controls=[
                    ft.Text(
                        "ESTUDIOS",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12,
                    ),
                    self.lista_estudios,
                ],
            ),
        )
        self.contenido = ft.Column(
            spacing=20,
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
                self.tarjeta_encabezado,
                ft.Row(
                    spacing=20,
                    vertical_alignment=(
                        ft.CrossAxisAlignment.START
                    ),
                    controls=[
                        self.tarjeta_descripcion,
                        ft.Column(
                            expand=True,
                            spacing=20,
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.STRETCH
                            ),
                            controls=[
                                self.tarjeta_disponibilidad,
                                self.tarjeta_experiencia,
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=20,
                    vertical_alignment=(
                        ft.CrossAxisAlignment.START
                    ),
                    controls=[
                        self.tarjeta_habilidades,
                        self.tarjeta_estudios,
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.OutlinedButton(
                            "REPORTAR",
                            style=ft.ButtonStyle(
                                color=ft.Colors.BLUE_500,
                                side=ft.BorderSide(
                                    1.5,
                                    ft.Colors.BLUE_500,
                                ),
                                shape=(
                                    ft.RoundedRectangleBorder(
                                        radius=10
                                    )
                                ),
                            ),
                            on_click=self.reportar,
                        ),
                    ],
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

    def _crear_card_estudio(self, estudio):
        """Metodo para crear una card de estudio."""
        titulo = (
            f"{estudio.get('titulo', '')} · "
            f"{estudio.get('institucion', '')}"
        )
        subtitulo = (
            f"{(estudio.get('nivel') or '').capitalize()}"
            f" · "
            f"{(estudio.get('estado') or '').replace('_', ' ')}"
        )
        return ft.Container(
            bgcolor=ft.Colors.BLUE_GREY_50,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            border_radius=10,
            padding=12,
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=34,
                        height=34,
                        border_radius=17,
                        bgcolor=ft.Colors.BLUE_100,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.SCHOOL_OUTLINED,
                            size=16,
                            color=ft.Colors.BLUE_700,
                        ),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=2,
                        controls=[
                            ft.Text(
                                titulo,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK_87,
                                size=13,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                subtitulo,
                                size=11,
                                color=ft.Colors.BLACK_54,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                    ),
                ],
            ),
        )

    def _crear_card_experiencia(self, experiencia):
        """Metodo para crear una card de experiencia laboral."""
        titulo = (
            f"{experiencia.get('puesto', '')} · "
            f"{experiencia.get('empresa', '')}"
        )
        subtitulo = (
            f"{experiencia.get('area', '')} — "
            f"{experiencia.get('descripcion', '')}"
        )
        return ft.Container(
            bgcolor=ft.Colors.BLUE_GREY_50,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            border_radius=10,
            padding=12,
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=34,
                        height=34,
                        border_radius=17,
                        bgcolor=ft.Colors.BLUE_100,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.WORK_OUTLINE,
                            size=16,
                            color=ft.Colors.BLUE_700,
                        ),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=2,
                        controls=[
                            ft.Text(
                                titulo,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK_87,
                                size=13,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                subtitulo,
                                size=11,
                                color=ft.Colors.BLACK_54,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                    ),
                ],
            ),
        )

    async def cargar(
        self,
        page: ft.Page,
        postulante_id: int
    ):
        """Metodo para cargar el perfil del postulante por su id"""
        self.postulante_id = postulante_id
        self.btn_contactar.visible = (
            Sesion.rol(page) == "EMPLEADOR"
        )
        try:
            datos = await PostulanteService.obtener_postulante(
                page=page,
                postulante_id=postulante_id
            )
            self.usuario_reportado_id = datos.get(
                "usuario_id"
            )
            self.mostrar_datos(datos)
        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await page.push_route("/login")
        except ErrorNoEncontrado:
            self.mostrar_mensaje(
                "No se encontró el postulante solicitado"
            )
        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo cargar el perfil. Intente nuevamente"
            )

    def mostrar_datos(self, datos: dict):
        """Metodo para mostrar los datos del postulante en pantalla"""
        self.txt_nombre.value = (
            f"{datos.get('nombre', '')} "
            f"{datos.get('apellido', '')}"
        ).strip()
        self.txt_ubicacion.value = datos.get(
            "ubicacion",
            "",
        )
        self.txt_descripcion.value = (
            datos.get("descripcion_personal")
            or "Sin descripción"
        )
        experiencias = datos.get(
            "experiencias_laborales"
        ) or []
        if experiencias:
            self.lista_experiencias.controls = [
                self._crear_card_experiencia(
                    experiencia
                )
                for experiencia in experiencias
            ]
        else:
            self.lista_experiencias.controls = [
                ft.Text(
                    "Sin experiencia registrada",
                    color=ft.Colors.BLACK_45,
                    size=12,
                )
            ]
        disponibilidad = datos.get(
            "disponibilidad"
        )
        if disponibilidad:
            disponibilidad = self.DISPONIBILIDADES.get(
                disponibilidad,
                disponibilidad.replace(
                    "_",
                    " ",
                ).title(),
            )
        self.txt_disponibilidad.value = (
            disponibilidad
            or "Sin disponibilidad registrada"
        )
        estudios = datos.get(
            "estudios"
        ) or []
        if estudios:
            self.lista_estudios.controls = [
                self._crear_card_estudio(
                    estudio
                )
                for estudio in estudios
            ]
        else:
            self.lista_estudios.controls = [
                ft.Text(
                    "Sin estudios registrados",
                    color=ft.Colors.BLACK_45,
                    size=12,
                )
            ]
        foto = datos.get("foto_perfil")
        if foto:
            self.avatar.foreground_image_src = foto
            self.avatar.content = None
        else:
            self.avatar.foreground_image_src = None
            self.avatar.content = ft.Icon(
                ft.Icons.PERSON,
                size=30,
                color=ft.Colors.BLUE_GREY_400,
            )
        self.cv_url = datos.get("cv_url")
        self.btn_ver_cv.disabled = False
        habilidades = datos.get("habilidades") or []
        if habilidades:
            self.fila_habilidades.controls = [
                ft.Container(
                    bgcolor=ft.Colors.BLUE_50,
                    border=ft.Border.all(
                        1,
                        ft.Colors.BLUE_200,
                    ),
                    border_radius=20,
                    padding=ft.Padding(
                        left=10,
                        top=5,
                        right=10,
                        bottom=5,
                    ),
                    content=ft.Text(
                        habilidad.get("nombre", ""),
                        color=ft.Colors.BLUE_900,
                        size=12,
                    ),
                )
                for habilidad in habilidades
            ]
        else:
            self.fila_habilidades.controls = [
                ft.Text(
                    "No especificadas",
                    color=ft.Colors.BLACK_45
                )
            ]
        self._igualar_alturas(
            cantidad_experiencias=len(experiencias),
            cantidad_estudios=len(estudios),
        )
    @staticmethod

    def _alto_tarjeta_lista(cantidad: int):
        """Alto estimado de una tarjeta con lista de items."""
        alto_items = (
            62 * cantidad + 10 * (cantidad - 1)
            if cantidad > 0
            else 15
        )
        return 57 + alto_items

    def _igualar_alturas(
        self,
        cantidad_experiencias: int,
        cantidad_estudios: int,
    ):
        """Iguala la altura de las tarjetas que comparten fila."""
        if cantidad_experiencias == 0:
            alto_experiencia = self.ALTO_EXPERIENCIA_VACIA
            self.tarjeta_experiencia.height = alto_experiencia
        else:
            alto_experiencia = self._alto_tarjeta_lista(
                cantidad_experiencias
            )
            self.tarjeta_experiencia.height = None
        alto_disponibilidad = 116
        espaciado = 20
        alto_columna = (
            alto_experiencia
            + espaciado
            + alto_disponibilidad
        )
        texto = self.txt_descripcion.value or ""
        lineas = sum(
            max(1, math.ceil(len(parte) / 60))
            for parte in texto.split("\n")
        )
        alto_texto = 57 + 20 * lineas
        if alto_texto > alto_columna:
            self.tarjeta_descripcion.height = None
        else:
            self.tarjeta_descripcion.height = alto_columna
        alto_estudios = max(
            self._alto_tarjeta_lista(cantidad_estudios),
            110,
        )
        self.tarjeta_estudios.height = alto_estudios
        self.tarjeta_habilidades.height = alto_estudios

    async def contactar(self, e):
        """Metodo para seleccionar la oferta desde la cual contactar"""
        if Sesion.rol(self.page) != "EMPLEADOR":
            return
        if not self.postulante_id:
            self.mostrar_mensaje(
                "No se pudo identificar al postulante"
            )
            return
        if self.cargando_ofertas_contacto:
            return
        self.cargando_ofertas_contacto = True
        self.oferta_seleccionada = None
        self.cards_ofertas = []
        indicador_carga = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
            controls=[
                ft.ProgressRing(
                    width=35,
                    height=35,
                ),
                ft.Text(
                    "Cargando ofertas laborales...",
                    size=14,
                    color=ft.Colors.BLACK_54,
                ),
            ],
        )
        contenido = ft.Column(
            expand=True,
            spacing=15,
            controls=[
                ft.Text(
                    "Seleccioná la oferta laboral desde la "
                    "cual querés contactar a este postulante.",
                    color=ft.Colors.BLACK,
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=indicador_carga,
                ),
            ],
        )
        self.txt_boton_enviar_contacto = ft.Text(
            "CONTACTAR",
            color=ft.Colors.WHITE,
        )
        self.rueda_boton_enviar_contacto = ft.ProgressRing(
            width=16,
            height=16,
            stroke_width=2,
            color=ft.Colors.WHITE,
            visible=False,
        )
        self.btn_enviar_contacto = ft.FilledButton(
            width=140,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    self.rueda_boton_enviar_contacto,
                    self.txt_boton_enviar_contacto,
                ],
            ),
            disabled=True,
            on_click=self.enviar_contacto,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(
                    radius=10,
                ),
            ),
        )
        dialogo = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.WHITE,
            title=ft.Text(
                "Contactar postulante",
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
            ),
            content=ft.Container(
                width=700,
                height=500,
                bgcolor=ft.Colors.WHITE,
                content=contenido,
            ),
            actions=[
                ft.TextButton(
                    "CANCELAR",
                    on_click=lambda e: self.page.pop_dialog(),
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
                ),
                self.btn_enviar_contacto,
            ],
        )
        self.page.show_dialog(dialogo)
        self.page.update()
        try:
            ofertas = (
                await EmpleadorService
                .verificar_conexiones_oferta_laboral(
                    page=self.page,
                    postulante_id=self.postulante_id,
                )
            )
            if not ofertas:
                contenido.controls[1] = (
                    self.crear_mensaje_sin_ofertas()
                )
                self.page.update()
                return
            lista_ofertas = ft.ListView(
                expand=True,
                spacing=10,
            )
            contenido.controls[1] = lista_ofertas
            for oferta in ofertas:
                card = self.crear_card_oferta(
                    oferta,
                    lista_ofertas,
                )
                self.cards_ofertas.append(
                    {
                        "oferta": oferta,
                        "card": card,
                    }
                )
                lista_ofertas.controls.append(card)
            self.page.update()
        except ErrorAutenticacion:
            self.page.pop_dialog()
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await self.page.push_route("/login")
        except ErrorNoEncontrado:
            contenido.controls[1] = (
                self.crear_mensaje_sin_ofertas()
            )
            self.page.update()
        except ErrorServidor:
            contenido.controls[1] = ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    horizontal_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=(
                        ft.MainAxisAlignment.CENTER
                    ),
                    controls=[
                        ft.Icon(
                            ft.Icons.ERROR_OUTLINE,
                            size=45,
                            color=ft.Colors.RED_300,
                        ),
                        ft.Text(
                            "No se pudieron cargar "
                            "las ofertas laborales.",
                            color=ft.Colors.RED_500,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                ),
            )
            self.page.update()
        finally:
            self.cargando_ofertas_contacto = False

    def crear_mensaje_sin_ofertas(self):
        """Metodo para mostrar que no existen ofertas disponibles"""
        return ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        ft.Icons.WORK_OFF,
                        size=45,
                        color=ft.Colors.BLUE_GREY_300,
                    ),
                    ft.Text(
                        "No hay ofertas disponibles",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                    ),
                    ft.Text(
                        "No tenés ofertas disponibles "
                        "para contactar a este postulante.",
                        size=13,
                        color=ft.Colors.BLACK_45,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    def crear_card_oferta(
        self,
        oferta: dict,
        lista_ofertas: ft.ListView,
    ):
        """Metodo para crear una card seleccionable de oferta"""
        icono_seleccion = ft.Icon(
            ft.Icons.RADIO_BUTTON_UNCHECKED,
            color=ft.Colors.BLUE_GREY_300,
            size=22,
        )
        card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            border_radius=12,
            padding=15,
            ink=True,
            on_click=lambda e: self.seleccionar_oferta(
                oferta,
                lista_ofertas,
            ),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Row(
                        vertical_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),
                        controls=[
                            ft.Icon(
                                ft.Icons.WORK_OUTLINE,
                                color=ft.Colors.BLUE_500,
                                size=24,
                            ),
                            ft.Text(
                                oferta.get(
                                    "titulo",
                                    "Sin título",
                                ),
                                expand=True,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK_87,
                            ),
                            icono_seleccion,
                        ],
                    ),
                    ft.Row(
                        spacing=20,
                        wrap=True,
                        controls=[
                            ft.Row(
                                spacing=5,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.LOCATION_ON_OUTLINED,
                                        size=17,
                                        color=ft.Colors.BLACK_54,
                                    ),
                                    ft.Text(
                                        oferta.get(
                                            "ubicacion",
                                            "Sin ubicación",
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
                                        ft.Icons.HOME_OUTLINED,
                                        size=17,
                                        color=ft.Colors.BLACK_54,
                                    ),
                                    ft.Text(
                                        oferta.get(
                                            "direccion",
                                            "Sin dirección",
                                        ),
                                        size=13,
                                        color=ft.Colors.BLACK_54,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Divider(
                        height=1,
                        color=ft.Colors.BLUE_GREY_100,
                    ),
                    ft.Text(
                        oferta.get(
                            "descripcion",
                            "Sin descripción",
                        ),
                        size=13,
                        color=ft.Colors.BLACK_87,
                        max_lines=4,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
            ),
        )
        card._icono_seleccion = icono_seleccion
        return card

    def seleccionar_oferta(
        self,
        oferta: dict,
        lista_ofertas: ft.ListView,
    ):
        """Metodo para seleccionar una unica oferta"""
        self.oferta_seleccionada = oferta
        for item in self.cards_ofertas:
            card = item["card"]
            card.border = ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            )
            card.bgcolor = ft.Colors.WHITE
            icono = getattr(
                card,
                "_icono_seleccion",
                None,
            )
            if icono:
                icono.name = ft.Icons.RADIO_BUTTON_UNCHECKED
                icono.color = ft.Colors.BLUE_GREY_300
        for item in self.cards_ofertas:
            if item["oferta"].get("id") == oferta.get("id"):
                card = item["card"]
                card.border = ft.Border.all(
                    2,
                    ft.Colors.BLUE_500,
                )
                card.bgcolor = ft.Colors.BLUE_50
                icono = getattr(
                    card,
                    "_icono_seleccion",
                    None,
                )
                if icono:
                    icono.name = ft.Icons.RADIO_BUTTON_CHECKED
                    icono.color = ft.Colors.BLUE_500
                break
        self.btn_enviar_contacto.disabled = False
        self.page.update()

    async def enviar_contacto(self, e):
        """Metodo para crear la conexion laboral"""
        if Sesion.rol(self.page) != "EMPLEADOR":
            return
        if not self.oferta_seleccionada:
            return
        if self.cargando_contacto:
            return
        oferta_id = self.oferta_seleccionada.get("id")
        if not oferta_id:
            return
        self.cargando_contacto = True
        self.btn_enviar_contacto.disabled = True
        self.txt_boton_enviar_contacto.value = "Cargando..."
        self.rueda_boton_enviar_contacto.visible = True
        self.page.update()
        try:
            await EmpleadorService.crear_conexion_laboral(
                page=self.page,
                oferta_laboral_id=oferta_id,
                postulante_id=self.postulante_id,
            )
            self.page.pop_dialog()
            self.btn_contactar.visible = True
            self.mostrar_mensaje(
                "Conexión laboral creada correctamente"
            )
        except ErrorAutenticacion:
            self.page.pop_dialog()
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await self.page.push_route("/login")
        except ErrorNoEncontrado:
            self.page.pop_dialog()
            self.mostrar_mensaje(
                "No se pudo encontrar la oferta o el postulante"
            )
        except ErrorServidor:
            self.page.pop_dialog()
            self.mostrar_mensaje(
                "No se pudo enviar la solicitud de contacto. "
                "Intente nuevamente"
            )
        finally:
            self.cargando_contacto = False

    async def ver_cv(self, e):
        """Metodo para informar y confirmar la descarga del CV."""
        if not self.cv_url:
            self.page.show_dialog(
                ft.AlertDialog(
                    modal=True,
                    bgcolor=ft.Colors.WHITE,
                    title=ft.Text(
                        "CV no disponible",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_87,
                    ),
                    content=ft.Text(
                        "Este postulante no subió su CV.",
                        color=ft.Colors.BLACK_54,
                    ),
                    actions=[
                        ft.TextButton(
                            "ACEPTAR",
                            on_click=lambda e: (
                                self.page.pop_dialog()
                            ),
                            style=ft.ButtonStyle(
                                color=ft.Colors.BLUE_500,
                            ),
                        ),
                    ],
                )
            )
            return
        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    "Descargar CV",
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK_87,
                ),
                content=ft.Text(
                    "Vas a descargar el CV de este postulante. "
                    "¿Querés continuar?",
                    color=ft.Colors.BLACK_54,
                ),
                actions=[
                    ft.TextButton(
                        "CANCELAR",
                        on_click=lambda e: (
                            self.page.pop_dialog()
                        ),
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_500,
                        ),
                    ),
                    ft.FilledButton(
                        "DESCARGAR",
                        on_click=self.confirmar_descarga_cv,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_500,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(
                                radius=10,
                            ),
                        ),
                    ),
                ],
            )
        )

    async def confirmar_descarga_cv(self, e):
        """Metodo para confirmar y abrir el CV del postulante."""
        self.page.pop_dialog()
        if self.cv_url:
            await self.page.launch_url(
                self.cv_url
            )

    async def volver(self, e):
        """Metodo para volver a la busqueda"""
        if Sesion.rol(self.page) == "ADMINISTRADOR":
            await self.page.push_route(
                "/perfil-personal-administrador"
            )
        else:
            await self.page.push_route(
                "/busqueda"
            )

    async def reportar(self, e):
        """Metodo para reportar al postulante"""
        await self.page.push_route(
            f"/reporte?usuario_reportado_id="
            f"{self.usuario_reportado_id}"
        )

    def mostrar_mensaje(self, mensaje):
        """Metodo para mostrar mensajes"""
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
                        on_click=lambda e: (
                            self.page.pop_dialog()
                        ),
                    )
                ],
            )
        )
