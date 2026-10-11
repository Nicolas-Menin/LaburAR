import asyncio
import base64
import mimetypes
import time
import unicodedata
from datetime import time as Hora
from decimal import Decimal, InvalidOperation

import flet as ft

from frontend.src.services.empleador_service import EmpleadorService
from frontend.src.services.oferta_laboral_service import OfertaLaboralService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
    ErrorNoEncontrado,
    ErrorValidacion
)
from frontend.src.components.rubros import RUBROS
# pylint: disable=E1121,E1123,E0401, E1101


class EditarPerfilEmpleadorView(ft.View):

    TAMANO_MAXIMO_FOTO_MB = 5

    ESTADOS_OFERTA = [
        "ACTIVA",
        "PAUSADA",
        "CERRADA"
    ]

    TIPOS_SALARIO = [
        "FIJO",
        "RANGO",
        "A_CONVENIR",
        "NO_INFORMAR"
    ]

    JORNADAS = [
        "COMPLETA",
        "MEDIA_JORNADA",
        "TEMPORAL",
        "A_CONVENIR"
    ]

    TURNOS = [
        "MAÑANA",
        "TARDE",
        "NOCHE",
        "A_CONVENIR"
    ]

    def __init__(self):
        super().__init__()

        self.route = "/editar-perfil-empleador"
        self.padding = 0
        self.spacing = 0
        self.bgcolor = ft.Colors.BLUE_GREY_50

        self.bg_image = ft.Image(
            src="images/LaburAR_bg5.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.ofertas = []

        self.cargando_perfil = False
        self.cargando_guardado = False
        self.cargando_foto = False
        self.cargando_oferta = False
        self.cargando_estado = False



        self.rubros_disponibles = sorted(
            RUBROS,
            key=lambda r: unicodedata.normalize(
                "NFD", r
            ).encode("ascii", "ignore").decode().lower()
        )

        self.dias_semana = [
            "Lunes", "Martes", "Miércoles",
            "Jueves", "Viernes", "Sábado", "Domingo"
        ]

        self.foto_perfil = ft.CircleAvatar(
            radius=45,
            bgcolor=ft.Colors.BLUE_50,
            content=ft.Icon(
                ft.Icons.BUSINESS,
                size=40,
                color=ft.Colors.BLUE_900,
            )
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
                            "JPG o PNG · máximo "
                            f"{self.TAMANO_MAXIMO_FOTO_MB} MB",
                            color=ft.Colors.BLACK_45,
                            size=11,
                        ),
                        ft.TextButton(
                            "Cambiar foto",
                            style=ft.ButtonStyle(
                                color=ft.Colors.BLUE_500,
                                padding=ft.Padding(
                                    0, 0, 0, 0
                                ),
                            ),
                            on_click=self.cambiar_foto,
                        ),
                    ],
                ),
            ],
        )

        self.txt_nombre_negocio = ft.TextField(
            label="Nombre del negocio",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
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

        self.txt_direccion = ft.TextField(
            label="Dirección",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
        )

        self.dd_rubro = self.crear_dropdown_rubro()

        self.txt_descripcion = ft.TextField(
            label="Descripción del negocio",
            hint_text="Contanos sobre tu negocio...",
            multiline=True,
            min_lines=8,
            max_lines=14,
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
                        "DATOS DEL NEGOCIO",
                        ft.Icons.BUSINESS
                    ),
                    self.seccion_foto,
                    ft.Divider(
                        color=ft.Colors.BLUE_GREY_100,
                        height=1
                    ),
                    self.txt_nombre_negocio,
                    ft.Row(
                        spacing=15,
                        controls=[
                            self.dd_ubicacion,
                            self.txt_direccion,
                        ]
                    ),
                    self.dd_rubro,
                    self.txt_descripcion,
                ]
            )
        )

        self.lista_ofertas = ft.Column(
            spacing=10
        )

        self.tarjeta_ofertas = ft.Container(
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
                                "OFERTAS LABORALES",
                                ft.Icons.WORK_OUTLINE
                            ),
                            self._boton_agregar(
                                self.abrir_form_oferta
                            ),
                        ]
                    ),
                    self.lista_ofertas,
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
                                    spacing=20,
                                    vertical_alignment=(
                                        ft.CrossAxisAlignment.START
                                    ),
                                    controls=[
                                        self.tarjeta_datos,
                                        self.tarjeta_ofertas,
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
            ),
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
    def _formatear_texto(valor):
        """Convierte un valor del backend (EN_CURSO)
        en texto legible"""

        if not valor:
            return ""

        return valor.replace(
            "_",
            " "
        ).capitalize()

    def _opciones_dropdown(self, valores):
        """Crea las opciones de un Dropdown
        a partir de una lista de valores"""

        return [
            ft.DropdownOption(
                valor,
                content=ft.Text(
                    self._formatear_texto(valor),
                    color=ft.Colors.BLACK_87,
                ),
            )
            for valor in valores
        ]

    def crear_dropdown_rubro(self, expand: bool = False):
        """Dropdown con los rubros predeterminados.

        Se puede escribir para filtrar la lista, pero solo es valido
        elegir un rubro de la lista.
        """

        return ft.Dropdown(
            label="Rubro",
            editable=True,
            enable_filter=True,
            menu_height=250,
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=expand,
            options=[
                ft.DropdownOption(
                    rubro,
                    content=ft.Text(
                        rubro,
                        color=ft.Colors.BLACK_87,
                    ),
                )
                for rubro in self.rubros_disponibles
            ],
        )

    @staticmethod
    def _parsear_hora(valor):
        """Convierte la hora que llega del backend
        ("08:00:00") en time"""

        if not valor:
            return None

        if isinstance(valor, Hora):
            return valor

        try:
            return Hora.fromisoformat(str(valor))

        except ValueError:
            return None

    @staticmethod
    def _texto_salario(valor) -> str:
        """Convierte el salario que llega del backend
        en texto numerico"""

        if valor is None:
            return ""

        try:
            return str(int(Decimal(str(valor))))

        except (InvalidOperation, ValueError):
            return ""

    def _crear_selector_hora(
        self,
        label: str,
        hora_inicial=None
    ):
        estado = {
            "hora": hora_inicial
        }

        txt_valor = ft.Text(
            (
                hora_inicial.strftime("%H:%M")
                if hora_inicial
                else "Sin seleccionar"
            ),
            color=(
                ft.Colors.BLACK_87
                if hora_inicial
                else ft.Colors.BLACK_45
            ),
            size=13,
        )

        time_picker = (
            ft.TimePicker(value=hora_inicial)
            if hora_inicial
            else ft.TimePicker()
        )

        def al_cambiar(e):
            if time_picker.value:
                estado["hora"] = time_picker.value

                txt_valor.value = (
                    estado["hora"].strftime("%H:%M")
                )

                txt_valor.color = ft.Colors.BLACK_87

            self.page.update()

        time_picker.on_change = al_cambiar

        def abrir(e):
            self.page.show_dialog(time_picker)

        control = ft.Container(
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
                        ft.Icons.ACCESS_TIME,
                        color=ft.Colors.BLUE_500,
                        size=20,
                    ),
                ]
            )
        )

        return control, lambda: estado["hora"]

    @staticmethod
    def _url_sin_cache(url: str):
        """Agrega un parametro a la URL para que se vuelva a descargar
        la imagen cuando se reemplaza una foto que mantiene la misma URL."""

        separador = "&" if "?" in url else "?"

        return f"{url}{separador}v={int(time.time())}"

    def _mostrar_foto(
        self,
        foto: str | None,
        evitar_cache: bool = False
    ):
        """Metodo para mostrar la foto de perfil
        (o el icono por defecto)"""

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
                ft.Icons.BUSINESS,
                size=40,
                color=ft.Colors.BLUE_900,
            )

    def _mostrar_cargando_foto(self, cargando: bool):
        """Metodo para mostrar u ocultar
        el indicador de carga de la foto"""

        self.cargando_foto = cargando

        self.indicador_foto.visible = cargando
        self.btn_cambiar_foto.disabled = cargando

        self.page.update()

    async def cambiar_foto(self, e):
        """Metodo para elegir una imagen
        y actualizar la foto de perfil"""

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
                mimetypes.guess_type(archivo.name)[0]
                or "image/jpeg"
            )

            foto_base64 = (
                f"data:{tipo_contenido};base64,"
                + base64.b64encode(
                    archivo.bytes
                ).decode("ascii")
            )

            resultado = await EmpleadorService.actualizar_empleador(
                self.page,
                foto_perfil=foto_base64,
            )

            foto = (resultado or {}).get("foto_perfil")

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

    async def cargar(self, page):
        self.cargando_perfil = True

        self.contenedor_carga.visible = True
        self.contenedor_principal.visible = False

        self.indicador_carga.controls[1].value = (
            "Cargando perfil..."
        )

        self.update()

        try:
            datos = await EmpleadorService.perfil(
                page
            )

            self.mostrar_datos(datos)

            self.contenedor_carga.visible = False
            self.contenedor_principal.visible = True

            self.update()

        except ErrorAutenticacion:
            self.contenedor_carga.visible = False

            self.update()

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
        self.txt_nombre_negocio.value = datos.get(
            "nombre_negocio",
            ""
        )

        self.dd_ubicacion.value = datos.get(
            "ubicacion",
            ""
        )

        self.txt_direccion.value = datos.get(
            "direccion",
            ""
        )

        self.dd_rubro.value = datos.get(
            "rubro",
            ""
        )

        self.txt_descripcion.value = datos.get(
            "descripcion",
            ""
        )

        self._mostrar_foto(
            datos.get("foto_perfil")
        )

        self.ofertas = list(
            datos.get(
                "ofertas_laborales",
                []
            )
        )

        self.renderizar_ofertas()

    def _tarjeta_oferta(self, oferta):
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
                                oferta.get("titulo", ""),
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK_87,
                                size=13,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                " · ".join(
                                    parte
                                    for parte in [
                                        self._formatear_texto(
                                            oferta.get("jornada")
                                        ),
                                        oferta.get("ubicacion", ""),
                                    ]
                                    if parte
                                ),
                                size=11,
                                color=ft.Colors.BLACK_54,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ]
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT_OUTLINED,
                        icon_color=ft.Colors.BLUE_500,
                        icon_size=18,
                        tooltip="Editar oferta",
                        data=oferta,
                        on_click=self.abrir_form_edicion_oferta,
                    ),
                    ft.Dropdown(
                        value=oferta.get("estado"),
                        width=140,
                        dense=True,
                        text_size=12,
                        color=ft.Colors.BLACK,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=10,
                        tooltip="Cambiar estado de la oferta",
                        options=self._opciones_dropdown(
                            self.ESTADOS_OFERTA
                        ),
                        data=oferta,
                        on_select=self.cambiar_estado_oferta,
                    ),
                ]
            )
        )

    def renderizar_ofertas(self):
        if not self.ofertas:
            self.lista_ofertas.controls = [
                ft.Text(
                    "Todavía no publicaste ofertas laborales",
                    color=ft.Colors.BLACK_45,
                    size=12,
                )
            ]

            return

        self.lista_ofertas.controls = [
            self._tarjeta_oferta(oferta)
            for oferta in self.ofertas
        ]

    async def cambiar_estado_oferta(self, e):
        """Metodo para cambiar el estado de una oferta laboral
        (ACTIVA, PAUSADA o CERRADA). Las ofertas no se eliminan."""

        dropdown = e.control
        oferta = dropdown.data

        estado_anterior = oferta.get("estado")
        estado_nuevo = dropdown.value

        if (
            self.cargando_estado
            or not estado_nuevo
            or estado_nuevo == estado_anterior
        ):
            return

        self.cargando_estado = True

        dropdown.disabled = True

        self.page.update()

        try:
            await EmpleadorService.actualizar_oferta_laboral(
                self.page,
                oferta_laboral_id=oferta["id"],
                estado=estado_nuevo,
            )

            oferta["estado"] = estado_nuevo

            self.mostrar_mensaje(
                "Estado de la oferta actualizado correctamente"
            )

        except ErrorAutenticacion:
            dropdown.value = estado_anterior

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except (
            ErrorServidor,
            ErrorValidacion
        ):
            dropdown.value = estado_anterior

            self.mostrar_mensaje(
                "No se pudo cambiar el estado de la oferta. "
                "Intentá nuevamente"
            )

        finally:
            self.cargando_estado = False

            dropdown.disabled = False

            self.page.update()

    async def abrir_form_edicion_oferta(self, e):
        """Metodo para editar una oferta: trae la oferta completa
        y abre el formulario con sus datos"""

        if self.cargando_oferta or self.cargando_estado:
            return

        oferta = e.control.data

        self.cargando_oferta = True

        e.control.disabled = True

        self.page.update()

        try:
            datos = await OfertaLaboralService.obtener_oferta_laboral(
                page=self.page,
                oferta_laboral_id=oferta["id"],
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

            return

        except (
            ErrorServidor,
            ErrorNoEncontrado
        ):
            self.mostrar_mensaje(
                "No se pudo cargar la oferta. "
                "Intentá nuevamente"
            )

            return

        finally:
            self.cargando_oferta = False

            e.control.disabled = False

            self.page.update()

        await self.abrir_form_oferta(
            e,
            oferta=oferta,
            datos=datos
        )

    async def abrir_form_oferta(
        self,
        e,
        oferta=None,
        datos=None
    ):
        """Formulario para crear una oferta (oferta=None)
        o para editar una existente."""

        if self.cargando_oferta:
            return

        editando = oferta is not None

        datos = datos or {}

        texto_boton = (
            "Guardar"
            if editando
            else "Agregar"
        )

        requisitos = list(
            datos.get("requisitos") or []
        )

        dias_seleccionados = [
            dia
            for dia in self.dias_semana
            if dia in (
                datos.get("dias_laborales") or []
            )
        ]

        txt_titulo = ft.TextField(
            label="Título",
            value=datos.get("titulo") or "",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
        )

        txt_descripcion = ft.TextField(
            label="Descripción",
            value=datos.get("descripcion") or "",
            multiline=True,
            min_lines=6,
            max_lines=12,
            expand=True,
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
        )

        fila_requisitos = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8,
        )

        def renderizar_requisitos():
            fila_requisitos.controls = [
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
                                requisito,
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
                                data=requisito,
                                on_click=quitar_requisito,
                            ),
                        ]
                    )
                )
                for requisito in requisitos
            ]

        def agregar_requisito(e):
            texto = (
                txt_requisito.value or ""
            ).strip()

            if not texto:
                return

            if texto not in requisitos:
                requisitos.append(texto)

            txt_requisito.value = ""

            renderizar_requisitos()

            self.page.update()

        def quitar_requisito(e):
            if e.control.data in requisitos:
                requisitos.remove(
                    e.control.data
                )

            renderizar_requisitos()

            self.page.update()

        txt_requisito = ft.TextField(
            label="Requisito",
            hint_text="Ej: Experiencia previa",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            on_submit=agregar_requisito,
        )

        btn_agregar_requisito = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_500,
            tooltip="Agregar requisito",
            on_click=agregar_requisito,
        )

        dd_ubicacion = ft.Dropdown(
            label="Ubicación",
            value=datos.get("ubicacion"),
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

        txt_direccion = ft.TextField(
            label="Dirección",
            value=datos.get("direccion") or "",
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
        )

        dd_rubro = self.crear_dropdown_rubro(
            expand=True
        )

        dd_rubro.value = datos.get("rubro")

        dd_estado = ft.Dropdown(
            label="Estado",
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            value="ACTIVA",
            visible=not editando,
            options=self._opciones_dropdown(
                self.ESTADOS_OFERTA
            ),
        )

        txt_salario_minimo = ft.TextField(
            label="Salario ($)",
            value=self._texto_salario(
                datos.get("salario_minimo")
            ),
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            visible=False,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        txt_salario_maximo = ft.TextField(
            label="Salario máximo ($)",
            value=self._texto_salario(
                datos.get("salario_maximo")
            ),
            color=ft.Colors.BLACK_87,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            visible=False,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        def aplicar_visibilidad_salario():
            tipo = dd_salario_tipo.value

            txt_salario_minimo.visible = (
                tipo in ("FIJO", "RANGO")
            )

            txt_salario_maximo.visible = (
                tipo == "RANGO"
            )

            txt_salario_minimo.label = (
                "Salario mínimo ($)"
                if tipo == "RANGO"
                else "Salario ($)"
            )

        def al_cambiar_salario(e):
            aplicar_visibilidad_salario()

            self.page.update()

        dd_salario_tipo = ft.Dropdown(
            label="Tipo de salario",
            value=datos.get("salario_tipo"),
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            options=self._opciones_dropdown(
                self.TIPOS_SALARIO
            ),
            on_select=al_cambiar_salario,
        )

        aplicar_visibilidad_salario()

        dd_jornada = ft.Dropdown(
            label="Jornada",
            value=datos.get("jornada"),
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            options=self._opciones_dropdown(
                self.JORNADAS
            ),
        )

        dd_turno = ft.Dropdown(
            label="Turno",
            value=datos.get("turno"),
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            options=self._opciones_dropdown(
                self.TURNOS
            ),
        )

        def pintar_dia(chip, seleccionado):
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

        def alternar_dia(e):
            dia = e.control.data

            if dia in dias_seleccionados:
                dias_seleccionados.remove(dia)
            else:
                dias_seleccionados.append(dia)

            pintar_dia(
                e.control,
                dia in dias_seleccionados
            )

            self.page.update()

        def crear_chip_dia(dia):
            chip = ft.Container(
                data=dia,
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
                on_click=alternar_dia,
                content=ft.Text(
                    dia,
                    size=12,
                ),
            )

            pintar_dia(
                chip,
                dia in dias_seleccionados
            )

            return chip

        fila_dias = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8,
            controls=[
                crear_chip_dia(dia)
                for dia in self.dias_semana
            ],
        )

        selector_inicio, obtener_hora_inicio = (
            self._crear_selector_hora(
                "Hora de inicio",
                self._parsear_hora(
                    datos.get("hora_inicio")
                )
            )
        )

        selector_fin, obtener_hora_fin = (
            self._crear_selector_hora(
                "Hora de fin",
                self._parsear_hora(
                    datos.get("hora_fin")
                )
            )
        )

        txt_error = ft.Text(
            color=ft.Colors.RED_400,
            size=12,
            visible=False,
        )

        def mostrar_error(mensaje):
            txt_error.value = mensaje
            txt_error.visible = True

            self.page.update()

        async def agregar(e):

            if self.cargando_oferta:
                return

            titulo = (
                txt_titulo.value or ""
            ).strip()

            descripcion = (
                txt_descripcion.value or ""
            ).strip()

            ubicacion = dd_ubicacion.value

            direccion = (
                txt_direccion.value or ""
            ).strip()

            rubro = dd_rubro.value
            estado = dd_estado.value
            salario_tipo = dd_salario_tipo.value
            jornada = dd_jornada.value
            turno = dd_turno.value

            if len(titulo) < 2:
                mostrar_error(
                    "Ingresá el título de la oferta"
                )
                return

            if len(descripcion) < 2:
                mostrar_error(
                    "Ingresá la descripción de la oferta"
                )
                return

            if not ubicacion:
                mostrar_error(
                    "Seleccioná la ubicación"
                )
                return

            if not direccion:
                mostrar_error(
                    "Ingresá la dirección"
                )
                return

            if rubro not in self.rubros_disponibles:
                mostrar_error(
                    "Seleccioná un rubro de la lista"
                )
                return

            if not estado:
                mostrar_error(
                    "Seleccioná el estado de la oferta"
                )
                return

            if not salario_tipo:
                mostrar_error(
                    "Seleccioná el tipo de salario"
                )
                return

            if not jornada:
                mostrar_error(
                    "Seleccioná la jornada"
                )
                return

            if not turno:
                mostrar_error(
                    "Seleccioná el turno"
                )
                return

            salario_minimo = None
            salario_maximo = None

            if salario_tipo in ("FIJO", "RANGO"):

                try:
                    salario_minimo = Decimal(
                        txt_salario_minimo.value or ""
                    )

                except InvalidOperation:
                    mostrar_error(
                        "Ingresá el salario"
                    )
                    return

                if salario_minimo <= 0:
                    mostrar_error(
                        "El salario debe ser mayor a 0"
                    )
                    return

            if salario_tipo == "RANGO":

                try:
                    salario_maximo = Decimal(
                        txt_salario_maximo.value or ""
                    )

                except InvalidOperation:
                    mostrar_error(
                        "Ingresá el salario máximo"
                    )
                    return

                if salario_maximo < salario_minimo:
                    mostrar_error(
                        "El salario máximo no puede ser menor "
                        "al mínimo"
                    )
                    return

            dias_laborales = (
                [
                    dia
                    for dia in self.dias_semana
                    if dia in dias_seleccionados
                ]
                or None
            )

            self.cargando_oferta = True

            txt_error.visible = False

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
                        await EmpleadorService
                        .actualizar_oferta_laboral(
                            self.page,
                            oferta_laboral_id=oferta["id"],
                            titulo=titulo,
                            descripcion=descripcion,
                            requisitos=list(requisitos),
                            ubicacion=ubicacion,
                            direccion=direccion,
                            rubro=rubro,
                            salario_tipo=salario_tipo,
                            salario_minimo=(
                                float(salario_minimo)
                                if salario_minimo is not None
                                else None
                            ),
                            salario_maximo=(
                                float(salario_maximo)
                                if salario_maximo is not None
                                else None
                            ),
                            jornada=jornada,
                            turno=turno,
                            dias_laborales=dias_laborales,
                            hora_inicio=obtener_hora_inicio(),
                            hora_fin=obtener_hora_fin(),
                        )
                    )

                    oferta.update(
                        {
                            "titulo": titulo,
                            "descripcion": descripcion,
                            "requisitos": list(requisitos),
                            "ubicacion": ubicacion,
                            "direccion": direccion,
                            "rubro": rubro,
                            "salario_tipo": salario_tipo,
                            "jornada": jornada,
                            "turno": turno,
                        }
                    )

                    if isinstance(
                        actualizada,
                        dict
                    ):
                        oferta.update(
                            actualizada
                        )

                else:
                    creada = (
                        await EmpleadorService
                        .crear_oferta_laboral(
                            self.page,
                            titulo=titulo,
                            descripcion=descripcion,
                            requisitos=list(requisitos),
                            ubicacion=ubicacion,
                            direccion=direccion,
                            rubro=rubro,
                            estado=estado,
                            salario_tipo=salario_tipo,
                            salario_minimo=salario_minimo,
                            salario_maximo=salario_maximo,
                            jornada=jornada,
                            turno=turno,
                            dias_laborales=dias_laborales,
                            hora_inicio=obtener_hora_inicio(),
                            hora_fin=obtener_hora_fin(),
                        )
                    )

                    self.ofertas.append(
                        creada
                    )

                self.renderizar_ofertas()

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
                txt_error.value = (
                    "No se pudo guardar la oferta. "
                    "Intentá nuevamente"
                )

                txt_error.visible = True

                btn_agregar.disabled = False

                btn_agregar.content = ft.Text(
                    texto_boton,
                    color=ft.Colors.WHITE,
                )

                self.page.update()

            finally:
                self.cargando_oferta = False

        btn_agregar = ft.Button(
            texto_boton,
            on_click=agregar,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
            ),
        )

        renderizar_requisitos()

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
                                "Editar oferta laboral"
                                if editando
                                else "Agregar oferta laboral"
                            ),
                            color=ft.Colors.BLACK_87,
                        ),
                    ]
                ),
                content=ft.Container(
                    width=700,
                    height=480,
                    content=ft.Column(
                        spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            txt_titulo,
                            txt_descripcion,
                            ft.Row(
                                spacing=10,
                                vertical_alignment=(
                                    ft.CrossAxisAlignment.CENTER
                                ),
                                controls=[
                                    txt_requisito,
                                    btn_agregar_requisito,
                                ]
                            ),
                            fila_requisitos,
                            ft.Row(
                                spacing=10,
                                controls=[
                                    dd_ubicacion,
                                    txt_direccion,
                                ]
                            ),
                            ft.Row(
                                spacing=10,
                                controls=[
                                    dd_rubro,
                                    dd_estado,
                                ]
                            ),
                            dd_salario_tipo,
                            ft.Row(
                                spacing=10,
                                controls=[
                                    txt_salario_minimo,
                                    txt_salario_maximo,
                                ]
                            ),
                            ft.Row(
                                spacing=10,
                                controls=[
                                    dd_jornada,
                                    dd_turno,
                                ]
                            ),
                            ft.Text(
                                "Días laborales (opcional)",
                                color=ft.Colors.BLACK_54,
                                size=12,
                            ),
                            fila_dias,
                            ft.Text(
                                "Horario (opcional)",
                                color=ft.Colors.BLACK_54,
                                size=12,
                            ),
                            ft.Row(
                                spacing=10,
                                controls=[
                                    selector_inicio,
                                    selector_fin,
                                ]
                            ),
                            txt_error,
                        ]
                    ),
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

        nombre_negocio = (
            self.txt_nombre_negocio.value or ""
        ).strip()

        direccion = (
            self.txt_direccion.value or ""
        ).strip()

        ubicacion = self.dd_ubicacion.value

        if len(nombre_negocio) < 2:
            self.mostrar_mensaje(
                "Ingresá el nombre del negocio"
            )
            return

        if len(direccion) < 2:
            self.mostrar_mensaje(
                "Ingresá la dirección del negocio"
            )
            return

        if not ubicacion:
            self.mostrar_mensaje(
                "Seleccioná la ubicación"
            )
            return

        rubro = self.dd_rubro.value

        if rubro not in self.rubros_disponibles:
            self.mostrar_mensaje(
                "Seleccioná un rubro de la lista"
            )
            return

        self.cargando_guardado = True

        self.btn_guardar.disabled = True

        self.btn_guardar.content = (
            self._contenido_guardando()
        )

        self.page.update()

        try:
            await EmpleadorService.actualizar_empleador(
                self.page,
                nombre_negocio=nombre_negocio,
                direccion=direccion,
                ubicacion=ubicacion,
                descripcion=(
                    self.txt_descripcion.value
                ),
                rubro=rubro,
            )

            self.mostrar_mensaje(
                "Perfil actualizado correctamente"
            )

            await self.page.push_route(
                "/perfil-personal-empleador"
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

            self.btn_guardar.disabled = False

            self.btn_guardar.content = (
                self._contenido_guardar()
            )

            self.page.update()

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
            or self.cargando_foto
            or self.cargando_oferta
            or self.cargando_estado
        ):
            return

        await self.page.push_route(
            "/perfil-personal-empleador"
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