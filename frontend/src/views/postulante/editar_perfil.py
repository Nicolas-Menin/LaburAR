import asyncio
import mimetypes
import base64
import time
from datetime import date, datetime

import flet as ft
from frontend.src.services.postulante_service import PostulanteService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
    ErrorValidacion
)
from frontend.src.components.habilidades import HABILIDADES

# pylint: disable=E1121,E1123,E0401, E1101


class EditarPerfilPostulanteView(ft.View):

    def __init__(self):
        super().__init__()

        self.route = "/editar-perfil-postulante"
        self.padding = 0
        self.spacing = 0
        self.bgcolor = ft.Colors.BLUE_GREY_50

        self.bg_image = ft.Image(
            src="images/LaburAR_bg5.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.habilidades_disponibles = sorted(HABILIDADES)
        self.habilidades_seleccionadas = []
        self.estudios = []
        self.experiencias = []

        self.cargando_perfil = False
        self.cargando_estudio = False
        self.cargando_experiencia = False
        self.cargando_guardado = False
        self.cargando_foto = False

        self.ESTADOS_ESTUDIO = [
            "EN_CURSO",
            "NO_TERMINADO",
            "FINALIZADO"
        ]

        self.NIVELES_ESTUDIO = [
            "PRIMARIO",
            "SECUNDARIO",
            "UNIVERSITARIO",
            "TERCIARIO",
            "CURSO"
        ]

        self.TAMANO_MAXIMO_FOTO_MB = 5
        self.TAMANO_MAXIMO_CV_MB = 10

        self.cv_url = None
        self.cargando_cv = False

        self.dias_semana = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo"
        ]

        self.foto_perfil = ft.CircleAvatar(
            radius=45,
            bgcolor=ft.Colors.BLUE_50,
            content=ft.Icon(
                ft.Icons.PERSON_OUTLINE,
                size=40,
                color=ft.Colors.BLUE_900,
            ),
        )

        self.indicador_foto = ft.ProgressRing(
            width=32,
            height=32,
            stroke_width=3,
            color=ft.Colors.BLUE_500,
            visible=False,
        )

        self.btn_cambiar_foto = ft.IconButton(
            icon=ft.Icons.CAMERA_ALT_OUTLINED,
            icon_color=ft.Colors.WHITE,
            icon_size=16,
            bgcolor=ft.Colors.BLUE_500,
            width=30,
            height=30,
            padding=0,
            tooltip="Cambiar foto",
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
            ),
            on_click=self.cambiar_foto,
        )

        self.seccion_foto = ft.Row(
            spacing=20,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Stack(
                    width=90,
                    height=90,
                    controls=[
                        self.foto_perfil,
                        ft.Container(
                            width=90,
                            height=90,
                            alignment=ft.Alignment.CENTER,
                            content=self.indicador_foto,
                        ),
                        ft.Container(
                            right=0,
                            bottom=0,
                            content=self.btn_cambiar_foto,
                        ),
                    ],
                ),
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(
                            "Foto de perfil",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK_87,
                            size=14,
                        ),
                        ft.Text(
                            "JPG, PNG o WEBP · máximo "
                            f"{self.TAMANO_MAXIMO_FOTO_MB} MB",
                            color=ft.Colors.BLACK_45,
                            size=11,
                        ),
                        ft.TextButton(
                            "Cambiar foto",
                            style=ft.ButtonStyle(
                                color=ft.Colors.BLUE_500,
                                padding=ft.Padding(0, 0, 0, 0),
                            ),
                            on_click=self.cambiar_foto,
                        ),
                    ],
                ),
            ],
        )

        self.indicador_cv = ft.ProgressRing(
            width=16,
            height=16,
            stroke_width=2,
            color=ft.Colors.BLUE_500,
            visible=False,
        )

        self.txt_estado_cv = ft.Text(
            "Sin CV cargado",
            color=ft.Colors.BLACK_45,
            size=12,
        )

        self.btn_ver_cv = ft.TextButton(
            "Ver CV",
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_500,
                padding=ft.Padding(0, 0, 0, 0),
            ),
            on_click=self.ver_cv,
            visible=False,
        )

        self.btn_subir_cv = ft.TextButton(
            "Subir CV",
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_500,
                padding=ft.Padding(0, 0, 0, 0),
            ),
            on_click=self.cambiar_cv,
        )

        self.seccion_cv = ft.Row(
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=40,
                    height=40,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE_50,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        ft.Icons.DESCRIPTION_OUTLINED,
                        size=20,
                        color=ft.Colors.BLUE_700,
                    ),
                ),
                ft.Column(
                    expand=True,
                    spacing=2,
                    controls=[
                        ft.Text(
                            "Curriculum Vitae (CV)",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK_87,
                            size=14,
                        ),
                        ft.Row(
                            spacing=10,
                            controls=[
                                self.txt_estado_cv,
                                self.indicador_cv
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    spacing=4,
                    controls=[
                        self.btn_ver_cv,
                        self.btn_subir_cv
                    ],
                ),
            ],
        )

        self.txt_nombre = ft.TextField(
            label="Nombre",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
        )

        self.txt_apellido = ft.TextField(
            label="Apellido",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
        )

        self.dd_ubicacion = ft.Dropdown(
            label="Ubicación",
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            options=[
                ft.DropdownOption(
                    "Punta Alta",
                    content=ft.Text(
                        "Punta Alta",
                        color=ft.Colors.BLACK_87
                    )
                )
            ],
        )

        self.dd_disponibilidad = ft.Dropdown(
            label="Disponibilidad",
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            on_select=self.on_cambio_disponibilidad,
            options=[
                ft.DropdownOption(
                    "JORNADA_COMPLETA",
                    content=ft.Text(
                        "Jornada completa",
                        color=ft.Colors.BLACK_87
                    )
                ),
                ft.DropdownOption(
                    "MEDIA_JORNADA",
                    content=ft.Text(
                        "Media jornada",
                        color=ft.Colors.BLACK_87
                    )
                ),
                ft.DropdownOption(
                    "FINES_SEMANA",
                    content=ft.Text(
                        "Fines de semana",
                        color=ft.Colors.BLACK_87
                    )
                ),
                ft.DropdownOption(
                    "A_CONVENIR",
                    content=ft.Text(
                        "A convenir",
                        color=ft.Colors.BLACK_87
                    )
                ),
            ],
        )

        self.dd_dia_desde = ft.Dropdown(
            label="Desde",
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            options=[
                ft.DropdownOption(d)
                for d in self.dias_semana
            ],
            on_select=self.actualizar_dias_hasta,
        )

        self.dd_dia_hasta = ft.Dropdown(
            label="Hasta",
            hint_text="Elegí inicio...",
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            options=[],
            disabled=True,
        )

        self.fila_dias_especificos = ft.Row(
            spacing=15,
            visible=False,
            controls=[
                self.dd_dia_desde,
                self.dd_dia_hasta
            ],
        )

        self.txt_descripcion = ft.TextField(
            label="Descripción personal",
            hint_text="Contanos sobre vos...",
            multiline=True,
            min_lines=5,
            max_lines=5,
            expand=True,
            border_radius=10,
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
        )

        self.tarjeta_datos = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=15,
            padding=20,
            expand=True,
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
                    self._titulo_seccion(
                        "DATOS PERSONALES",
                        ft.Icons.PERSON_OUTLINE
                    ),
                    self.seccion_foto,
                    ft.Divider(
                        color=ft.Colors.BLUE_GREY_100,
                        height=1
                    ),
                    self.seccion_cv,
                    ft.Row(
                        spacing=15,
                        controls=[
                            self.txt_nombre,
                            self.txt_apellido,
                        ]
                    ),
                    ft.Row(
                        spacing=15,
                        controls=[
                            self.dd_ubicacion,
                            self.dd_disponibilidad,
                        ]
                    ),
                    self.fila_dias_especificos,
                    self.txt_descripcion,
                ]
            )
        )

        self.search_bar_habilidades = ft.SearchBar(
            view_bgcolor=ft.Colors.WHITE,
            bar_bgcolor=ft.Colors.WHITE,
            bar_hint_text="Buscar habilidad...",
            view_hint_text="Escribí para buscar...",
            view_header_text_style=ft.TextStyle(
                color=ft.Colors.BLACK
            ),
            bar_elevation=0,
            view_elevation=4,
            divider_color=ft.Colors.BLUE_GREY_100,
            on_change=self.filtrar_habilidades,
            on_tap=self.abrir_vista_habilidades,
            controls=self.crear_tiles_habilidades(
                self.habilidades_disponibles
            ),
        )

        self.row_habilidades = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8,
        )

        self.contenedor_habilidades_seleccionadas = ft.Container(
            height=340,
            width=900,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=10,
            padding=10,
            bgcolor=ft.Colors.BLUE_GREY_50,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    self.row_habilidades
                ]
            )
        )

        self.tarjeta_habilidades = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=15,
            padding=20,
            expand=True,
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
                expand=True,
                spacing=15,
                controls=[
                    self._titulo_seccion(
                        "HABILIDADES",
                        ft.Icons.STAR_OUTLINE
                    ),
                    self.search_bar_habilidades,
                    ft.Text(
                        "Seleccionadas:",
                        size=12,
                        color=ft.Colors.BLACK_45,
                    ),
                    self.contenedor_habilidades_seleccionadas,
                ]
            )
        )

        self.lista_estudios = ft.Column(
            spacing=10
        )

        self.tarjeta_estudios = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=15,
            padding=20,
            expand=True,
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
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self._titulo_seccion(
                                "ESTUDIOS",
                                ft.Icons.SCHOOL_OUTLINED
                            ),
                            self._boton_agregar(
                                self.abrir_form_estudio
                            ),
                        ]
                    ),
                    self.lista_estudios,
                ]
            )
        )

        self.lista_experiencias = ft.Column(
            spacing=10
        )

        self.tarjeta_experiencias = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=15,
            padding=20,
            expand=True,
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
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self._titulo_seccion(
                                "EXPERIENCIAS LABORALES",
                                ft.Icons.WORK_OUTLINE
                            ),
                            self._boton_agregar(
                                self.abrir_form_experiencia
                            ),
                        ]
                    ),
                    self.lista_experiencias,
                ]
            )
        )

        self.btn_guardar = ft.Button(
            content=self._contenido_guardar(),
            height=50,
            width=220,
            on_click=self.guardar,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(
                    radius=15
                )
            )
        )

        self.indicador_carga = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.ProgressRing(
                    width=40,
                    height=40,
                    stroke_width=4,
                    color=ft.Colors.BLUE_500,
                ),
                ft.Text(
                    "Cargando perfil...",
                    color=ft.Colors.BLACK_54,
                    size=14,
                ),
            ]
        )

        self.contenedor_carga = ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=self.indicador_carga,
        )

        self.encabezado = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
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
                ft.Text(
                    "Editar perfil",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK_87,
                ),
            ]
        )

        self.contenido_principal = ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.Column(
                            expand=True,
                            scroll=ft.Scrollbar(
                                thumb_visibility=True,
                                track_visibility=True,
                                thickness=8,
                            ),
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.STRETCH
                            ),
                            spacing=20,
                            controls=[
                                self.encabezado,
                                ft.Row(
                                    expand=True,
                                    spacing=20,
                                    vertical_alignment=(
                                        ft.CrossAxisAlignment.START
                                    ),
                                    controls=[
                                        self.tarjeta_datos,
                                        self.tarjeta_habilidades,
                                    ],
                                ),
                                ft.Row(
                                    spacing=20,
                                    vertical_alignment=(
                                        ft.CrossAxisAlignment.START
                                    ),
                                    controls=[
                                        self.tarjeta_estudios,
                                        self.tarjeta_experiencias,
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        self.btn_guardar
                    ],
                ),
            ],
        )

        self.contenedor_principal = ft.Container(
            expand=True,
            padding=20,
            content=self.contenido_principal,
            visible=False,
        )

        self.controls = [
            ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        content=self.bg_image,
                    ),
                    self.contenedor_carga,
                    self.contenedor_principal,
                ],
            )
        ]

    def _titulo_seccion(self, texto, icono):
        return ft.Row(
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    icono,
                    size=16,
                    color=ft.Colors.BLUE_500,
                ),
                ft.Text(
                    texto,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK_54,
                    size=12,
                ),
            ]
        )

    def _boton_agregar(self, on_click):
        return ft.TextButton(
            content=ft.Row(
                tight=True,
                spacing=4,
                controls=[
                    ft.Icon(
                        ft.Icons.ADD,
                        size=16,
                        color=ft.Colors.BLUE_500,
                    ),
                    ft.Text(
                        "Agregar",
                        color=ft.Colors.BLUE_500,
                        size=13,
                    ),
                ]
            ),
            on_click=on_click,
        )

    def _contenido_guardar(self):
        return ft.Row(
            tight=True,
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.SAVE_OUTLINED,
                    color=ft.Colors.WHITE,
                    size=18,
                ),
                ft.Text(
                    "GUARDAR CAMBIOS"
                ),
            ]
        )

    def _contenido_guardando(self):
        return ft.Row(
            tight=True,
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ProgressRing(
                    width=16,
                    height=16,
                    stroke_width=2,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    "Guardando...",
                    color=ft.Colors.WHITE,
                ),
            ]
        )

    @staticmethod
    def _parsear_fecha(valor):
        """Convierte la fecha que llega del backend ("2024-03-01") en date."""

        if not valor:
            return None

        if isinstance(valor, datetime):
            return valor.date()

        if isinstance(valor, date):
            return valor

        try:
            return datetime.fromisoformat(
                str(valor)
            ).date()
        except ValueError:
            return None

    def _crear_selector_fecha(
        self,
        label: str,
        opcional: bool = False,
        fecha_inicial=None
    ):
        estado = {
            "fecha": fecha_inicial
        }

        txt_valor = ft.Text(
            (
                fecha_inicial.strftime("%d/%m/%Y")
                if fecha_inicial
                else (
                    "Sin seleccionar"
                    if opcional
                    else "Tocá para elegir"
                )
            ),
            color=(
                ft.Colors.BLACK_87
                if fecha_inicial
                else ft.Colors.BLACK_45
            ),
            size=13,
        )

        date_picker = ft.DatePicker(
            value=(
                datetime(
                    fecha_inicial.year,
                    fecha_inicial.month,
                    fecha_inicial.day
                )
                if fecha_inicial
                else None
            ),
            current_date=datetime.now(),
            first_date=datetime(
                1950,
                1,
                1
            ),
            last_date=datetime(
                2100,
                12,
                31
            ),
        )

        def al_cambiar(e):
            if date_picker.value:
                estado["fecha"] = (
                    date_picker.value.date()
                )

                txt_valor.value = (
                    estado["fecha"].strftime(
                        "%d/%m/%Y"
                    )
                )

                txt_valor.color = (
                    ft.Colors.BLACK_87
                )

            self.page.update()

        date_picker.on_change = al_cambiar

        def abrir(e):
            self.page.show_dialog(
                date_picker
            )

        control = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_200
            ),
            border_radius=10,
            padding=ft.Padding(
                left=12,
                top=6,
                right=4,
                bottom=6
            ),
            on_click=abrir,
            expand=True,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text(
                                label,
                                size=11,
                                color=ft.Colors.BLACK_45,
                            ),
                            txt_valor,
                        ]
                    ),
                    ft.Icon(
                        ft.Icons.CALENDAR_MONTH,
                        color=ft.Colors.BLUE_500,
                        size=20,
                    ),
                ]
            )
        )

        return control, lambda: estado["fecha"]

    @staticmethod
    def _url_sin_cache(url: str) -> str:
        """Agrega un parametro a la URL para evitar cache."""

        separador = "&" if "?" in url else "?"

        return (
            f"{url}"
            f"{separador}"
            f"v={int(time.time())}"
        )

    def _mostrar_foto(
        self,
        foto: str | None,
        evitar_cache: bool = False
    ):
        """Muestra la foto de perfil o el icono por defecto."""

        if foto:
            self.foto_perfil.foreground_image_src = (
                self._url_sin_cache(foto)
                if evitar_cache
                else foto
            )

            self.foto_perfil.content = None
        else:
            self.foto_perfil.foreground_image_src = None

            self.foto_perfil.content = ft.Icon(
                ft.Icons.PERSON_OUTLINE,
                size=40,
                color=ft.Colors.BLUE_900,
            )

    def _mostrar_cargando_foto(self, cargando: bool):
        self.cargando_foto = cargando

        self.indicador_foto.visible = cargando
        self.btn_cambiar_foto.disabled = cargando

        self.page.update()

    async def cambiar_foto(self, e):
        """Metodo para elegir una imagen y actualizar la foto."""

        if self.cargando_foto:
            return

        archivos = await ft.FilePicker().pick_files(
            dialog_title="Elegir foto de perfil",
            file_type=ft.FilePickerFileType.IMAGE,
            allowed_extensions=[
                "png",
                "jpg",
                "jpeg"
            ],
            allow_multiple=False,
            with_data=True,
        )

        if not archivos:
            return

        archivo = archivos[0]

        if not archivo.bytes:
            self.mostrar_mensaje(
                "No se pudo leer la imagen seleccionada"
            )
            return

        limite_bytes = (
            self.TAMANO_MAXIMO_FOTO_MB
            * 1024
            * 1024
        )

        if archivo.size and archivo.size > limite_bytes:
            self.mostrar_mensaje(
                "La imagen supera el tamaño máximo de "
                f"{self.TAMANO_MAXIMO_FOTO_MB} MB"
            )
            return

        self._mostrar_cargando_foto(True)

        try:
            tipo_contenido = (
                mimetypes.guess_type(
                    archivo.name
                )[0]
                or "image/jpeg"
            )

            foto_base64 = (
                f"data:{tipo_contenido};base64,"
                + base64.b64encode(
                    archivo.bytes
                ).decode("ascii")
            )

            resultado = (
                await PostulanteService.actualizar_postulante(
                    self.page,
                    foto_perfil=foto_base64,
                )
            )

            foto = (
                (resultado or {})
                .get("foto_perfil")
            )

            if foto:
                self._mostrar_foto(
                    foto,
                    evitar_cache=True
                )

            self.mostrar_mensaje(
                "Foto de perfil actualizada correctamente"
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except (
            ErrorServidor,
            ErrorValidacion
        ):
            self.mostrar_mensaje(
                "No se pudo actualizar la foto de perfil. "
                "Intente nuevamente"
            )

        finally:
            self._mostrar_cargando_foto(False)

    def _mostrar_estado_cv(self):
        """Refleja si hay o no CV cargado."""

        if self.cv_url:
            self.txt_estado_cv.value = (
                "CV cargado"
            )

            self.txt_estado_cv.color = (
                ft.Colors.BLACK_87
            )

            self.btn_ver_cv.visible = True
            self.btn_subir_cv.text = "Cambiar CV"
        else:
            self.txt_estado_cv.value = (
                "Sin CV cargado"
            )

            self.txt_estado_cv.color = (
                ft.Colors.BLACK_45
            )

            self.btn_ver_cv.visible = False
            self.btn_subir_cv.text = "Subir CV"

    def _mostrar_cargando_cv(self, cargando: bool):
        self.cargando_cv = cargando

        self.indicador_cv.visible = cargando
        self.btn_subir_cv.disabled = cargando
        self.btn_ver_cv.disabled = cargando

        self.page.update()

    async def ver_cv(self, e):
        """Metodo para visualizar el CV."""

        if not self.cv_url:
            return

        launcher = ft.UrlLauncher()

        await launcher.launch_url(
            self.cv_url
        )

    async def cambiar_cv(self, e):
        """Metodo para elegir un PDF y actualizar el CV."""

        if self.cargando_cv:
            return

        archivos = await ft.FilePicker().pick_files(
            dialog_title="Elegir CV",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["pdf"],
            allow_multiple=False,
            with_data=True,
        )

        if not archivos:
            return

        archivo = archivos[0]

        if not archivo.bytes:
            self.mostrar_mensaje(
                "No se pudo leer el archivo seleccionado"
            )
            return

        limite_bytes = (
            self.TAMANO_MAXIMO_CV_MB
            * 1024
            * 1024
        )

        if archivo.size and archivo.size > limite_bytes:
            self.mostrar_mensaje(
                "El archivo supera el tamaño máximo de "
                f"{self.TAMANO_MAXIMO_CV_MB} MB"
            )
            return

        self._mostrar_cargando_cv(True)

        try:
            tipo_contenido = (
                mimetypes.guess_type(
                    archivo.name
                )[0]
                or "application/pdf"
            )

            cv_base64 = (
                f"data:{tipo_contenido};base64,"
                + base64.b64encode(
                    archivo.bytes
                ).decode("ascii")
            )

            resultado = (
                await PostulanteService.actualizar_postulante(
                    self.page,
                    cv=cv_base64,
                )
            )

            self.cv_url = (
                (resultado or {}).get("cv_url")
                or (resultado or {}).get("cv")
            )

            self._mostrar_estado_cv()

            self.mostrar_mensaje(
                "CV actualizado correctamente"
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except (
            ErrorServidor,
            ErrorValidacion
        ):
            self.mostrar_mensaje(
                "No se pudo actualizar el CV. "
                "Intente nuevamente"
            )

        finally:
            self._mostrar_cargando_cv(False)

    def on_cambio_disponibilidad(self, e):
        """Muestra los días cuando corresponde."""

        self.fila_dias_especificos.visible = (
            e.control.value == "DIAS_ESPECIFICOS"
        )

        self.update()

    def configurar_dias_hasta(self):
        """Configura las opciones del dropdown Hasta."""

        dia_desde = self.dd_dia_desde.value

        if dia_desde:
            idx_inicio = (
                self.dias_semana.index(
                    dia_desde
                )
            )

            self.dd_dia_hasta.options = [
                ft.DropdownOption(d)
                for d in self.dias_semana[
                    idx_inicio:
                ]
            ]

            self.dd_dia_hasta.hint_text = (
                "Elegí fin..."
            )

            self.dd_dia_hasta.disabled = False

            if (
                self.dd_dia_hasta.value
                and self.dias_semana.index(
                    self.dd_dia_hasta.value
                ) < idx_inicio
            ):
                self.dd_dia_hasta.value = None
        else:
            self.dd_dia_hasta.options = []

            self.dd_dia_hasta.hint_text = (
                "Elegí inicio..."
            )

            self.dd_dia_hasta.value = None

            self.dd_dia_hasta.disabled = True

    def actualizar_dias_hasta(self, e):
        """Actualiza el dropdown Hasta."""

        self.configurar_dias_hasta()

        self.dd_dia_hasta.update()

    async def cargar(self, page):
        self.cargando_perfil = True

        self.contenedor_carga.visible = True
        self.contenedor_principal.visible = False

        self.indicador_carga.controls[1].value = (
            "Cargando perfil..."
        )

        self.update()

        try:
            datos = await PostulanteService.perfil(
                page
            )

            self.mostrar_datos(
                datos
            )

            self.contenedor_carga.visible = False
            self.contenedor_principal.visible = True

            self.update()

        except ErrorAutenticacion:
            self.contenedor_carga.visible = False

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except ErrorServidor:
            self.contenedor_carga.visible = False

            self.update()

            self.mostrar_mensaje(
                "No se pudo cargar el perfil. "
                "Intente nuevamente"
            )

        finally:
            self.cargando_perfil = False

    def mostrar_datos(self, datos):
        self.txt_nombre.value = datos.get(
            "nombre",
            ""
        )

        self.txt_apellido.value = datos.get(
            "apellido",
            ""
        )

        self.dd_ubicacion.value = datos.get(
            "ubicacion",
            ""
        )

        self.dd_disponibilidad.value = datos.get(
            "disponibilidad",
            ""
        )

        self.txt_descripcion.value = datos.get(
            "descripcion_personal",
            ""
        )

        self._mostrar_foto(
            datos.get(
                "foto_perfil"
            )
        )

        self.cv_url = (
            datos.get("cv_url")
            or datos.get("cv")
            or datos.get("curriculum_vitae")
        )

        self._mostrar_estado_cv()

        dias_laborales = (
            datos.get("dias_laborales")
            or []
        )

        self.fila_dias_especificos.visible = (
            self.dd_disponibilidad.value
            == "DIAS_ESPECIFICOS"
        )

        if dias_laborales:
            self.dd_dia_desde.value = (
                dias_laborales[0]
            )

            self.configurar_dias_hasta()

            self.dd_dia_hasta.value = (
                dias_laborales[-1]
            )

        self.habilidades_seleccionadas = list(
            datos.get(
                "habilidades",
                []
            )
        )

        self.renderizar_etiquetas()

        self.estudios = list(
            datos.get(
                "estudios",
                []
            )
        )

        self.renderizar_estudios()

        self.experiencias = list(
            datos.get(
                "experiencias_laborales",
                []
            )
        )

        self.renderizar_experiencias()

    def crear_tiles_habilidades(self, habilidades):
        return [
            ft.ListTile(
                title=ft.Text(
                    habilidad,
                    color=ft.Colors.BLACK,
                ),
                on_click=(
                    self.seleccionar_habilidad_desde_busqueda
                ),
                bgcolor=ft.Colors.WHITE,
            )
            for habilidad in habilidades
        ]

    async def abrir_vista_habilidades(self, e):
        await self.search_bar_habilidades.open_view()

    def filtrar_habilidades(self, e):
        texto = (
            e.control.value or ""
        ).lower().strip()

        self.search_bar_habilidades.controls = (
            self.crear_tiles_habilidades(
                [
                    habilidad
                    for habilidad in self.habilidades_disponibles
                    if texto in habilidad.lower()
                ]
            )
        )

        self.page.update()

    async def seleccionar_habilidad_desde_busqueda(
        self,
        e
    ):
        nombre = e.control.title.value

        await self.search_bar_habilidades.close_view(
            nombre
        )

        if not nombre:
            return

        if any(
            habilidad.get("nombre") == nombre
            for habilidad in self.habilidades_seleccionadas
        ):
            return

        try:
            creada = (
                await PostulanteService.crear_habilidad(
                    self.page,
                    nombre=nombre
                )
            )

            self.habilidades_seleccionadas.append(
                creada
            )

            self.renderizar_etiquetas()

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except (
            ErrorServidor,
            ErrorValidacion
        ):
            self.mostrar_mensaje(
                "No se pudo agregar la habilidad. "
                "Intentá nuevamente"
            )

    async def remover_habilidad(self, e):
        habilidad = e.control.data

        try:
            await PostulanteService.eliminar_habilidad(
                self.page,
                habilidad_id=habilidad["id"]
            )

            if habilidad in self.habilidades_seleccionadas:
                self.habilidades_seleccionadas.remove(
                    habilidad
                )

                self.renderizar_etiquetas()

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo quitar la habilidad. "
                "Intentá nuevamente"
            )

    def renderizar_etiquetas(self):
        if not self.habilidades_seleccionadas:
            self.row_habilidades.controls = [
                ft.Text(
                    "Todavía no agregaste habilidades",
                    color=ft.Colors.BLACK_45,
                    size=12,
                )
            ]

            return

        self.row_habilidades.controls = [
            ft.Container(
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
                        ft.Text(
                            habilidad.get(
                                "nombre",
                                ""
                            ),
                            color=ft.Colors.BLUE_900,
                            weight=ft.FontWeight.W_500,
                            size=12,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=ft.Colors.BLUE_900,
                            icon_size=14,
                            width=20,
                            height=20,
                            padding=0,
                            data=habilidad,
                            on_click=self.remover_habilidad,
                        ),
                    ]
                )
            )
            for habilidad in self.habilidades_seleccionadas
        ]

    def _formatear_estado_estudio(self, estado):
        if not estado:
            return ""

        return estado.replace(
            "_",
            " "
        )

    def _formatear_nivel_estudio(self, nivel):
        if not nivel:
            return ""

        return nivel.capitalize()

    def _tarjeta_item(
        self,
        titulo,
        subtitulo,
        icono,
        data,
        on_click_borrar,
        on_click_editar=None
    ):
        acciones = []

        if on_click_editar:
            acciones.append(
                ft.IconButton(
                    icon=ft.Icons.EDIT_OUTLINED,
                    icon_color=ft.Colors.BLUE_500,
                    icon_size=18,
                    tooltip="Editar",
                    data=data,
                    on_click=on_click_editar,
                )
            )

        acciones.append(
            ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=ft.Colors.RED_400,
                icon_size=18,
                tooltip="Eliminar",
                data=data,
                on_click=on_click_borrar,
            )
        )

        return ft.Container(
            bgcolor=ft.Colors.BLUE_GREY_50,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100
            ),
            border_radius=10,
            padding=12,
            content=ft.Row(
                spacing=10,
                vertical_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                controls=[
                    ft.Container(
                        width=34,
                        height=34,
                        border_radius=17,
                        bgcolor=ft.Colors.BLUE_100,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            icono,
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
                                overflow=(
                                    ft.TextOverflow.ELLIPSIS
                                ),
                            ),
                            ft.Text(
                                subtitulo,
                                size=11,
                                color=ft.Colors.BLACK_54,
                                max_lines=2,
                                overflow=(
                                    ft.TextOverflow.ELLIPSIS
                                ),
                            ),
                        ]
                    ),
                    *acciones,
                ]
            )
        )

    def renderizar_estudios(self):
        if not self.estudios:
            self.lista_estudios.controls = [
                ft.Text(
                    "Todavía no agregaste estudios",
                    color=ft.Colors.BLACK_45,
                    size=12,
                )
            ]

            return

        self.lista_estudios.controls = [
            self._tarjeta_item(
                titulo=(
                    f"{estudio.get('titulo', '')} · "
                    f"{estudio.get('institucion', '')}"
                ),
                subtitulo=(
                    f"{self._formatear_nivel_estudio(
                        estudio.get('nivel')
                    )}"
                    f" · "
                    f"{self._formatear_estado_estudio(
                        estudio.get('estado')
                    )}"
                ),
                icono=ft.Icons.SCHOOL_OUTLINED,
                data=estudio,
                on_click_borrar=self.remover_estudio,
                on_click_editar=(
                    self.abrir_form_edicion_estudio
                ),
            )
            for estudio in self.estudios
        ]

    async def remover_estudio(self, e):
        estudio = e.control.data

        try:
            await PostulanteService.eliminar_estudio(
                self.page,
                estudio_id=estudio["id"]
            )

            if estudio in self.estudios:
                self.estudios.remove(
                    estudio
                )

                self.renderizar_estudios()

                self.page.update()

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo quitar el estudio. "
                "Intentá nuevamente"
            )

    async def abrir_form_edicion_estudio(self, e):
        """Abre el formulario de estudio con sus datos."""

        await self.abrir_form_estudio(
            e,
            estudio=e.control.data
        )

    async def abrir_form_estudio(
        self,
        e,
        estudio=None
    ):
        """Formulario para crear o editar un estudio."""

        editando = estudio is not None

        datos = estudio or {}

        texto_boton = (
            "Guardar"
            if editando
            else "Agregar"
        )

        txt_institucion = ft.TextField(
            label="Institución",
            value=datos.get("institucion") or "",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
        )

        txt_titulo = ft.TextField(
            label="Título / Carrera",
            value=datos.get("titulo") or "",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
        )

        dd_nivel = ft.Dropdown(
            label="Nivel",
            value=datos.get("nivel"),
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            menu_style=ft.MenuStyle(
                bgcolor=ft.Colors.WHITE,
                elevation=4,
                shape=ft.RoundedRectangleBorder(
                    radius=10
                ),
            ),
            options=[
                ft.DropdownOption(
                    nivel,
                    content=ft.Text(
                        nivel.capitalize(),
                        color=ft.Colors.BLACK_87,
                    ),
                )
                for nivel in self.NIVELES_ESTUDIO
            ],
        )

        dd_estado = ft.Dropdown(
            label="Estado",
            value=datos.get("estado"),
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            menu_style=ft.MenuStyle(
                bgcolor=ft.Colors.WHITE,
                elevation=4,
                shape=ft.RoundedRectangleBorder(
                    radius=10
                ),
            ),
            options=[
                ft.DropdownOption(
                    estado,
                    content=ft.Text(
                        estado.replace("_", " "),
                        color=ft.Colors.BLACK_87,
                    ),
                )
                for estado in self.ESTADOS_ESTUDIO
            ],
        )

        selector_inicio, obtener_fecha_inicio = (
            self._crear_selector_fecha(
                "Fecha de inicio",
                fecha_inicial=self._parsear_fecha(
                    datos.get("fecha_inicio")
                )
            )
        )

        selector_fin, obtener_fecha_fin = (
            self._crear_selector_fecha(
                "Fecha de fin",
                opcional=True,
                fecha_inicial=self._parsear_fecha(
                    datos.get("fecha_fin")
                )
            )
        )

        txt_error = ft.Text(
            "",
            color=ft.Colors.RED_500,
            size=12,
        )

        async def agregar(e):
            if self.cargando_estudio:
                return

            institucion = (
                txt_institucion.value.strip()
            )

            titulo = (
                txt_titulo.value.strip()
            )

            nivel = dd_nivel.value
            estado = dd_estado.value

            fecha_inicio = (
                obtener_fecha_inicio()
            )

            fecha_fin = (
                obtener_fecha_fin()
            )

            if not institucion:
                txt_error.value = (
                    "Ingrese la institución."
                )

                self.update()

                return

            if not titulo:
                txt_error.value = (
                    "Ingrese el título o carrera."
                )

                self.update()

                return

            if not nivel:
                txt_error.value = (
                    "Seleccione el nivel."
                )

                self.update()

                return

            if not estado:
                txt_error.value = (
                    "Seleccione el estado."
                )

                self.update()

                return

            if not fecha_inicio:
                txt_error.value = (
                    "Seleccione la fecha de inicio."
                )

                self.update()

                return

            if fecha_fin and fecha_fin < fecha_inicio:
                txt_error.value = (
                    "La fecha de fin no puede ser "
                    "anterior a la fecha de inicio"
                )

                txt_error.visible = True

                self.page.update()

                return

            self.cargando_estudio = True

            btn_agregar.disabled = True

            btn_agregar.content = ft.Row(
                tight=True,
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.ProgressRing(
                        width=16,
                        height=16,
                        stroke_width=2,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        "Guardando...",
                        color=ft.Colors.WHITE,
                    ),
                ],
            )

            self.update()

            try:
                if editando:
                    actualizado = (
                        await PostulanteService
                        .actualizar_estudio(
                            page=self.page,
                            estudio_id=estudio["id"],
                            institucion=institucion,
                            titulo=titulo,
                            nivel=nivel,
                            estado=estado,
                            fecha_inicio=fecha_inicio,
                            fecha_fin=fecha_fin
                        )
                    )

                    estudio.update(
                        {
                            "institucion": institucion,
                            "titulo": titulo,
                            "nivel": nivel,
                            "estado": estado,
                            "fecha_inicio": fecha_inicio,
                            "fecha_fin": fecha_fin,
                        }
                    )

                    if isinstance(
                        actualizado,
                        dict
                    ):
                        estudio.update(
                            actualizado
                        )
                else:
                    creado = (
                        await PostulanteService
                        .crear_estudio(
                            page=self.page,
                            institucion=institucion,
                            titulo=titulo,
                            nivel=nivel,
                            estado=estado,
                            fecha_inicio=fecha_inicio,
                            fecha_fin=(
                                fecha_fin
                                if fecha_fin
                                else None
                            ),
                        )
                    )

                    self.estudios.append(
                        creado
                    )

                self.renderizar_estudios()

                self.page.pop_dialog()

                self.update()

            except ErrorAutenticacion:
                self.page.pop_dialog()

                self.update()

                self.mostrar_dialogo_sesion_expirada()

                await asyncio.sleep(5)

                await self.page.push_route(
                    "/login"
                )

            except ErrorValidacion:
                txt_error.value = (
                    "Los datos ingresados no son válidos."
                )

                btn_agregar.disabled = False

                btn_agregar.content = ft.Text(
                    texto_boton,
                    color=ft.Colors.WHITE,
                )

                self.update()

            except ErrorServidor:
                txt_error.value = (
                    "No se pudo guardar el estudio. "
                    "Intente nuevamente."
                )

                btn_agregar.disabled = False

                btn_agregar.content = ft.Text(
                    texto_boton,
                    color=ft.Colors.WHITE,
                )

                self.update()

            finally:
                self.cargando_estudio = False

        btn_agregar = ft.Button(
            texto_boton,
            on_click=agregar,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(
                    radius=10
                ),
            ),
        )

        dialogo = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.WHITE,
            title=ft.Text(
                (
                    "Editar estudio"
                    if editando
                    else "Agregar estudio"
                ),
                color=ft.Colors.BLACK_87,
                weight=ft.FontWeight.BOLD,
            ),
            content=ft.Column(
                tight=True,
                spacing=10,
                width=330,
                controls=[
                    txt_institucion,
                    txt_titulo,
                    ft.Row(
                        spacing=10,
                        controls=[
                            dd_nivel,
                            dd_estado,
                        ],
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                            selector_inicio,
                            selector_fin,
                        ],
                    ),
                    txt_error,
                ],
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLUE_500,
                    ),
                    on_click=lambda e:
                    self.page.pop_dialog(),
                ),
                btn_agregar,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.show_dialog(
            dialogo
        )

    def renderizar_experiencias(self):
        if not self.experiencias:
            self.lista_experiencias.controls = [
                ft.Text(
                    "Todavía no agregaste experiencias laborales",
                    color=ft.Colors.BLACK_45,
                    size=12,
                )
            ]

            return

        self.lista_experiencias.controls = [
            self._tarjeta_item(
                titulo=(
                    f"{experiencia.get('puesto', '')} · "
                    f"{experiencia.get('empresa', '')}"
                ),
                subtitulo=(
                    f"{experiencia.get('area', '')} — "
                    f"{experiencia.get('descripcion', '')}"
                ),
                icono=ft.Icons.WORK_OUTLINE,
                data=experiencia,
                on_click_borrar=(
                    self.remover_experiencia
                ),
                on_click_editar=(
                    self.abrir_form_edicion_experiencia
                ),
            )
            for experiencia in self.experiencias
        ]

    async def remover_experiencia(self, e):
        experiencia = e.control.data

        try:
            await (
                PostulanteService
                .eliminar_experiencia_laboral(
                    self.page,
                    experiencia_laboral_id=(
                        experiencia["id"]
                    )
                )
            )

            if experiencia in self.experiencias:
                self.experiencias.remove(
                    experiencia
                )

                self.renderizar_experiencias()

                self.page.update()

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo quitar la experiencia. "
                "Intentá nuevamente"
            )

    async def abrir_form_edicion_experiencia(
        self,
        e
    ):
        """Abre el formulario de experiencia."""

        await self.abrir_form_experiencia(
            e,
            experiencia=e.control.data
        )

    async def abrir_form_experiencia(
        self,
        e,
        experiencia=None
    ):
        """Formulario para crear o editar experiencia."""

        if self.cargando_experiencia:
            return

        editando = experiencia is not None

        datos = experiencia or {}

        texto_boton = (
            "Guardar"
            if editando
            else "Agregar"
        )

        txt_empresa = ft.TextField(
            label="Empresa",
            value=datos.get("empresa") or "",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
        )

        txt_puesto = ft.TextField(
            label="Puesto",
            value=datos.get("puesto") or "",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
        )

        txt_area = ft.TextField(
            label="Área",
            value=datos.get("area") or "",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
        )

        txt_descripcion = ft.TextField(
            label="Descripción",
            value=datos.get("descripcion") or "",
            multiline=True,
            min_lines=2,
            max_lines=4,
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
        )

        selector_inicio, obtener_fecha_inicio = (
            self._crear_selector_fecha(
                "Fecha de inicio",
                fecha_inicial=self._parsear_fecha(
                    datos.get("fecha_inicio")
                )
            )
        )

        selector_fin, obtener_fecha_fin = (
            self._crear_selector_fecha(
                "Fecha de fin",
                fecha_inicial=self._parsear_fecha(
                    datos.get("fecha_fin")
                )
            )
        )

        txt_error = ft.Text(
            color=ft.Colors.RED_400,
            size=12,
            visible=False,
        )

        async def agregar(e):
            if self.cargando_experiencia:
                return

            fecha_inicio = (
                obtener_fecha_inicio()
            )

            fecha_fin = (
                obtener_fecha_fin()
            )

            if (
                not txt_empresa.value
                or not txt_puesto.value
                or not txt_area.value
            ):
                txt_error.value = (
                    "Completá todos los campos obligatorios"
                )

                txt_error.visible = True

                self.page.update()

                return

            if not fecha_inicio:
                txt_error.value = (
                    "Elegí la fecha de inicio"
                )

                txt_error.visible = True

                self.page.update()

                return

            self.cargando_experiencia = True

            btn_agregar.disabled = True

            btn_agregar.content = ft.Row(
                tight=True,
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.ProgressRing(
                        width=16,
                        height=16,
                        stroke_width=2,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        "Guardando...",
                        color=ft.Colors.WHITE,
                    ),
                ]
            )

            self.page.update()

            try:
                if editando:
                    actualizada = (
                        await PostulanteService
                        .actualizar_experiencia_laboral(
                            self.page,
                            experiencia_laboral_id=(
                                experiencia["id"]
                            ),
                            empresa=(
                                txt_empresa.value
                            ),
                            puesto=(
                                txt_puesto.value
                            ),
                            fecha_inicio=fecha_inicio,
                            fecha_fin=fecha_fin,
                            descripcion=(
                                txt_descripcion.value
                                or ""
                            ),
                            area=(
                                txt_area.value
                            ),
                        )
                    )

                    experiencia.update(
                        {
                            "empresa": (
                                txt_empresa.value
                            ),
                            "puesto": (
                                txt_puesto.value
                            ),
                            "fecha_inicio": fecha_inicio,
                            "fecha_fin": fecha_fin,
                            "descripcion": (
                                txt_descripcion.value
                                or ""
                            ),
                            "area": (
                                txt_area.value
                            ),
                        }
                    )

                    if isinstance(
                        actualizada,
                        dict
                    ):
                        experiencia.update(
                            actualizada
                        )
                else:
                    creada = (
                        await PostulanteService
                        .crear_experiencia_laboral(
                            self.page,
                            empresa=(
                                txt_empresa.value
                            ),
                            puesto=(
                                txt_puesto.value
                            ),
                            fecha_inicio=fecha_inicio,
                            fecha_fin=fecha_fin,
                            descripcion=(
                                txt_descripcion.value
                                or ""
                            ),
                            area=(
                                txt_area.value
                            ),
                        )
                    )

                    self.experiencias.append(
                        creada
                    )

                self.renderizar_experiencias()

                self.page.pop_dialog()

                self.page.update()

            except ErrorAutenticacion:
                self.page.pop_dialog()

                self.mostrar_dialogo_sesion_expirada()

                await asyncio.sleep(5)

                await self.page.push_route(
                    "/login"
                )

            except (
                ErrorServidor,
                ErrorValidacion
            ):
                self.cargando_experiencia = False

                txt_error.value = (
                    "No se pudo guardar la experiencia. "
                    "Intentá nuevamente"
                )

                txt_error.visible = True

                btn_agregar.disabled = False

                btn_agregar.content = ft.Text(
                    texto_boton,
                    color=ft.Colors.WHITE,
                )

                self.page.update()

                return

            finally:
                self.cargando_experiencia = False

        btn_agregar = ft.Button(
            texto_boton,
            on_click=agregar,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(
                    radius=10
                ),
            ),
        )

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Row(
                    spacing=8,
                    controls=[
                        ft.Icon(
                            ft.Icons.WORK_OUTLINE,
                            color=ft.Colors.BLUE_500,
                        ),
                        ft.Text(
                            (
                                "Editar experiencia"
                                if editando
                                else "Agregar experiencia"
                            ),
                            color=ft.Colors.BLACK_87,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ]
                ),
                content=ft.Column(
                    tight=True,
                    spacing=12,
                    width=380,
                    controls=[
                        ft.Row(
                            spacing=10,
                            controls=[
                                txt_empresa,
                                txt_puesto,
                            ]
                        ),
                        txt_area,
                        ft.Row(
                            spacing=10,
                            controls=[
                                selector_inicio,
                                selector_fin,
                            ]
                        ),
                        txt_descripcion,
                        txt_error,
                    ]
                ),
                actions=[
                    ft.TextButton(
                        "Cancelar",
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_500,
                        ),
                        on_click=lambda e:
                        self.page.pop_dialog(),
                    ),
                    btn_agregar,
                ],
            )
        )

    async def guardar(self, e):
        if self.cargando_guardado:
            return

        self.cargando_guardado = True

        self.btn_guardar.disabled = True

        self.btn_guardar.content = (
            self._contenido_guardando()
        )

        self.page.update()

        try:
            await PostulanteService.actualizar_postulante(
                self.page,
                nombre=self.txt_nombre.value,
                apellido=self.txt_apellido.value,
                ubicacion=self.dd_ubicacion.value,
                descripcion_personal=(
                    self.txt_descripcion.value
                ),
                disponibilidad=(
                    self.dd_disponibilidad.value
                ),
            )

            self.mostrar_mensaje(
                "Perfil actualizado correctamente"
            )

            await self.page.push_route(
                "/perfil-personal-postulante"
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except (
            ErrorServidor,
            ErrorValidacion
        ):
            self.mostrar_mensaje(
                "No se pudo guardar el perfil. "
                "Intente nuevamente"
            )

        finally:
            self.cargando_guardado = False

            self.btn_guardar.disabled = False

            self.btn_guardar.content = (
                self._contenido_guardar()
            )

            self.page.update()

    async def volver(self, e):
        if (
            self.cargando_guardado
            or self.cargando_estudio
            or self.cargando_experiencia
            or self.cargando_foto
            or self.cargando_cv
        ):
            return

        await self.page.push_route(
            "/perfil-personal-postulante"
        )

    def mostrar_mensaje(self, mensaje):
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    mensaje
                )
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