import asyncio
import unicodedata

import flet as ft

from frontend.src.services.postulante_service import PostulanteService
from frontend.src.services.empleador_service import EmpleadorService
from frontend.src.services.oferta_laboral_service import OfertaLaboralService
from frontend.src.services.mensaje_service import MensajeService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion
)
from frontend.src.components.habilidades import HABILIDADES
from frontend.src.components.rubros import RUBROS
from frontend.src.session.sesion import Sesion

# pylint: disable=E1121,E1123,E0401,E1101


class BusquedaView(ft.View):

    def __init__(
        self,
        perfil_postulante,
        perfil_empleador,
        perfil_oferta,
        perfil_personal_postulante,
        perfil_personal_empleador
    ):
        super().__init__()

        self.route = "/busqueda"
        self.padding = 0
        self.spacing = 0
        self.bgcolor = ft.Colors.BLUE_GREY_50
        self.theme_mode = ft.ThemeMode.LIGHT
        self.expand = True

        self.perfil_postulante = perfil_postulante
        self.perfil_empleador = perfil_empleador
        self.perfil_oferta = perfil_oferta
        self.perfil_personal_postulante = perfil_personal_postulante
        self.perfil_personal_empleador = perfil_personal_empleador

        self._running = True
        self._tarea_mensajes = None

        self.habilidades_disponibles = sorted(list(HABILIDADES))
        self.habilidades_seleccionadas = []
        self.cargando = False
        self.contador = 0
        self.cantidad_mensajes_no_leidos = 0
        self.botones_cards_cargando = set()
        self.textos_botones_cards = {}

        self.rubros_disponibles = sorted(
            RUBROS,
            key=lambda r: unicodedata.normalize(
                "NFD", r
            ).encode("ascii", "ignore").decode().lower()
        )

        self.filtros_aplicados = {
            "perfil": "postulante"
        }

        self.claves_filtros = {
            "Ubicación": "ubicacion",
            "Disponibilidad": "disponibilidad",
            "Estudios": "estudios",
            "Experiencias Laborales": "experiencias_laborales",
            "Dirección": "direccion",
            "Rubro": "rubro",
            "Jornada": "jornada",
            "Turno": "turno",
        }

        self.dias_semana = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo"
        ]

        self.dias_seleccionados = []

        self.fila_dias = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8,
        )

        self.columna_filtros = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=15
        )

        self.cargar_filtros_postulante()

        self.perfil = ft.RadioGroup(
            value="postulante",
            on_change=self.cambiar_filtros_perfil,
            content=ft.Column(
                controls=[
                    ft.Radio(
                        label="Postulante",
                        value="postulante",
                        fill_color=ft.Colors.BLUE_500,
                        label_style=ft.TextStyle(
                            color=ft.Colors.BLACK
                        )
                    ),
                    ft.Radio(
                        label="Empleador",
                        value="empleador",
                        fill_color=ft.Colors.BLUE_500,
                        label_style=ft.TextStyle(
                            color=ft.Colors.BLACK
                        )
                    ),
                    ft.Radio(
                        label="Oferta Laboral",
                        value="oferta",
                        fill_color=ft.Colors.BLUE_500,
                        label_style=ft.TextStyle(
                            color=ft.Colors.BLACK
                        )
                    )
                ]
            )
        )

        self.panel_overlay = ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(
                0.6,
                ft.Colors.BLACK
            ),
            visible=False,
            on_click=self.cancelar_panel
        )

        self.search_bar_habilidades = ft.SearchBar(
            view_bgcolor=ft.Colors.WHITE,
            bar_hint_text="Buscar habilidad...",
            view_hint_text="Escribí para buscar...",
            view_header_text_style=ft.TextStyle(
                color=ft.Colors.BLACK
            ),
            bar_bgcolor=ft.Colors.WHITE,
            bar_border_side=ft.BorderSide(
                1,
                ft.Colors.BLUE_GREY_200
            ),
            bar_elevation=0,
            view_elevation=4,
            divider_color=ft.Colors.BLUE_GREY_100,
            on_change=self.filtrar_habilidades,
            on_tap=self.abrir_vista_habilidades,
            controls=[
                ft.ListTile(
                    title=ft.Text(
                        h,
                        color=ft.Colors.BLACK
                    ),
                    on_click=self.seleccionar_habilidad_desde_busqueda,
                    bgcolor=ft.Colors.WHITE,
                )
                for h in self.habilidades_disponibles
            ]
        )

        self.row_habilidades = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8
        )

        self.contenedor_etiquetas = ft.Container(
            expand=True,
            content=self.row_habilidades
        )

        self.wrapper_search_bar = ft.Container(
            content=self.search_bar_habilidades,
            ignore_interactions=False,
        )

        self.contenedor_habilidades = ft.Container(
            expand=True,
            animate_opacity=200,
            content=ft.Column(
                expand=True,
                spacing=15,
                horizontal_alignment=(
                    ft.CrossAxisAlignment.STRETCH
                ),
                controls=[
                    ft.Text(
                        "HABILIDADES",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12
                    ),
                    self.wrapper_search_bar,
                    ft.Text(
                        "Seleccionadas:",
                        size=12,
                        color=ft.Colors.BLACK_45
                    ),
                    ft.Container(
                        height=300,
                        border=ft.Border.all(
                            1,
                            ft.Colors.BLUE_GREY_100
                        ),
                        theme=ft.Theme(
                            scrollbar_theme=ft.ScrollbarTheme(
                                thumb_color=ft.Colors.BLUE,
                                thumb_visibility=True,
                                track_color=ft.Colors.BLUE_GREY_100,
                                track_visibility=True,
                                thickness=6,
                                radius=3,
                            )
                        ),
                        border_radius=10,
                        padding=10,
                        bgcolor=ft.Colors.BLUE_GREY_50,
                        content=ft.Column(
                            scroll=ft.ScrollMode.ALWAYS,
                            controls=[
                                self.contenedor_etiquetas
                            ]
                        )
                    )
                ]
            )
        )

        self.panel_modal = ft.Container(
            width=950,
            height=600,
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            padding=40,
            shadow=ft.BoxShadow(
                blur_radius=30,
                color=ft.Colors.BLACK_54
            ),
            offset=ft.Offset(0, 2),
            animate_offset=ft.Animation(
                400,
                ft.AnimationCurve.DECELERATE
            ),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Text(
                        "Filtros de Búsqueda",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_87,
                        font_family="Inter-Bold"
                    ),
                    ft.Divider(
                        height=20,
                        color=ft.Colors.BLUE_GREY_100
                    ),
                    ft.Row(
                        expand=True,
                        vertical_alignment=(
                            ft.CrossAxisAlignment.START
                        ),
                        spacing=25,
                        controls=[
                            ft.Container(
                                width=170,
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "TIPO DE PERFIL",
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.BLACK_54,
                                            font_family="Inter-Bold",
                                            size=12
                                        ),
                                        self.perfil
                                    ]
                                )
                            ),
                            ft.Container(
                                width=280,
                                content=self.columna_filtros
                            ),
                            self.contenedor_habilidades
                        ]
                    ),
                    ft.Divider(
                        height=10,
                        color=ft.Colors.TRANSPARENT
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        spacing=15,
                        controls=[
                            ft.Button(
                                "Aplicar filtros",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE_500
                                ),
                                on_click=self.aplicar_filtros
                            ),
                            ft.OutlinedButton(
                                "Cancelar",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.BLUE_500
                                ),
                                on_click=self.cancelar_panel
                            ),
                            ft.OutlinedButton(
                                "Quitar filtros",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.RED_500,
                                    side=ft.BorderSide(
                                        1,
                                        ft.Colors.RED_500
                                    )
                                ),
                                on_click=self.quitar_filtros
                            )
                        ]
                    )
                ]
            )
        )

        self.modal_wrapper = ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=self.panel_modal,
            visible=False
        )

        self.badge_mensajes = ft.Container(
            width=22,
            height=22,
            bgcolor=ft.Colors.RED,
            border_radius=50,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                "0",
                size=11,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
            ),
            visible=False,
        )

        self.boton_mensajes = ft.Stack(
            width=50,
            height=50,
            controls=[
                ft.IconButton(
                    icon=ft.Image(
                        src="images/Chat_icon.png",
                        width=40,
                        height=40,
                    ),
                    icon_color=ft.Colors.BLACK_87,
                    icon_size=28,
                    tooltip="Mensajes",
                    on_click=self.ir_a_mensajeria,
                ),
                ft.Container(
                    right=0,
                    top=0,
                    content=self.badge_mensajes,
                ),
            ],
        )

        self.boton_perfil = ft.GestureDetector(
            on_tap=self.ir_a_perfil_personal,
            content=ft.CircleAvatar(
                content=ft.Icon(
                    ft.Icons.PERSON,
                    color=ft.Colors.WHITE
                ),
                bgcolor=ft.Colors.BLUE_500,
                radius=20,
            ),
        )

        self.header = ft.Container(
            padding=ft.Padding.symmetric(
                horizontal=20,
                vertical=15
            ),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.boton_mensajes,
                    self.boton_perfil,
                ],
            ),
        )

        self.frase_motivadora = ft.Text(
            "¿Qué estás buscando hoy?",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK_87,
            text_align=ft.TextAlign.CENTER
        )

        self.busqueda = ft.TextField(
            hint_text="Buscar puesto, perfil...",
            expand=True,
            border_radius=15,
            bgcolor="#f8f4f4",
            border_color=ft.Colors.TRANSPARENT,
            focused_border_color=ft.Colors.BLUE_500,
            color=ft.Colors.BLACK_87,
            on_submit=self.buscar
        )

        self.boton_buscar = ft.Button(
            "BUSCAR",
            height=50,
            on_click=self.buscar,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(
                    radius=15
                )
            )
        )

        self.barra_busqueda = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.busqueda,
                self.boton_buscar
            ]
        )

        self.filtros = ft.OutlinedButton(
            "FILTROS",
            icon=ft.Icons.FILTER_LIST,
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
            on_click=self.abrir_panel
        )

        self.tamano_pagina = 10
        self.offset = 0
        self.pagina = 1
        self.cantidad_actual = 0
        self.offsets_previos = []
        self.hay_mas = False
        self.consulta_actual = ""
        self.filtros_busqueda = {
            "perfil": "postulante"
        }

        self.lista_resultados = ft.Column(
            spacing=15,
            horizontal_alignment=(
                ft.CrossAxisAlignment.STRETCH
            )
        )

        self.btn_anterior = ft.OutlinedButton(
            "Anterior",
            icon=ft.Icons.CHEVRON_LEFT,
            on_click=self.pagina_anterior,
            disabled=True
        )

        self.txt_pagina = ft.Text(
            "Página 1",
            color=ft.Colors.BLACK_87
        )

        self.btn_siguiente = ft.OutlinedButton(
            "Siguiente",
            icon=ft.Icons.CHEVRON_RIGHT,
            on_click=self.pagina_siguiente,
            disabled=True
        )

        self.paginacion = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False,
            controls=[
                self.btn_anterior,
                self.txt_pagina,
                self.btn_siguiente
            ]
        )

        self.bg_image = ft.Image(
            src="images/LaburAR_bg2.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.contenido_principal = ft.Column(
            expand=True,
            spacing=0,
            controls=[
                self.header,
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.STRETCH
                        ),
                        controls=[
                            ft.Container(
                                alignment=ft.Alignment.TOP_CENTER,
                                content=ft.Container(
                                    width=700,
                                    padding=ft.Padding.only(
                                        top=60,
                                        bottom=20
                                    ),
                                    content=ft.Column(
                                        horizontal_alignment=(
                                            ft.CrossAxisAlignment.CENTER
                                        ),
                                        spacing=20,
                                        controls=[
                                            self.frase_motivadora,
                                            self.barra_busqueda,
                                            self.filtros,
                                            self.lista_resultados,
                                            self.paginacion
                                        ]
                                    )
                                )
                            )
                        ]
                    )
                )
            ]
        )

        self.controls = [
            ft.Stack(
                expand=True,
                fit=ft.StackFit.EXPAND,
                controls=[
                    ft.Container(
                        expand=True,
                        content=self.bg_image,
                    ),
                    self.contenido_principal,
                    self.panel_overlay,
                    self.modal_wrapper,
                ]
            )
        ]

    def _mostrar_cargando_perfil(self, cargando):
        """Actualiza visualmente el icono de perfil durante la carga."""

        self.boton_perfil.disabled = cargando

        if cargando:
            self.boton_perfil.content = ft.CircleAvatar(
                content=ft.ProgressRing(
                    width=20,
                    height=20,
                    stroke_width=2,
                    color=ft.Colors.WHITE,
                ),
                bgcolor=ft.Colors.BLUE_500,
                radius=20,
            )
        else:
            self.boton_perfil.content = ft.CircleAvatar(
                content=ft.Icon(
                    ft.Icons.PERSON,
                    color=ft.Colors.WHITE
                ),
                bgcolor=ft.Colors.BLUE_500,
                radius=20,
            )

        self.boton_perfil.update()

    async def ir_a_perfil_personal(self, e):
        """Metodo para navegar al perfil personal segun el rol del usuario"""

        if self.cargando:
            return

        self.cargando = True
        self._mostrar_cargando_perfil(True)

        try:
            rol = Sesion.rol(self.page)

            if rol == "POSTULANTE":
                await self.perfil_personal_postulante.cargar(
                    self.page
                )

                await self.page.push_route(
                    "/perfil-personal-postulante"
                )

            elif rol == "EMPLEADOR":
                await self.perfil_personal_empleador.cargar(
                    self.page
                )

                await self.page.push_route(
                    "/perfil-personal-empleador"
                )

        finally:
            self.cargando = False
            self._mostrar_cargando_perfil(False)

    def cambiar_filtros_perfil(self, e):
        """Metodo para cambiar los filtros segun el perfil seleccionado"""

        tipo = e.control.value

        if tipo == "postulante":
            self.cargar_filtros_postulante()
        elif tipo == "empleador":
            self.cargar_filtros_empleador()
        elif tipo == "oferta":
            self.cargar_filtros_oferta()

        self.actualizar_estado_habilidades(tipo)

        self.habilidades_seleccionadas.clear()
        self.row_habilidades.controls.clear()

        self.panel_modal.update()

    def actualizar_estado_habilidades(self, tipo):
        """Metodo para activar o desactivar el bloque de habilidades"""

        es_postulante = tipo == "postulante"

        self.contenedor_habilidades.disabled = not es_postulante
        self.contenedor_habilidades.opacity = (
            1 if es_postulante else 0.4
        )
        self.search_bar_habilidades.disabled = not es_postulante
        self.wrapper_search_bar.ignore_interactions = (
            not es_postulante
        )

    def crear_dropdown_rubro(self):
        """Metodo para crear el dropdown de rubro"""

        return ft.Dropdown(
            label="Rubro",
            editable=True,
            enable_filter=True,
            menu_height=250,
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            options=[
                ft.DropdownOption(
                    r,
                    style=ft.ButtonStyle(
                        color={
                            ft.ControlState.DEFAULT:
                                ft.Colors.BLACK_87
                        }
                    )
                )
                for r in self.rubros_disponibles
            ],
            border_radius=10,
            on_blur=self.validar_rubro,
        )

    async def validar_rubro(self, e):
        """Metodo para validar que el rubro ingresado sea uno de la lista"""

        await asyncio.sleep(0.2)

        dd = e.control

        if dd.value in self.rubros_disponibles:
            return

        if dd in self.columna_filtros.controls:
            idx = self.columna_filtros.controls.index(dd)

            self.columna_filtros.controls[idx] = (
                self.crear_dropdown_rubro()
            )

            self.columna_filtros.update()

    def cargar_filtros_postulante(self):
        """Metodo para cargar los filtros del perfil postulante"""

        self.columna_filtros.controls = [
            ft.Text(
                "DATOS DEL POSTULANTE",
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK_54,
                font_family="Inter-Bold",
                size=12
            ),
            ft.Dropdown(
                label="Ubicación",
                color=ft.Colors.BLACK,
                bgcolor=ft.Colors.WHITE,
                options=[
                    ft.DropdownOption(
                        "Punta Alta",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    )
                ],
                border_radius=10,
            ),
            ft.Dropdown(
                label="Disponibilidad",
                options=[
                    ft.DropdownOption(
                        "JORNADA_COMPLETA",
                        "Jornada Completa",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                    ft.DropdownOption(
                        "MEDIA_JORNADA",
                        "Media Jornada",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                    ft.DropdownOption(
                        "FINES_SEMANA",
                        "Fines de Semana",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                    ft.DropdownOption(
                        "A_CONVENIR",
                        "A Convenir",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    )
                ],
                border_radius=10,
                color=ft.Colors.BLACK,
                bgcolor=ft.Colors.WHITE
            ),
            ft.TextField(
                label="Estudios",
                hint_text="Ej: Ingeniero de software...",
                border_radius=10,
                color=ft.Colors.BLACK_87
            ),
            ft.TextField(
                label="Experiencias Laborales",
                hint_text="Ej: Analista en Sistemas...",
                border_radius=10,
                color=ft.Colors.BLACK_87
            )
        ]

    def cargar_filtros_empleador(self):
        """Metodo para cargar los filtros del perfil empleador"""

        self.columna_filtros.controls = [
            ft.Text(
                "DATOS DEL EMPLEADOR",
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK_54,
                font_family="Inter-Bold",
                size=12
            ),
            ft.Dropdown(
                label="Ubicación",
                color=ft.Colors.BLACK,
                bgcolor=ft.Colors.WHITE,
                options=[
                    ft.DropdownOption(
                        "Punta Alta",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    )
                ],
                border_radius=10,
            ),
            ft.TextField(
                label="Dirección",
                hint_text="Ej: Bernardo de Irigoyen 123",
                border_radius=10,
                color=ft.Colors.BLACK_87
            ),
            self.crear_dropdown_rubro()
        ]

    def cargar_filtros_oferta(self):
        """Metodo para cargar los filtros del perfil oferta laboral"""

        self.dias_seleccionados = []

        self.fila_dias.controls = [
            self.crear_chip_dia(dia)
            for dia in self.dias_semana
        ]

        self.columna_filtros.controls = [
            ft.Text(
                "DATOS DE LA OFERTA",
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK_54,
                font_family="Inter-Bold",
                size=12
            ),
            self.crear_dropdown_rubro(),
            ft.Dropdown(
                label="Jornada",
                options=[
                    ft.DropdownOption(
                        "COMPLETA",
                        "Completa",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                    ft.DropdownOption(
                        "MEDIA_JORNADA",
                        "Media Jornada",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                    ft.DropdownOption(
                        "TEMPORAL",
                        "Temporal",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                    ft.DropdownOption(
                        "A_CONVENIR",
                        "A Convenir",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                ],
                border_radius=10,
                color=ft.Colors.BLACK,
                bgcolor=ft.Colors.WHITE
            ),
            ft.Dropdown(
                label="Turno",
                options=[
                    ft.DropdownOption(
                        "MAÑANA",
                        "Mañana",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                    ft.DropdownOption(
                        "TARDE",
                        "Tarde",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                    ft.DropdownOption(
                        "NOCHE",
                        "Noche",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                    ft.DropdownOption(
                        "A_CONVENIR",
                        "A Convenir",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.DEFAULT:
                                    ft.Colors.BLACK_87
                            }
                        )
                    ),
                ],
                border_radius=10,
                color=ft.Colors.BLACK,
                bgcolor=ft.Colors.WHITE,
            ),
            ft.Text(
                "DÍAS LABORALES",
                size=11,
                color=ft.Colors.BLACK_54,
                weight=ft.FontWeight.BOLD
            ),
            self.fila_dias,
        ]

    def crear_chip_dia(self, dia: str):
        """Metodo para crear el boton de un dia"""

        chip = ft.Container(
            data=dia,
            tooltip=dia,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_500
            ),
            border_radius=20,
            padding=ft.Padding(
                left=12,
                top=6,
                right=12,
                bottom=6
            ),
            on_click=self.alternar_dia,
            content=ft.Text(
                dia[:3],
                size=12,
                weight=ft.FontWeight.W_500,
            ),
        )

        self.estilizar_chip_dia(
            chip,
            dia in self.dias_seleccionados
        )

        return chip

    @staticmethod
    def estilizar_chip_dia(chip, seleccionado: bool):
        """Metodo para pintar un dia como seleccionado o no"""

        chip.bgcolor = (
            ft.Colors.BLUE_500
            if seleccionado
            else ft.Colors.WHITE
        )

        chip.content.color = (
            ft.Colors.WHITE
            if seleccionado
            else ft.Colors.BLUE_900
        )

    def alternar_dia(self, e):
        """Metodo para elegir o quitar un dia del filtro"""

        dia = e.control.data

        if dia in self.dias_seleccionados:
            self.dias_seleccionados.remove(dia)
        else:
            self.dias_seleccionados.append(dia)

        self.estilizar_chip_dia(
            e.control,
            dia in self.dias_seleccionados
        )

        e.control.update()

    async def abrir_vista_habilidades(self, e):
        """Metodo para abrir la vista de busqueda de habilidades"""

        if self.perfil.value != "postulante":
            return

        await self.search_bar_habilidades.open_view()

    def filtrar_habilidades(self, e):
        """Metodo para filtrar las habilidades"""

        if self.perfil.value != "postulante":
            return

        texto_buscado = (
            e.control.value or ""
        ).lower().strip()

        habilidades_filtradas = [
            h
            for h in self.habilidades_disponibles
            if texto_buscado in h.lower()
        ]

        self.search_bar_habilidades.controls = [
            ft.ListTile(
                title=ft.Text(
                    h,
                    color=ft.Colors.BLACK
                ),
                on_click=self.seleccionar_habilidad_desde_busqueda,
                bgcolor=ft.Colors.WHITE,
            )
            for h in habilidades_filtradas
        ]

        self.page.update()

    async def seleccionar_habilidad_desde_busqueda(self, e):
        """Metodo para seleccionar una habilidad"""

        habilidad = e.control.title.value

        if (
            habilidad
            and habilidad not in self.habilidades_seleccionadas
        ):
            self.habilidades_seleccionadas.append(
                habilidad
            )
            self.renderizar_etiquetas()

        await self.search_bar_habilidades.close_view(
            habilidad
        )

    def remover_habilidad(self, e):
        """Metodo para remover una habilidad"""

        habilidad = e.control.data

        if habilidad in self.habilidades_seleccionadas:
            self.habilidades_seleccionadas.remove(
                habilidad
            )
            self.renderizar_etiquetas()

        self.page.update()

    def renderizar_etiquetas(self):
        """Metodo para renderizar las etiquetas"""

        self.row_habilidades.controls.clear()

        for hab in self.habilidades_seleccionadas:
            tag = ft.Container(
                bgcolor=ft.Colors.BLUE_50,
                border=ft.Border.all(
                    1,
                    ft.Colors.BLUE_200
                ),
                border_radius=20,
                padding=ft.Padding(
                    left=10,
                    top=5,
                    right=10,
                    bottom=5
                ),
                content=ft.Row(
                    tight=True,
                    spacing=5,
                    controls=[
                        ft.Icon(
                            ft.Icons.CIRCLE,
                            size=8,
                            color=ft.Colors.BLUE_500
                        ),
                        ft.Text(
                            hab,
                            color=ft.Colors.BLUE_900,
                            weight=ft.FontWeight.W_500,
                            size=12
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=ft.Colors.BLUE_900,
                            icon_size=14,
                            width=20,
                            height=20,
                            padding=0,
                            data=hab,
                            on_click=self.remover_habilidad
                        )
                    ]
                )
            )

            self.row_habilidades.controls.append(tag)

        self.panel_modal.update()

    def obtener_filtros(self):
        """Metodo para obtener los filtros cargados"""

        filtros = {
            "perfil": self.perfil.value
        }

        for control in self.columna_filtros.controls:
            if not isinstance(
                control,
                (ft.Dropdown, ft.TextField)
            ):
                continue

            clave = self.claves_filtros.get(
                control.label
            )

            valor = (
                control.value.strip()
                if control.value
                else ""
            )

            if not clave or not valor:
                continue

            if (
                clave == "rubro"
                and valor not in self.rubros_disponibles
            ):
                continue

            filtros[clave] = valor

        if (
            self.perfil.value == "postulante"
            and self.habilidades_seleccionadas
        ):
            filtros["habilidades"] = list(
                self.habilidades_seleccionadas
            )

        if (
            self.perfil.value == "oferta"
            and self.dias_seleccionados
        ):
            filtros["dias_laborales"] = [
                dia
                for dia in self.dias_semana
                if dia in self.dias_seleccionados
            ]

        return filtros

    def obtener_filtros_aplicados(self):
        """Metodo para obtener una copia de los filtros"""

        return dict(
            self.filtros_aplicados
        )

    def restaurar_filtros(self, filtros):
        """Metodo para restaurar el panel"""

        tipo = filtros.get(
            "perfil",
            "postulante"
        )

        self.perfil.value = tipo

        if tipo == "postulante":
            self.cargar_filtros_postulante()
        elif tipo == "empleador":
            self.cargar_filtros_empleador()
        elif tipo == "oferta":
            self.cargar_filtros_oferta()

        for control in self.columna_filtros.controls:
            if isinstance(
                control,
                (ft.Dropdown, ft.TextField)
            ):
                clave = self.claves_filtros.get(
                    control.label
                )

                if clave in filtros:
                    control.value = filtros[clave]

        if tipo == "oferta":
            self.dias_seleccionados = list(
                filtros.get(
                    "dias_laborales",
                    []
                )
            )

            for chip in self.fila_dias.controls:
                self.estilizar_chip_dia(
                    chip,
                    chip.data in self.dias_seleccionados
                )

        self.habilidades_seleccionadas = list(
            filtros.get(
                "habilidades",
                []
            )
        )

        self.actualizar_estado_habilidades(tipo)
        self.renderizar_etiquetas()

    def _mostrar_cargando(self, cargando):
        """Actualiza visualmente los controles durante una búsqueda."""

        self.boton_buscar.disabled = cargando
        self.btn_anterior.disabled = (
            cargando or self.pagina == 1
        )
        self.btn_siguiente.disabled = (
            cargando or not self.hay_mas
        )

        if cargando:
            self.boton_buscar.content = ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.ProgressRing(
                        width=18,
                        height=18,
                        stroke_width=2,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        "BUSCANDO...",
                        color=ft.Colors.WHITE,
                    ),
                ]
            )
        else:
            self.boton_buscar.content = ft.Text(
                "BUSCAR",
                color=ft.Colors.WHITE,
            )

        self.boton_buscar.update()
        self.btn_anterior.update()
        self.btn_siguiente.update()

    def aplicar_filtros(self, e):
        """Metodo para aplicar los filtros"""

        self.filtros_aplicados = (
            self.obtener_filtros()
        )

        asyncio.create_task(
            self.cerrar_panel(e)
        )

        asyncio.create_task(
            self.buscar(e)
        )

    def quitar_filtros(self, e):
        """Metodo para quitar todos los filtros y repetir la busqueda"""

        tipo = self.perfil.value

        self.filtros_aplicados = {
            "perfil": tipo
        }

        self.restaurar_filtros(
            self.filtros_aplicados
        )

        asyncio.create_task(
            self.cerrar_panel(e)
        )

        asyncio.create_task(
            self.buscar(e)
        )

    async def buscar(self, e):
        """Metodo para buscar segun texto y filtros"""

        if self.cargando:
            return

        self.cargando = True
        self._mostrar_cargando(True)

        try:
            self.consulta_actual = self.busqueda.value

            self.filtros_busqueda = (
                self.obtener_filtros_aplicados()
            )

            self.offsets_previos = []

            await self.cargar_resultados(
                0,
                1
            )

        finally:
            self.cargando = False
            self._mostrar_cargando(False)

    async def pagina_siguiente(self, e):
        """Metodo para ir a la pagina siguiente"""

        if self.cargando:
            return

        self.cargando = True
        self._mostrar_cargando(True)

        try:
            offset_actual = self.offset

            nuevo_offset = (
                self.offset
                + self.cantidad_actual
            )

            if await self.cargar_resultados(
                nuevo_offset,
                self.pagina + 1
            ):
                self.offsets_previos.append(
                    offset_actual
                )

        finally:
            self.cargando = False
            self._mostrar_cargando(False)

    async def pagina_anterior(self, e):
        """Metodo para ir a la pagina anterior"""

        if (
            self.cargando
            or not self.offsets_previos
        ):
            return

        self.cargando = True
        self._mostrar_cargando(True)

        try:
            if await self.cargar_resultados(
                self.offsets_previos[-1],
                self.pagina - 1
            ):
                self.offsets_previos.pop()

        finally:
            self.cargando = False
            self._mostrar_cargando(False)

    async def cargar_resultados(
        self,
        offset: int,
        pagina: int
    ):
        """Metodo para cargar una pagina"""

        tipo = self.filtros_busqueda.get(
            "perfil",
            "postulante"
        )

        if tipo == "postulante":
            resultados = await self.filtrar_postulantes(
                self.filtros_busqueda,
                offset
            )
        elif tipo == "empleador":
            resultados = await self.filtrar_empleadores(
                self.filtros_busqueda,
                offset
            )
        else:
            resultados = await self.filtrar_ofertas_laborales(
                self.filtros_busqueda,
                offset
            )

        if resultados is None:
            return False

        if not resultados and offset > 0:
            self.hay_mas = False
            self.btn_siguiente.disabled = True
            self.page.update()
            return False

        self.offset = offset
        self.pagina = pagina
        self.cantidad_actual = len(resultados)
        self.hay_mas = (
            len(resultados) >= self.tamano_pagina
        )

        self.mostrar_resultados(
            resultados,
            tipo
        )

        return True

    async def filtrar_postulantes(
        self,
        perfil: dict,
        offset: int
    ):
        """Metodo para buscar postulantes"""

        try:
            return await PostulanteService.buscar_postulantes(
                page=self.page,
                busqueda=self.consulta_actual,
                ubicacion=perfil.get("ubicacion"),
                estudios=perfil.get("estudios"),
                experiencias_laborales=perfil.get(
                    "experiencias_laborales"
                ),
                disponibilidad=perfil.get(
                    "disponibilidad"
                ),
                habilidades=perfil.get(
                    "habilidades",
                    []
                ),
                offset=offset,
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

            return None

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo realizar la búsqueda. "
                "Intente nuevamente"
            )

            return None

    async def filtrar_empleadores(
        self,
        perfil: dict,
        offset: int
    ):
        """Metodo para buscar empleadores"""

        try:
            return await EmpleadorService.buscar_empleadores(
                page=self.page,
                busqueda=self.consulta_actual,
                direccion=perfil.get(
                    "direccion"
                ),
                ubicacion=perfil.get(
                    "ubicacion"
                ),
                rubro=perfil.get(
                    "rubro"
                ),
                offset=offset,
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(2)

            await self.page.push_route(
                "/login"
            )

            return None

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo realizar la búsqueda. "
                "Intente nuevamente"
            )

            return None

    async def filtrar_ofertas_laborales(
        self,
        perfil: dict,
        offset: int
    ):
        """Metodo para buscar ofertas laborales"""

        try:
            return await OfertaLaboralService.buscar_ofertas_laborales(
                page=self.page,
                busqueda=self.consulta_actual,
                rubro=perfil.get(
                    "rubro"
                ),
                jornada=perfil.get(
                    "jornada"
                ),
                dias_laborales=perfil.get(
                    "dias_laborales",
                    []
                ),
                offset=offset,
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

            return None

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo realizar la búsqueda. "
                "Intente nuevamente"
            )

            return None

    def mostrar_resultados(
        self,
        resultados,
        tipo
    ):
        """Metodo para mostrar los resultados"""

        if resultados:
            self.lista_resultados.controls = [
                self.crear_card(
                    r,
                    tipo
                )
                for r in resultados
            ]
        else:
            self.lista_resultados.controls = [
                ft.Text(
                    "No se encontraron resultados",
                    color=ft.Colors.BLACK_54,
                    text_align=ft.TextAlign.CENTER
                )
            ]

        self.txt_pagina.value = (
            f"Página {self.pagina}"
        )

        self.btn_anterior.disabled = (
            self.pagina == 1
        )

        self.btn_siguiente.disabled = (
            not self.hay_mas
        )

        self.paginacion.visible = bool(
            resultados
        )

        self.page.update()

    def _mostrar_cargando_card(
        self,
        boton,
        cargando,
        texto_original
    ):
        """Actualiza visualmente el boton de una card"""

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
                ]
            )
        else:
            boton.content = ft.Text(
                texto_original,
                color=ft.Colors.BLUE_500,
            )

        boton.update()

    def crear_card(
        self,
        item: dict,
        tipo: str
    ):
        """Metodo para crear la card"""

        subtitulo = ""
        fila_subtitulo = None

        if tipo == "postulante":
            titulo = (
                f"{item.get('nombre', '')} "
                f"{item.get('apellido', '')}"
            ).strip()

            descripcion = (
                item.get(
                    "descripcion_personal"
                ) or ""
            )

            foto = item.get(
                "foto_perfil"
            )

            icono = ft.Icons.PERSON
            texto_boton = "VER PERFIL"

        elif tipo == "empleador":
            titulo = item.get(
                "nombre_negocio",
                ""
            )

            descripcion = (
                item.get(
                    "descripcion"
                ) or ""
            )

            foto = item.get(
                "foto_perfil"
            )

            icono = ft.Icons.BUSINESS
            texto_boton = "VER PERFIL"

        else:
            titulo = item.get(
                "titulo",
                ""
            )

            subtitulo = (
                f"{item.get('nombre_negocio', '')} · "
                f"{item.get('ubicacion', '')}"
            )

            descripcion = (
                item.get(
                    "descripcion"
                ) or ""
            )

            foto = item.get(
                "foto_perfil_empleador"
            )

            icono = ft.Icons.WORK_OUTLINE
            texto_boton = "VER OFERTA"

            fila_subtitulo = ft.Container(
                content=ft.Text(
                    subtitulo,
                    size=12,
                    color=ft.Colors.BLUE_500,
                    weight=ft.FontWeight.W_500,
                    style=ft.TextStyle(
                        decoration=(
                            ft.TextDecoration.UNDERLINE
                        )
                    ),
                ),
                padding=ft.Padding(
                    left=0,
                    top=2,
                    right=0,
                    bottom=2
                ),
                ink=True,
                border_radius=4,
                data=item,
                on_click=self.ver_perfil_empleador,
            )

        if fila_subtitulo is None:
            fila_subtitulo = ft.Text(
                subtitulo,
                size=12,
                color=ft.Colors.BLUE_GREY_400,
                visible=bool(
                    subtitulo
                )
            )

        avatar = ft.CircleAvatar(
            radius=40,
            bgcolor=ft.Colors.BLUE_GREY_100,
            foreground_image_src=(
                foto
                if foto
                else None
            ),
            content=(
                None
                if foto
                else ft.Icon(
                    icono,
                    size=36,
                    color=ft.Colors.BLUE_GREY_400
                )
            ),
        )

        boton_perfil = ft.OutlinedButton(
            content=ft.Text(
                texto_boton,
                color=ft.Colors.BLUE_500,
            ),
            data=item,
            on_click=self.ver_perfil,
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_500
            ),
        )

        self.textos_botones_cards[id(boton_perfil)] = (
            texto_boton
        )

        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            padding=15,
            shadow=ft.BoxShadow(
                blur_radius=12,
                spread_radius=0,
                offset=ft.Offset(0, 4),
                color=ft.Colors.BLACK_26,
            ),
            content=ft.Row(
                vertical_alignment=(
                    ft.CrossAxisAlignment.START
                ),
                spacing=15,
                controls=[
                    avatar,
                    ft.Column(
                        expand=True,
                        spacing=5,
                        controls=[
                            ft.Text(
                                titulo,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK_87
                            ),
                            fila_subtitulo,
                            ft.Text(
                                descripcion,
                                color=ft.Colors.BLACK_54,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS
                            ),
                            ft.Row(
                                alignment=(
                                    ft.MainAxisAlignment.END
                                ),
                                controls=[
                                    boton_perfil
                                ]
                            ),
                        ]
                    ),
                ]
            )
        )

    async def ver_perfil_empleador(self, e):
        """Navega al perfil del empleador dueño de una oferta"""

        try:
            item = e.control.data

            await self.perfil_empleador.cargar(
                self.page,
                item["empleador_id"]
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

    async def ir_a_mensajeria(self, e):
        """Metodo para navegar a la vista de mensajeria"""

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

    async def ver_perfil(self, e):
        """Metodo para navegar al perfil o a la oferta seleccionada."""

        boton = e.control
        clave = id(boton)

        if clave in self.botones_cards_cargando:
            return

        self.botones_cards_cargando.add(clave)

        texto_original = self.textos_botones_cards.get(
            clave,
            "VER PERFIL"
        )

        self._mostrar_cargando_card(
            boton,
            True,
            texto_original
        )

        try:
            item = boton.data

            tipo = self.filtros_busqueda.get(
                "perfil",
                "postulante"
            )

            if tipo == "empleador":
                await self.perfil_empleador.cargar(
                    page=self.page,
                    empleador_id=item["id"]
                )

                await self.page.push_route(
                    "/perfil-empleador"
                )

            elif tipo == "oferta":
                await self.perfil_oferta.cargar(
                    page=self.page,
                    oferta_id=item["id"]
                )

                await self.page.push_route(
                    "/perfil-oferta"
                )

            elif tipo == "postulante":
                await self.perfil_postulante.cargar(
                    page=self.page,
                    postulante_id=item["id"]
                )

                await self.page.push_route(
                    "/perfil-postulante"
                )

        finally:
            self.botones_cards_cargando.discard(clave)

            self._mostrar_cargando_card(
                boton,
                False,
                texto_original
            )

    def mostrar_mensaje(self, mensaje):
        """Metodo para mostrar los mensajes de excepciones"""

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    mensaje
                )
            )
        )

    async def cancelar_panel(self, e):
        """Metodo para cancelar el panel sin guardar cambios"""

        await self.cerrar_panel(e)

        self.restaurar_filtros(
            self.filtros_aplicados
        )

    def abrir_panel(self, e):
        """Metodo para abrir el panel de filtros"""

        self.modal_wrapper.visible = True
        self.panel_overlay.visible = True

        self.panel_modal.offset = ft.Offset(
            0,
            0
        )

        self.page.update()

    async def cerrar_panel(self, e):
        """Metodo para cerrar el panel de filtros"""

        self.panel_modal.offset = ft.Offset(
            0,
            2
        )

        self.panel_overlay.visible = False

        self.page.update()

        await asyncio.sleep(0.4)

        self.modal_wrapper.visible = False

        self.page.update()

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

    def did_mount(self):
        self._running = True

        self._tarea_mensajes = self.page.run_task(
            self.verificar_mensajes
        )

    def will_unmount(self):
        self.detener_verificacion_mensajes()

    def actualizar_badge_mensajes(self):
        """Actualiza el contador de mensajes no leídos."""

        cantidad = self.cantidad_mensajes_no_leidos

        self.badge_mensajes.content.value = (
            "99+"
            if cantidad > 99
            else str(cantidad)
        )

        self.badge_mensajes.visible = (
            cantidad > 0
        )

        self.badge_mensajes.update()

    async def verificar_mensajes(self):
        """Verifica periódicamente los mensajes no leídos."""

        try:
            while self._running:
                respuesta = (
                    await MensajeService.verificar_mensajes_no_leidos(
                        page=self.page
                    )
                )

                if not self._running:
                    return

                self.cantidad_mensajes_no_leidos = respuesta[
                    "cantidad_mensajes_no_leidos"
                ]

                self.actualizar_badge_mensajes()

                await asyncio.sleep(60)

        except asyncio.CancelledError:
            return

        except ErrorAutenticacion:
            self._running = False

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except ErrorServidor:
            if self._running:
                self.mostrar_mensaje(
                    "No se ha podido traer la cantidad "
                    "de mensajes no leídos"
                )

    def detener_verificacion_mensajes(self):
        self._running = False

        if self._tarea_mensajes:
            self._tarea_mensajes.cancel()
            self._tarea_mensajes = None