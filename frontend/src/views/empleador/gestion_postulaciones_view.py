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


class GestionPostulantesView(ft.View):

    def __init__(self, perfil_postulante):
        super().__init__()

        self.perfil_postulante = perfil_postulante

        self.route = "/gestion-postulantes"
        self.padding = 0
        self.spacing = 0
        self.bgcolor = ft.Colors.BLUE_GREY_50

        self.bg_image = ft.Image(
            src="images/LaburAR_bg3.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.postulaciones = []
        self.cargando = False
        self.navegando = False
        self.accionando = False
        self.consulta_actual = ""

        self.tamano_pagina = 10
        self.offset = 0
        self.pagina = 1
        self.cantidad_actual = 0
        self.offsets_previos = []
        self.hay_mas = False

        self.botones_por_postulacion = {}

        self.oferta_filtro_id = None
        self.oferta_filtro_nombre = None
        self.oferta_seleccionada = None
        self.cards_ofertas = []
        self.lista_ofertas = None
        self.txt_busqueda_oferta = None
        self.btn_aplicar_filtro = None
        self.btn_limpiar_filtro = None

        self.ESTADOS_POSTULACION = {
            "PENDIENTE": (
                "Solicitud recibida",
                ft.Colors.BLUE_500,
                ft.Colors.BLUE_50,
            ),
            "ACEPTADA": (
                "Aceptada",
                ft.Colors.GREEN_600,
                ft.Colors.GREEN_50,
            ),
            "RECHAZADA": (
                "Rechazada",
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
            "GESTIÓN DE POSTULANTES",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK_87,
            text_align=ft.TextAlign.CENTER,
            font_family="Inter-Bold",
        )

        self.txt_busqueda = ft.TextField(
            hint_text="Buscar postulante",
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

        self.filtros = ft.OutlinedButton(
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

        self.fila_filtros = ft.Row(
            width=760,
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.filtros,
                self.chip_filtro,
            ],
        )

        self.lista_postulaciones = ft.Column(
            width=760,
            spacing=15,
            horizontal_alignment=(
                ft.CrossAxisAlignment.STRETCH
            ),
        )

        self.btn_anterior = ft.OutlinedButton(
            "ANTERIOR",
            icon=ft.Icons.CHEVRON_LEFT,
            visible=False,
            disabled=True,
            on_click=self.pagina_anterior,
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

        self.txt_pagina = ft.Text(
            "Página 1",
            color=ft.Colors.BLACK_87,
            weight=ft.FontWeight.W_500,
        )

        self.btn_siguiente = ft.OutlinedButton(
            "SIGUIENTE",
            icon=ft.Icons.CHEVRON_RIGHT,
            visible=False,
            disabled=True,
            on_click=self.pagina_siguiente,
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

        self.paginacion = ft.Row(
            width=760,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                self.btn_anterior,
                self.txt_pagina,
                self.btn_siguiente,
            ],
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
                self.fila_filtros,
                self.lista_postulaciones,
                self.paginacion,
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
                                    alignment=(
                                        ft.MainAxisAlignment.START
                                    ),
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
        self.offsets_previos = []

        self.oferta_filtro_id = None
        self.oferta_filtro_nombre = None
        self.oferta_seleccionada = None
        self.chip_filtro.visible = False

        await self.cargar_resultados(
            page,
            0,
            1,
        )

    async def buscar(self, e):
        """Método para realizar una búsqueda."""

        if self.cargando:
            return

        self.consulta_actual = (
            self.txt_busqueda.value
        )

        self.offsets_previos = []

        await self.cargar_resultados(
            self.page,
            0,
            1,
        )

    async def pagina_siguiente(self, e):
        """Método para ir a la página siguiente."""

        if self.cargando:
            return

        offset_actual = self.offset

        nuevo_offset = (
            self.offset + self.cantidad_actual
        )

        if await self.cargar_resultados(
            self.page,
            nuevo_offset,
            self.pagina + 1,
        ):
            self.offsets_previos.append(
                offset_actual
            )

    async def pagina_anterior(self, e):
        """Método para volver a la página anterior."""

        if self.cargando or not self.offsets_previos:
            return

        if await self.cargar_resultados(
            self.page,
            self.offsets_previos[-1],
            self.pagina - 1,
        ):
            self.offsets_previos.pop()

    async def cargar_resultados(
        self,
        page,
        offset: int,
        pagina: int,
    ):
        """Método para traer una página de postulaciones."""

        self.cargando = True

        self.lista_postulaciones.controls = [
            self.indicador_carga
        ]

        self.update()

        try:
            resultados = (
                await EmpleadorService.filtrar_postulaciones(
                    page,
                    oferta_id=self.oferta_filtro_id,
                    busqueda=(
                        self.consulta_actual or None
                    ),
                    offset=offset,
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
            self.lista_postulaciones.controls = [
                ft.Container(
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No se pudieron cargar las "
                        "postulaciones. Intentá nuevamente",
                        color=ft.Colors.BLACK_54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]

            self.update()

            self.cargando = False

            return False

        if not resultados and offset > 0:
            self.hay_mas = False

            self.btn_siguiente.visible = False
            self.btn_siguiente.disabled = True

            self.update()

            self.cargando = False

            return False

        self.offset = offset
        self.pagina = pagina

        self.postulaciones = (
            resultados or []
        )

        self.cantidad_actual = len(
            self.postulaciones
        )

        self.hay_mas = (
            self.cantidad_actual
            >= self.tamano_pagina
        )

        self.mostrar_postulaciones()

        self.cargando = False

        return True

    @staticmethod
    def _id_oferta(oferta: dict):
        """Obtiene el id de una oferta."""

        for clave in (
            "id",
            "oferta_id",
            "id_oferta",
        ):
            if oferta.get(clave) is not None:
                return oferta[clave]

        return None

    @staticmethod
    def _nombre_oferta(oferta: dict):
        """Obtiene el nombre de una oferta."""

        return (
            oferta.get("titulo_oferta")
            or oferta.get("nombre_oferta")
            or oferta.get("titulo")
            or oferta.get("nombre")
            or "Oferta sin título"
        )

    async def abrir_panel(self, e):
        """Abre el diálogo para elegir la oferta."""

        if self.cargando:
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
                    "querés filtrar las postulaciones.",
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
            disabled=(
                self.oferta_seleccionada is None
            ),
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
            visible=(
                self.oferta_filtro_id is not None
            ),
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
                    on_click=(
                        lambda e: self.page.pop_dialog()
                    ),
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

    async def cargar_ofertas(
        self,
        busqueda: str,
    ):
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

            await self.page.push_route(
                "/login"
            )

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

        self.lista_ofertas.controls = (
            self.cards_ofertas
        )

        self.lista_ofertas.update()

    def _card_oferta(
        self,
        oferta: dict,
    ):
        """Arma una card seleccionable de oferta."""

        datos = {
            "id": self._id_oferta(oferta),
            "nombre": self._nombre_oferta(oferta),
        }

        seleccionada = (
            self.oferta_seleccionada is not None
            and self.oferta_seleccionada["id"]
            == datos["id"]
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
                vertical_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
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

        self.oferta_seleccionada = (
            e.control.data
        )

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

            card.content.controls[-1].visible = (
                activa
            )

            card.update()

        self.btn_aplicar_filtro.disabled = False
        self.btn_aplicar_filtro.update()

    async def aplicar_filtro(self, e):
        """Aplica el filtro de oferta seleccionado."""

        if self.oferta_seleccionada is None:
            return

        self.oferta_filtro_id = (
            self.oferta_seleccionada["id"]
        )

        self.oferta_filtro_nombre = (
            self.oferta_seleccionada["nombre"]
        )

        self.txt_chip_filtro.value = (
            f"Oferta: {self.oferta_filtro_nombre}"
        )

        self.chip_filtro.visible = True

        self.page.pop_dialog()

        self.offsets_previos = []

        await self.cargar_resultados(
            self.page,
            0,
            1,
        )

    async def quitar_filtro(self, e):
        """Quita el filtro de oferta."""

        if self.cargando:
            return

        self.oferta_filtro_id = None
        self.oferta_filtro_nombre = None
        self.oferta_seleccionada = None
        self.chip_filtro.visible = False

        if e.control is self.btn_limpiar_filtro:
            self.page.pop_dialog()

        self.offsets_previos = []

        await self.cargar_resultados(
            self.page,
            0,
            1,
        )

    def mostrar_postulaciones(self):
        """Método para mostrar las postulaciones."""

        self.botones_por_postulacion = {}

        if not self.postulaciones:
            self.lista_postulaciones.controls = [
                ft.Container(
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No se encontraron postulaciones",
                        color=ft.Colors.BLACK_54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]

        else:
            self.lista_postulaciones.controls = [
                self._tarjeta_postulacion(
                    postulacion
                )
                for postulacion in self.postulaciones
            ]

        self.txt_pagina.value = (
            f"Página {self.pagina}"
        )

        hay_paginacion = (
            self.pagina > 1
            or self.hay_mas
        )

        self.btn_anterior.visible = hay_paginacion
        self.btn_siguiente.visible = hay_paginacion

        self.btn_anterior.disabled = (
            self.pagina == 1
        )

        self.btn_siguiente.disabled = (
            not self.hay_mas
        )

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

    @staticmethod
    def _boton_estilo(color):
        """Estilo común de los botones de la card."""

        return ft.ButtonStyle(
            color=color,
            side=ft.BorderSide(
                1.5,
                color,
            ),
            shape=ft.RoundedRectangleBorder(
                radius=12,
            ),
        )

    def _tarjeta_postulacion(
        self,
        postulacion: dict,
    ):
        """Método para armar una card de postulación."""

        nombre_postulante = (
            f"{postulacion.get('nombre_postulante', '')} "
            f"{postulacion.get('apellido_postulante', '')}"
        ).strip()

        titulo_oferta = postulacion.get(
            "titulo_oferta",
            "",
        )

        foto = postulacion.get(
            "foto_postulante"
        )

        fecha = self._formatear_fecha(
            postulacion.get(
                "fecha_postulacion"
            )
        )

        estado = postulacion.get(
            "estado"
        )

        (
            texto_estado,
            color_estado,
            fondo_estado,
        ) = self.ESTADOS_POSTULACION.get(
            estado,
            (
                estado or "—",
                ft.Colors.BLUE_GREY_400,
                ft.Colors.BLUE_GREY_50,
            ),
        )

        boton_perfil = ft.OutlinedButton(
            "VER PERFIL",
            data={
                "postulacion": postulacion,
                "texto": "VER PERFIL",
                "color": ft.Colors.BLUE_500,
            },
            on_click=self.ver_perfil_postulante,
            style=self._boton_estilo(
                ft.Colors.BLUE_500
            ),
        )

        botones = [boton_perfil]

        if estado == "PENDIENTE":
            botones.append(
                ft.OutlinedButton(
                    "ACEPTAR",
                    data={
                        "postulacion": postulacion,
                        "estado": "ACEPTADA",
                        "texto": "ACEPTAR",
                        "color": ft.Colors.GREEN_600,
                    },
                    on_click=self.confirmar_cambio_estado,
                    style=self._boton_estilo(
                        ft.Colors.GREEN_600
                    ),
                )
            )

            botones.append(
                ft.OutlinedButton(
                    "RECHAZAR",
                    data={
                        "postulacion": postulacion,
                        "estado": "RECHAZADA",
                        "texto": "RECHAZAR",
                        "color": ft.Colors.RED_500,
                    },
                    on_click=self.confirmar_cambio_estado,
                    style=self._boton_estilo(
                        ft.Colors.RED_500
                    ),
                )
            )

        self.botones_por_postulacion[
            postulacion.get("id")
        ] = botones

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
                                        ft.Icons.PERSON,
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
                                        nombre_postulante,
                                        size=16,
                                        weight=(
                                            ft.FontWeight.BOLD
                                        ),
                                        color=(
                                            ft.Colors.BLACK_87
                                        ),
                                    ),
                                    ft.Text(
                                        (
                                            "Postulado al "
                                            "puesto de "
                                            f"{titulo_oferta}"
                                        ),
                                        size=13,
                                        color=(
                                            ft.Colors.BLACK_54
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
                                            "Postulado el "
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
                        spacing=10,
                        controls=botones,
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

    def _bloquear_hermanos(
        self,
        boton,
        postulacion_id,
        bloquear: bool,
    ):
        """Deshabilita/habilita los demás botones de la card."""

        for otro in self.botones_por_postulacion.get(
            postulacion_id,
            [],
        ):
            if otro is boton:
                continue

            otro.disabled = bloquear

            try:
                otro.update()
            except RuntimeError:
                pass

    async def ver_perfil_postulante(self, e):
        """Carga el perfil del postulante y recién ahí navega."""

        if self.navegando or self.accionando:
            return

        boton = e.control
        datos = boton.data
        postulacion = datos["postulacion"]

        self.navegando = True

        self._estado_boton(
            boton,
            True,
            datos["texto"],
            datos["color"],
        )

        self._bloquear_hermanos(
            boton,
            postulacion.get("id"),
            True,
        )

        try:
            await self.perfil_postulante.cargar(
                self.page,
                postulacion["postulante_id"],
            )

            await self.page.push_route(
                "/perfil-postulante"
            )

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route("/login")

        except ErrorNoEncontrado:
            self.mostrar_mensaje(
                "No se encontró el postulante solicitado"
            )

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo cargar el perfil. Intentá nuevamente"
            )

        finally:
            self.navegando = False

            self._estado_boton(
                boton,
                False,
                datos["texto"],
                datos["color"],
            )

            self._bloquear_hermanos(
                boton,
                postulacion.get("id"),
                False,
            )

    def confirmar_cambio_estado(self, e):
        """Pide confirmación antes de aceptar o rechazar."""

        if self.navegando or self.accionando:
            return

        boton = e.control
        datos = boton.data
        postulacion = datos["postulacion"]
        nuevo_estado = datos["estado"]

        aceptar = nuevo_estado == "ACEPTADA"

        nombre = (
            f"{postulacion.get('nombre_postulante', '')} "
            f"{postulacion.get('apellido_postulante', '')}"
        ).strip()

        async def confirmar(ev):
            self.page.pop_dialog()

            await self.cambiar_estado(
                boton,
                datos,
            )

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    (
                        "Aceptar postulación"
                        if aceptar
                        else "Rechazar postulación"
                    ),
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                content=ft.Text(
                    (
                        f"¿Querés aceptar la postulación de "
                        f"{nombre}?"
                        if aceptar
                        else
                        f"¿Querés rechazar la postulación de "
                        f"{nombre}?"
                    ),
                    color=ft.Colors.BLACK_87,
                ),
                actions=[
                    ft.TextButton(
                        "CANCELAR",
                        on_click=(
                            lambda ev:
                            self.page.pop_dialog()
                        ),
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
                    ft.FilledButton(
                        "ACEPTAR" if aceptar else "RECHAZAR",
                        on_click=confirmar,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=(
                                ft.Colors.GREEN_600
                                if aceptar
                                else ft.Colors.RED_500
                            ),
                            shape=ft.RoundedRectangleBorder(
                                radius=10,
                            ),
                        ),
                    ),
                ],
            )
        )

    async def cambiar_estado(
        self,
        boton,
        datos: dict,
    ):
        """Llama al backend para aceptar o rechazar."""

        if self.accionando:
            return

        postulacion = datos["postulacion"]
        nuevo_estado = datos["estado"]

        self.accionando = True

        self._estado_boton(
            boton,
            True,
            datos["texto"],
            datos["color"],
        )

        self._bloquear_hermanos(
            boton,
            postulacion.get("id"),
            True,
        )

        exito = False

        try:
            await EmpleadorService.actualizar_estado_postulacion(
                self.page,
                estado=nuevo_estado,
                oferta_id=postulacion["oferta_id"],
                postulacion_id=postulacion["id"],
            )

            exito = True

        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route("/login")

        except ErrorNoEncontrado:
            self.mostrar_mensaje(
                "No se encontró la postulación"
            )

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo actualizar la postulación. "
                "Intentá nuevamente"
            )

        finally:
            self.accionando = False

            if not exito:
                self._estado_boton(
                    boton,
                    False,
                    datos["texto"],
                    datos["color"],
                )

                self._bloquear_hermanos(
                    boton,
                    postulacion.get("id"),
                    False,
                )

        if exito:
            postulacion["estado"] = nuevo_estado

            self.mostrar_postulaciones()

            self.mostrar_mensaje(
                "Postulación aceptada"
                if nuevo_estado == "ACEPTADA"
                else "Postulación rechazada"
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