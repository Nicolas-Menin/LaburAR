import asyncio
import unicodedata

import flet as ft

from frontend.src.session.sesion import Sesion
from frontend.src.services.conversacion_service import ConversacionService
from frontend.src.services.empleador_service import EmpleadorService
from frontend.src.services.mensaje_service import MensajeService
from frontend.src.services.chat_service import ChatService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
)

# pylint: disable=E1121,E1123,E0401,E1101


class MensajeriaView(ft.View):

    def __init__(self):
        super().__init__()

        self.route = "/mensajes"
        self.padding = 0
        self.spacing = 0
        self.bgcolor = ft.Colors.BLUE_GREY_50

        self.bg_image = ft.Image(
            src="images/LaburAR_bg4.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self._running = True
        self.conversacion_actual = None
        self.conversaciones = []
        self.conexion_ws = None
        self.tarea_ws = None
        self._tarea_conversaciones = None

        self.cargando_conversaciones = False
        self.texto_busqueda = ""

        self.oferta_filtro_id = None
        self.oferta_filtro_nombre = None
        self.oferta_seleccionada = None
        self.cards_ofertas = []
        self.lista_ofertas = None
        self.txt_busqueda_oferta = None
        self.btn_aplicar_filtro = None
        self.btn_limpiar_filtro = None

        self.btn_filtros = ft.OutlinedButton(
            "FILTROS",
            icon=ft.Icons.FILTER_LIST,
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
            on_click=self.abrir_panel,
        )

        self.txt_chip_filtro = ft.Text(
            "",
            width=180,
            size=12,
            color=ft.Colors.BLUE_500,
            weight=ft.FontWeight.W_500,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        self.chip_filtro = ft.Container(
            visible=False,
            bgcolor=ft.Colors.BLUE_50,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_500,
            ),
            border_radius=20,
            padding=ft.Padding(
                left=12,
                top=2,
                right=4,
                bottom=2,
            ),
            content=ft.Row(
                tight=True,
                spacing=4,
                controls=[
                    self.txt_chip_filtro,
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_size=16,
                        icon_color=ft.Colors.BLUE_500,
                        on_click=self.quitar_filtro,
                    ),
                ],
            ),
        )

        self.fila_filtro = ft.Container(
            visible=False,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                tight=True,
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.btn_filtros,
                    self.chip_filtro,
                ],
            ),
        )

        self.txt_busqueda = ft.TextField(
            hint_text="Buscar conversación",
            height=45,
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
            on_change=self.filtrar_por_texto,
        )

        self.lista_conversaciones = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        self.indicador_carga_conversaciones = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.ProgressRing(
                    width=32,
                    height=32,
                    stroke_width=3,
                    color=ft.Colors.BLUE_500,
                ),
                ft.Text(
                    "Cargando conversaciones...",
                    color=ft.Colors.BLACK_54,
                    size=13,
                ),
            ],
        )

        self.panel_conversaciones = ft.Container(
            width=300,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            border_radius=15,
            padding=15,
            content=ft.Column(
                expand=True,
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Text(
                        "CONVERSACIONES",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12,
                    ),
                    self.txt_busqueda,
                    self.fila_filtro,
                    ft.Container(
                        expand=True,
                        content=self.lista_conversaciones,
                    ),
                ],
            ),
        )

        self.avatar_conversacion = ft.CircleAvatar(
            radius=22,
            bgcolor=ft.Colors.BLUE_GREY_100,
            content=ft.Icon(
                ft.Icons.PERSON,
                size=20,
                color=ft.Colors.BLUE_GREY_400,
            ),
        )

        self.txt_nombre_conversacion = ft.Text(
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK_87,
            font_family="Inter-Bold",
            expand=True,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        self.btn_salir_chat = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color=ft.Colors.BLACK_54,
            tooltip="Salir de la conversación",
            visible=False,
            on_click=self.salir_conversacion,
        )

        self.encabezado_conversacion = ft.Container(
            padding=ft.Padding.symmetric(
                horizontal=15,
                vertical=12,
            ),
            border=ft.Border(
                bottom=ft.BorderSide(
                    1,
                    ft.Colors.BLUE_GREY_100,
                )
            ),
            content=ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.avatar_conversacion,
                    self.txt_nombre_conversacion,
                    self.btn_salir_chat,
                ],
            ),
        )

        self.lista_mensajes = ft.Column(
            expand=True,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                self.crear_texto_sin_conversacion()
            ],
        )

        self.campo_mensaje = ft.TextField(
            hint_text="Escribí un mensaje...",
            expand=True,
            border_radius=20,
            bgcolor=ft.Colors.BLUE_GREY_50,
            border_color=ft.Colors.TRANSPARENT,
            focused_border_color=ft.Colors.BLUE_500,
            color=ft.Colors.BLACK_87,
            on_submit=self.enviar_mensaje,
            disabled=True,
        )

        self.btn_enviar = ft.IconButton(
            icon=ft.Icons.SEND,
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_500,
            on_click=self.enviar_mensaje,
            disabled=True,
        )

        self.barra_envio = ft.Container(
            padding=15,
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.campo_mensaje,
                    self.btn_enviar,
                ],
            ),
        )

        self.panel_chat = ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            border_radius=15,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    self.encabezado_conversacion,
                    ft.Container(
                        expand=True,
                        padding=15,
                        content=self.lista_mensajes,
                    ),
                    self.barra_envio,
                ],
            ),
        )

        self.header = ft.Container(
            padding=ft.Padding.symmetric(
                horizontal=20,
                vertical=15,
            ),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
        )

        self.controls = [
            ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        content=self.bg_image,
                    ),
                    ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[
                            self.header,
                            ft.Container(
                                expand=True,
                                padding=ft.Padding.only(
                                    left=20,
                                    right=20,
                                    bottom=20,
                                ),
                                content=ft.Row(
                                    expand=True,
                                    spacing=20,
                                    vertical_alignment=(
                                        ft.CrossAxisAlignment.STRETCH
                                    ),
                                    controls=[
                                        self.panel_conversaciones,
                                        self.panel_chat,
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
            )
        ]

    def did_mount(self):
        self._running = True
        self.reiniciar_chat()

        self.oferta_filtro_id = None
        self.oferta_filtro_nombre = None
        self.oferta_seleccionada = None
        self.chip_filtro.visible = False
        self.fila_filtro.visible = (
            Sesion.rol(self.page) == "EMPLEADOR"
        )

        self.texto_busqueda = ""
        self.txt_busqueda.value = ""
        self.txt_busqueda.hint_text = (
            "Buscar por postulante"
            if Sesion.rol(self.page) == "EMPLEADOR"
            else "Buscar por oferta o empresa"
        )

        self.mostrar_cargando_conversaciones()

        self._tarea_conversaciones = self.page.run_task(
            self.verificar_conversaciones
        )

    def mostrar_cargando_conversaciones(self):
        """Muestra el indicador mientras se cargan las conversaciones."""

        self.lista_conversaciones.controls = [
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=self.indicador_carga_conversaciones,
            )
        ]

        self.update()

    async def verificar_conversaciones(self):
        """Verifica periódicamente las conversaciones y sus mensajes no leídos."""

        carga_inicial = True

        try:
            while self._running:
                filtro_usado = self.oferta_filtro_id

                if Sesion.rol(self.page) == "POSTULANTE":
                    resultado = (
                        await ConversacionService.traer_conversaciones_postulante(
                            page=self.page
                        )
                    )

                elif Sesion.rol(self.page) == "EMPLEADOR":
                    resultado = (
                        await ConversacionService.traer_conversaciones_empleador(
                            page=self.page,
                            oferta_id=filtro_usado,
                        )
                    )

                else:
                    self.mostrar_mensaje(
                        "No se pudo identificar el tipo de usuario"
                    )
                    return None

                if not self._running:
                    return

                if filtro_usado == self.oferta_filtro_id:
                    self.conversaciones = resultado
                    self.ordenar_conversaciones()
                    self.mostrar_conversaciones()

                    # Solo al entrar a la vista, no en cada chequeo de 60s
                    if (
                        carga_inicial
                        and not self.conversaciones
                        and self.oferta_filtro_id is None
                    ):
                        self.mostrar_dialogo_sin_conversaciones()

                carga_inicial = False
                await asyncio.sleep(60)

        except asyncio.CancelledError:
            return

        except ErrorAutenticacion:
            self._running = False
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)
            await self.page.push_route("/login")

        except ErrorServidor:
            if self._running:
                if carga_inicial:
                    self.lista_conversaciones.controls = [
                        ft.Container(
                            padding=20,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text(
                                "No se pudieron cargar las conversaciones",
                                color=ft.Colors.BLACK_45,
                                size=12,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        )
                    ]

                    self.update()
                else:
                    self.mostrar_mensaje(
                        "No se ha podido actualizar la lista de conversaciones"
                    )

    def will_unmount(self):
        self.reiniciar_chat()
        self.detener_verificacion_conversaciones()

    async def cargar_conversaciones(self):
        """Metodo para traer las conversaciones del usuario segun su rol."""

        self.cargando_conversaciones = True

        try:
            if not Sesion.token(self.page):
                self.mostrar_dialogo_sesion_expirada()
                await asyncio.sleep(5)
                await self.page.push_route("/login")

            if Sesion.rol(self.page) == "POSTULANTE":
                self.conversaciones = (
                    await ConversacionService.traer_conversaciones_postulante(
                        page=self.page
                    )
                )

            elif Sesion.rol(self.page) == "EMPLEADOR":
                self.conversaciones = (
                    await ConversacionService.traer_conversaciones_empleador(
                        page=self.page,
                        oferta_id=self.oferta_filtro_id,
                    )
                )

            else:
                self.mostrar_mensaje(
                    "No se pudo identificar el tipo de usuario"
                )
                return

            self.ordenar_conversaciones()
            self.mostrar_conversaciones()

            if (
                not self.conversaciones
                and self.oferta_filtro_id is None
            ):
                self.mostrar_dialogo_sin_conversaciones()

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await self.page.push_route("/login")

        except ErrorServidor:
            self.lista_conversaciones.controls = [
                ft.Container(
                    padding=20,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No se pudieron cargar las conversaciones",
                        color=ft.Colors.BLACK_45,
                        size=12,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]

            self.update()
            self.mostrar_mensaje(
                "No se pudieron cargar las conversaciones"
            )

        finally:
            self.cargando_conversaciones = False

    def ordenar_conversaciones(self):
        """Metodo para ordenar las conversaciones."""

        self.conversaciones.sort(
            key=lambda c: c.get(
                "cantidad_mensajes_no_leidos",
                0
            ) > 0,
            reverse=True,
        )

    def obtener_nombre_conversacion(self, conversacion: dict):
        """Metodo para obtener el nombre a mostrar, segun el contrato recibido."""

        if "nombre_empleador" in conversacion:
            return conversacion.get(
                "nombre_empleador",
                ""
            )

        nombre = conversacion.get("nombre", "")
        apellido = conversacion.get("apellido", "")

        return f"{nombre} {apellido}".strip()

    @staticmethod
    def _normalizar(texto: str) -> str:
        """Pasa a minúsculas y quita tildes para comparar textos."""

        texto = unicodedata.normalize(
            "NFD",
            str(texto or ""),
        )

        sin_tildes = "".join(
            caracter
            for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )

        return sin_tildes.lower().strip()

    def _texto_conversacion(self, conversacion: dict) -> str:
        """Todo lo que muestra una card, para poder buscar en ello."""

        return self._normalizar(
            f"{self.obtener_nombre_conversacion(conversacion)} "
            f"{conversacion.get('nombre_oferta', '')}"
        )

    def _conversaciones_visibles(self) -> list:
        """Conversaciones que coinciden con el texto de búsqueda."""

        consulta = self._normalizar(self.texto_busqueda)

        if not consulta:
            return self.conversaciones

        return [
            conversacion
            for conversacion in self.conversaciones
            if consulta in self._texto_conversacion(conversacion)
        ]

    def filtrar_por_texto(self, e):
        """Filtra, en pantalla, las conversaciones ya cargadas."""

        self.texto_busqueda = e.control.value or ""
        self.mostrar_conversaciones()

    def mostrar_conversaciones(self):
        """Metodo para dibujar la lista de conversaciones en pantalla."""

        visibles = self._conversaciones_visibles()

        if not visibles:
            if not self.conversaciones:
                texto_vacio = (
                    "No hay conversaciones para esta oferta"
                    if self.oferta_filtro_id is not None
                    else "No tenés conversaciones todavía"
                )
            else:
                texto_vacio = (
                    "No se encontraron conversaciones "
                    "con esa búsqueda"
                )

            self.lista_conversaciones.controls = [
                ft.Container(
                    padding=20,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        texto_vacio,
                        color=ft.Colors.BLACK_45,
                        size=12,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]

            self.update()
            return

        self.lista_conversaciones.controls = [
            self.crear_item_conversacion(conversacion)
            for conversacion in visibles
        ]

        self.update()

    def obtener_titulo_chat(self, conversacion: dict) -> str:
        """Título del chat abierto.

        Postulante: 'ABSA - Desarrollador Backend'.
        Empleador: 'Nicolas Menin para puesto Desarrollador Backend'.
        """

        nombre = self.obtener_nombre_conversacion(conversacion)
        oferta = conversacion.get("nombre_oferta") or ""

        if not oferta:
            return nombre

        if "nombre_empleador" in conversacion:
            return f"{nombre} - {oferta}"

        return f"{nombre} para puesto {oferta}"

    def crear_item_conversacion(self, conversacion: dict):
        """Metodo para crear la card de una conversacion en la lista."""

        conversacion_id = conversacion.get("conversacion_id")

        seleccionada = (
            self.conversacion_actual is not None
            and self.conversacion_actual.get(
                "conversacion_id"
            ) == conversacion_id
        )

        no_leidos = conversacion.get(
            "cantidad_mensajes_no_leidos",
            0,
        )

        nombre = self.obtener_nombre_conversacion(conversacion)
        foto = conversacion.get("foto_perfil")
        nombre_oferta = conversacion.get("nombre_oferta", "")

        es_postulante = "nombre_empleador" in conversacion

        if es_postulante:
            linea_principal = nombre_oferta
            linea_secundaria = nombre
            color_secundario = ft.Colors.BLACK_45
        else:
            linea_principal = nombre
            linea_secundaria = nombre_oferta
            color_secundario = ft.Colors.BLACK_54

        return ft.Container(
            bgcolor=(
                ft.Colors.BLUE_50
                if seleccionada
                else ft.Colors.WHITE
            ),
            border=ft.Border.all(
                1,
                (
                    ft.Colors.BLUE_200
                    if seleccionada
                    else ft.Colors.BLUE_GREY_100
                ),
            ),
            border_radius=12,
            padding=10,
            on_click=self.seleccionar_conversacion,
            data=conversacion,
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.CircleAvatar(
                        radius=18,
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
                                ft.Icons.PERSON,
                                size=16,
                                color=ft.Colors.BLUE_GREY_400,
                            )
                        ),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=2,
                        controls=[
                            ft.Text(
                                linea_principal,
                                color=ft.Colors.BLACK_87,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                weight=(
                                    ft.FontWeight.BOLD
                                    if no_leidos
                                    else ft.FontWeight.NORMAL
                                ),
                            ),
                            ft.Text(
                                linea_secundaria,
                                size=11,
                                color=color_secundario,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                    ),
                    ft.Container(
                        width=8,
                        height=8,
                        border_radius=4,
                        bgcolor=ft.Colors.BLUE_500,
                        visible=bool(no_leidos),
                    ),
                ],
            ),
        )

    @staticmethod
    def _id_oferta(oferta: dict):
        """Obtiene el id de una oferta."""

        for clave in ("id", "oferta_id", "id_oferta"):
            if oferta.get(clave) is not None:
                return oferta[clave]

        return None

    @staticmethod
    def _nombre_oferta(oferta: dict):
        """Obtiene el nombre de una oferta."""

        return (
            oferta.get("titulo")
            or oferta.get("titulo_oferta")
            or oferta.get("nombre_oferta")
            or oferta.get("nombre")
            or "Oferta sin título"
        )

    async def abrir_panel(self, e):
        """Abre el diálogo para elegir la oferta por la cual filtrar."""

        if self.cargando_conversaciones:
            return

        self.oferta_seleccionada = (
            {
                "id": self.oferta_filtro_id,
                "nombre": self.oferta_filtro_nombre,
            }
            if self.oferta_filtro_id is not None
            else None
        )

        self.cards_ofertas = []

        self.txt_busqueda_oferta = ft.TextField(
            hint_text="Buscar oferta laboral",
            expand=True,
            height=50,
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
            on_submit=self.buscar_ofertas,
        )

        btn_buscar_oferta = ft.Button(
            "BUSCAR",
            width=110,
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(
                    radius=15,
                ),
            ),
            on_click=self.buscar_ofertas,
        )

        self.lista_ofertas = ft.ListView(
            expand=True,
            spacing=10,
        )

        contenido = ft.Column(
            expand=True,
            spacing=15,
            controls=[
                ft.Text(
                    "Seleccioná la oferta laboral por la cual "
                    "querés filtrar las conversaciones.",
                    color=ft.Colors.BLACK,
                ),
                ft.Row(
                    spacing=10,
                    controls=[
                        self.txt_busqueda_oferta,
                        btn_buscar_oferta,
                    ],
                ),
                self.lista_ofertas,
            ],
        )

        self.btn_aplicar_filtro = ft.FilledButton(
            "APLICAR",
            disabled=self.oferta_seleccionada is None,
            on_click=self.aplicar_filtro,
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
        )

        self.btn_limpiar_filtro = ft.TextButton(
            "QUITAR FILTRO",
            visible=self.oferta_filtro_id is not None,
            on_click=self.quitar_filtro,
            style=ft.ButtonStyle(
                color=ft.Colors.RED_500,
                shape=ft.RoundedRectangleBorder(
                    radius=10,
                ),
            ),
        )

        dialogo = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.WHITE,
            title=ft.Text(
                "Filtrar por oferta laboral",
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
                self.btn_limpiar_filtro,
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
                self.btn_aplicar_filtro,
            ],
        )

        self.page.show_dialog(dialogo)
        await self.cargar_ofertas("")

    async def buscar_ofertas(self, e):
        """Busca ofertas dentro del diálogo."""

        await self.cargar_ofertas(
            self.txt_busqueda_oferta.value
        )

    async def cargar_ofertas(self, busqueda: str):
        """Trae las ofertas del empleador."""

        self.lista_ofertas.controls = [
            ft.Row(
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
        ]

        self.lista_ofertas.update()

        try:
            ofertas = (
                await EmpleadorService.filtrar_ofertas_laborales(
                    self.page,
                    busqueda=busqueda or None,
                )
            )

        except ErrorAutenticacion:
            self.page.pop_dialog()
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)
            await self.page.push_route("/login")
            return

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

            self.lista_ofertas.update()
            return

        self.cards_ofertas = []

        if not ofertas:
            self.lista_ofertas.controls = [
                ft.Container(
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No se encontraron ofertas laborales",
                        color=ft.Colors.BLACK_54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]

            self.lista_ofertas.update()
            return

        for oferta in ofertas:
            self.cards_ofertas.append(
                self._card_oferta(oferta)
            )

        self.lista_ofertas.controls = self.cards_ofertas
        self.lista_ofertas.update()

    def _card_oferta(self, oferta: dict):
        """Arma una card seleccionable de oferta."""

        datos = {
            "id": self._id_oferta(oferta),
            "nombre": self._nombre_oferta(oferta),
        }

        seleccionada = (
            self.oferta_seleccionada is not None
            and self.oferta_seleccionada["id"] == datos["id"]
        )

        return ft.Container(
            data=datos,
            on_click=self.seleccionar_oferta,
            padding=15,
            border_radius=15,
            bgcolor=(
                ft.Colors.BLUE_50
                if seleccionada
                else ft.Colors.WHITE
            ),
            border=ft.Border.all(
                2 if seleccionada else 1,
                (
                    ft.Colors.BLUE_500
                    if seleccionada
                    else ft.Colors.BLUE_GREY_100
                ),
            ),
            content=ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        ft.Icons.WORK_OUTLINE,
                        color=ft.Colors.BLUE_GREY_400,
                    ),
                    ft.Text(
                        datos["nombre"],
                        expand=True,
                        size=15,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.BLACK_87,
                    ),
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE,
                        color=ft.Colors.BLUE_500,
                        visible=seleccionada,
                    ),
                ],
            ),
        )

    def seleccionar_oferta(self, e):
        """Marca una oferta como seleccionada."""

        self.oferta_seleccionada = e.control.data

        for card in self.cards_ofertas:
            activa = (
                card.data["id"]
                == self.oferta_seleccionada["id"]
            )

            card.bgcolor = (
                ft.Colors.BLUE_50
                if activa
                else ft.Colors.WHITE
            )

            card.border = ft.Border.all(
                2 if activa else 1,
                (
                    ft.Colors.BLUE_500
                    if activa
                    else ft.Colors.BLUE_GREY_100
                ),
            )

            card.content.controls[-1].visible = activa
            card.update()

        self.btn_aplicar_filtro.disabled = False
        self.btn_aplicar_filtro.update()

    async def aplicar_filtro(self, e):
        """Aplica el filtro de oferta y recarga las conversaciones."""

        if self.oferta_seleccionada is None:
            return

        self.oferta_filtro_id = self.oferta_seleccionada["id"]
        self.oferta_filtro_nombre = self.oferta_seleccionada["nombre"]

        self.txt_chip_filtro.value = (
            f"Oferta: {self.oferta_filtro_nombre}"
        )

        self.chip_filtro.visible = True
        self.page.pop_dialog()
        self.mostrar_cargando_conversaciones()

        await self.cargar_conversaciones()

    async def quitar_filtro(self, e):
        """Quita el filtro de oferta y recarga las conversaciones."""

        if self.cargando_conversaciones:
            return

        self.oferta_filtro_id = None
        self.oferta_filtro_nombre = None
        self.oferta_seleccionada = None
        self.chip_filtro.visible = False

        if e.control is self.btn_limpiar_filtro:
            self.page.pop_dialog()

        self.mostrar_cargando_conversaciones()
        await self.cargar_conversaciones()

    async def seleccionar_conversacion(self, e):
        """Metodo para abrir una conversacion, cargar su historial y conectar el websocket."""

        self.cerrar_websocket()
        self.conversacion_actual = e.control.data

        self.txt_nombre_conversacion.value = (
            self.obtener_titulo_chat(self.conversacion_actual)
        )

        foto = self.conversacion_actual.get("foto_perfil")

        self.avatar_conversacion.foreground_image_src = (
            foto
            if foto
            else None
        )

        self.btn_salir_chat.visible = True

        self.lista_mensajes.controls = [
            self.crear_indicador_carga_chat()
        ]

        self.campo_mensaje.disabled = True
        self.btn_enviar.disabled = True

        self.mostrar_conversaciones()

        await self.cargar_historial()
        await self.marcar_como_leidos()

        self.conectar_websocket()

    async def salir_conversacion(self, e):
        """Metodo para salir de la conversacion activa y cerrar su websocket."""

        self.reiniciar_chat()
        self.mostrar_conversaciones()

    def reiniciar_chat(self):
        """Metodo para dejar la vista sin ningun chat abierto.

        Cierra el websocket y limpia el panel del chat. No actualiza la
        pantalla, asi que se puede usar tambien al montar o desmontar la vista.
        """

        self.cerrar_websocket()
        self.conversacion_actual = None

        self.txt_nombre_conversacion.value = ""
        self.avatar_conversacion.foreground_image_src = None
        self.btn_salir_chat.visible = False

        self.campo_mensaje.value = ""
        self.campo_mensaje.disabled = True
        self.btn_enviar.disabled = True

        self.lista_mensajes.controls = [
            self.crear_texto_sin_conversacion()
        ]

    def crear_indicador_carga_chat(self):
        """Metodo para crear el indicador que se ve mientras carga el chat."""

        return ft.Container(
            padding=ft.Padding.only(top=60),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.ProgressRing(
                        width=32,
                        height=32,
                        stroke_width=3,
                        color=ft.Colors.BLUE_500,
                    ),
                    ft.Text(
                        "Cargando mensajes...",
                        color=ft.Colors.BLACK_54,
                        size=13,
                    ),
                ],
            ),
        )

    def crear_texto_sin_conversacion(self):
        """Metodo para crear el texto que se ve cuando no hay chat abierto."""

        return ft.Text(
            "Seleccioná una conversación para empezar",
            color=ft.Colors.BLACK_45,
            size=12,
            text_align=ft.TextAlign.CENTER,
        )

    async def cargar_historial(self):
        """Metodo para traer el historial de mensajes de la conversacion activa."""

        if not self.conversacion_actual:
            return

        conversacion_id = self.conversacion_actual["conversacion_id"]

        try:
            respuesta = await MensajeService.listar_mensajes(
                page=self.page,
                conversacion_id=conversacion_id,
            )

            if (
                not self.conversacion_actual
                or self.conversacion_actual.get(
                    "conversacion_id"
                ) != conversacion_id
            ):
                return

            mensajes = respuesta.get("mensajes", [])
            self.mostrar_mensajes(mensajes)

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await self.page.push_route("/login")

        except ErrorServidor:
            self.lista_mensajes.controls = [
                ft.Text(
                    "No se pudieron cargar los mensajes",
                    color=ft.Colors.RED_400,
                    size=12,
                    text_align=ft.TextAlign.CENTER,
                )
            ]

            self.update()
            self.mostrar_mensaje(
                "No se pudieron cargar los mensajes"
            )

    async def marcar_como_leidos(self):
        """Metodo para marcar como leidos los mensajes de la conversacion activa."""

        if not self.conversacion_actual:
            return

        try:
            await MensajeService.actualizar_estado_mensajes(
                page=self.page,
                conversacion_id=self.conversacion_actual[
                    "conversacion_id"
                ],
            )

        except (
            ErrorAutenticacion,
            ErrorServidor,
        ):
            pass

    def mostrar_mensajes(self, mensajes: list):
        """Metodo para dibujar los mensajes de la conversacion activa."""

        if not mensajes:
            self.lista_mensajes.controls = [
                ft.Text(
                    "Todavía no hay mensajes",
                    color=ft.Colors.BLACK_45,
                    size=12,
                )
            ]

            self.update()
            return

        self.lista_mensajes.controls = [
            self.crear_burbuja(mensaje)
            for mensaje in mensajes
        ]

        self.update()

    def crear_burbuja(self, mensaje: dict):
        """Metodo para crear la burbuja de un mensaje."""

        usuario_id = (
            Sesion.obtener_usuario_id(self.page)
            if Sesion.token(self.page)
            else None
        )

        es_propio = (
            str(mensaje.get("remitente_id"))
            == str(usuario_id)
        )

        contenido = mensaje.get("contenido", "")

        burbuja = ft.Container(
            bgcolor=(
                ft.Colors.BLUE_500
                if es_propio
                else ft.Colors.BLUE_GREY_50
            ),
            border=(
                None
                if es_propio
                else ft.Border.all(
                    1,
                    ft.Colors.BLUE_GREY_100,
                )
            ),
            border_radius=15,
            padding=ft.Padding(
                left=14,
                top=10,
                right=14,
                bottom=10,
            ),
            content=ft.Text(
                contenido,
                color=(
                    ft.Colors.WHITE
                    if es_propio
                    else ft.Colors.BLACK_87
                ),
            ),
        )

        contenedor_burbuja = ft.Container(
            expand=True,
            alignment=(
                ft.Alignment.CENTER_RIGHT
                if es_propio
                else ft.Alignment.CENTER_LEFT
            ),
            content=burbuja,
        )

        return ft.Row(
            expand=True,
            controls=[contenedor_burbuja],
        )

    def conectar_websocket(self):
        """Metodo para conectar el websocket de la conversacion activa."""

        if not self.conversacion_actual:
            return

        conversacion_id = self.conversacion_actual["conversacion_id"]

        self.tarea_ws = self.page.run_task(
            self.escuchar_websocket,
            conversacion_id,
        )

    def cerrar_websocket(self):
        """Metodo para cerrar la conexion websocket activa, si existe.

        Cancela la tarea que escucha el websocket. La conexion se cierra
        dentro de esa tarea (bloque finally de escuchar_websocket).
        """

        if self.tarea_ws:
            self.tarea_ws.cancel()
            self.tarea_ws = None

        self.conexion_ws = None

    async def escuchar_websocket(self, conversacion_id: int):
        """Metodo que mantiene abierta la conexion websocket y recibe mensajes en vivo."""

        conexion = None

        try:
            conexion = await ChatService.conectar(
                page=self.page,
                conversacion_id=conversacion_id,
            )

            self.conexion_ws = conexion

            if (
                self.conversacion_actual
                and self.conversacion_actual.get(
                    "conversacion_id"
                ) == conversacion_id
            ):
                self.campo_mensaje.disabled = False
                self.btn_enviar.disabled = False
                self.update()

            while True:
                mensaje = await ChatService.recibir_mensajes(conexion)

                if (
                    self.conversacion_actual
                    and self.conversacion_actual.get(
                        "conversacion_id"
                    ) == conversacion_id
                ):
                    self.lista_mensajes.controls.append(
                        self.crear_burbuja(mensaje)
                    )

                    self.update()

        except asyncio.CancelledError:
            raise

        except Exception:
            self.mostrar_mensaje(
                "Se perdió la conexión del chat. Reabrí la conversación"
            )

            await asyncio.sleep(5)
            await self.page.push_route("/login")

        finally:
            if conexion is not None:
                try:
                    await ChatService.cerrar(conexion)
                except Exception:
                    pass

            if self.conexion_ws is conexion:
                self.conexion_ws = None

    async def enviar_mensaje(self, e):
        """Metodo para enviar un mensaje por el websocket de la conversacion activa."""

        texto = (
            self.campo_mensaje.value.strip()
            if self.campo_mensaje.value
            else ""
        )

        if not texto or not self.conexion_ws:
            return

        await ChatService.enviar_mensajes(
            self.conexion_ws,
            texto,
        )

        usuario_id = (
            Sesion.obtener_usuario_id(self.page)
            if Sesion.token(self.page)
            else None
        )

        self.lista_mensajes.controls.append(
            self.crear_burbuja(
                {
                    "remitente_id": usuario_id,
                    "contenido": texto,
                }
            )
        )

        self.campo_mensaje.value = ""
        self.update()

    async def volver(self, e):
        """Metodo para volver a la busqueda."""

        self.cerrar_websocket()

        try:
            await self.page.push_route("/busqueda")

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await self.page.push_route("/login")

    def mostrar_mensaje(self, mensaje):
        """Metodo para mostrar mensajes de excepciones."""

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje)
            )
        )

    def mostrar_dialogo_sin_conversaciones(self):
        """Avisa que para conversar tiene que existir una conexion laboral."""

        otra_parte = (
            "un postulante"
            if Sesion.rol(self.page) == "EMPLEADOR"
            else "un empleador"
        )

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    "Todavía no tenés conversaciones",
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK_87,
                ),
                content=ft.Text(
                    "Para tener una conversación primero tiene que "
                    f"existir una conexión laboral con {otra_parte}. "
                    "Cuando haya una, la conversación va a aparecer acá.",
                    color=ft.Colors.BLACK_87,
                ),
                actions=[
                    ft.TextButton(
                        "ENTENDIDO",
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_500,
                        ),
                        on_click=lambda e: self.page.pop_dialog(),
                    )
                ],
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
                        on_click=lambda e: self.page.pop_dialog(),
                    )
                ],
            )
        )

    def detener_verificacion_conversaciones(self):
        self._running = False

        if self._tarea_conversaciones is not None:
            self._tarea_conversaciones.cancel()
            self._tarea_conversaciones = None