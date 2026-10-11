import asyncio
from datetime import datetime

import flet as ft

from frontend.src.services.administrador_service import AdministradorService
from frontend.src.session.sesion import Sesion
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
    ErrorNoEncontrado,
)

# pylint: disable=E1121,E1123,E0401,E1101


class GestionReportesView(ft.View):

    ROL_ADMINISTRADOR = "ADMINISTRADOR"

    ROLES = {
        "POSTULANTE": (
            "Postulante",
            ft.Icons.PERSON,
        ),
        "EMPLEADOR": (
            "Empleador",
            ft.Icons.STOREFRONT,
        ),
    }

    FILTROS_REPORTE = {
        "PENDIENTE": (
            "PENDIENTES",
            ft.Icons.HOURGLASS_EMPTY,
        ),
        "REVISADO": (
            "REVISADOS",
            ft.Icons.CHECK_CIRCLE_OUTLINE,
        ),
        "SANCIONADO": (
            "SANCIONADOS",
            ft.Icons.GAVEL,
        ),
    }

    ESTADOS_REPORTE = {
        "PENDIENTE": (
            "Pendiente",
            ft.Colors.BLUE_500,
            ft.Colors.BLUE_50,
        ),
        "REVISADO": (
            "Revisado",
            ft.Colors.GREEN_600,
            ft.Colors.GREEN_50,
        ),
        "SANCIONADO": (
            "Sancionado",
            ft.Colors.RED_500,
            ft.Colors.RED_50,
        ),
    }

    def __init__(self):
        super().__init__()

        self.route = "/gestion-reportes"
        self.padding = 0
        self.spacing = 0
        self.expand = True

        self.bg_image = ft.Image(
            src="images/LaburAR_bg3.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.reportes = []
        self.cargando = False
        self.accionando = False
        self.consulta_actual = ""
        self.filtro_actual = "PENDIENTE"

        self.tamano_pagina = 10
        self.offset = 0
        self.pagina = 1
        self.cantidad_actual = 0
        self.offsets_previos = []
        self.hay_mas = False
        self.pagina_vacia = False

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
            "GESTIÓN DE REPORTES",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK_87,
            text_align=ft.TextAlign.CENTER,
            font_family="Inter-Bold",
        )

        self.txt_busqueda = ft.TextField(
            hint_text="Buscar reporte",
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
            content=ft.Text(
                self.FILTROS_REPORTE[
                    self.filtro_actual
                ][0],
                color=ft.Colors.BLUE_500,
            ),
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

        self.fila_filtros = ft.Row(
            width=760,
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.filtros,
            ],
        )

        self.lista_reportes = ft.Column(
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
                self.lista_reportes,
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
                                    alignment=(
                                        ft.Alignment.TOP_CENTER
                                    ),
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

    async def _acceso_denegado(self, page):
        """Avisa que no tiene permisos y lo saca de la vista."""

        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text(
                    "Acceso denegado"
                ),
                content=ft.Text(
                    "No tenés permisos para acceder "
                    "a esta sección."
                ),
            )
        )

        await asyncio.sleep(3)

        try:
            page.pop_dialog()
        except RuntimeError:
            pass

        await page.push_route(
            "/login"
        )

    async def cargar(self, page):
        """Método para la carga inicial de la vista."""

        if Sesion.rol(page) != self.ROL_ADMINISTRADOR:

            self.lista_reportes.controls = []

            await self._acceso_denegado(page)

            return

        self.consulta_actual = ""
        self.txt_busqueda.value = ""
        self.offsets_previos = []

        self.filtro_actual = "PENDIENTE"

        self.filtros.content = ft.Text(
            self.FILTROS_REPORTE[
                self.filtro_actual
            ][0],
            color=ft.Colors.BLUE_500,
        )

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
        """Método para traer una página de reportes."""

        self.cargando = True
        self.pagina_vacia = False

        self.lista_reportes.controls = [
            self.indicador_carga
        ]

        self.update()

        try:

            resultados = (
                await AdministradorService.buscar_reportes(
                    page,
                    filtros=self.filtro_actual,
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

            self.lista_reportes.controls = [
                ft.Container(
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No se pudieron cargar los "
                        "reportes. Intentá nuevamente",
                        color=ft.Colors.BLACK_54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]

            self.update()

            self.cargando = False

            return False

        if not resultados and offset > 0:

            self.pagina_vacia = True

            self.hay_mas = False

            self.mostrar_reportes()

            self.cargando = False

            return False

        self.offset = offset
        self.pagina = pagina

        self.reportes = (
            resultados or []
        )

        self.cantidad_actual = len(
            self.reportes
        )

        self.hay_mas = (
            self.cantidad_actual
            >= self.tamano_pagina
        )

        self.mostrar_reportes()

        self.cargando = False

        return True

    async def abrir_panel(self, e):
        """Abre el diálogo para elegir el estado del reporte."""

        if self.cargando:
            return

        opciones = []

        for clave, (texto, icono) in (
            self.FILTROS_REPORTE.items()
        ):

            seleccionada = (
                clave == self.filtro_actual
            )

            opciones.append(
                ft.Container(
                    data=clave,
                    on_click=self.seleccionar_filtro,
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
                                icono,
                                color=ft.Colors.BLUE_GREY_400,
                            ),
                            ft.Text(
                                texto,
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
            )

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    "Filtrar por estado de reporte",
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                content=ft.Container(
                    width=500,
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Column(
                        tight=True,
                        spacing=10,
                        controls=opciones,
                    ),
                ),
                actions=[
                    ft.TextButton(
                        "CANCELAR",
                        on_click=(
                            lambda e:
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
                ],
            )
        )

    async def seleccionar_filtro(self, e):
        """Aplica el estado elegido y recarga."""

        self.filtro_actual = e.control.data

        self.filtros.content = ft.Text(
            self.FILTROS_REPORTE[
                self.filtro_actual
            ][0],
            color=ft.Colors.BLUE_500,
        )

        self.page.pop_dialog()

        self.offsets_previos = []

        await self.cargar_resultados(
            self.page,
            0,
            1,
        )

    def mostrar_reportes(self):
        """Método para mostrar los reportes."""

        if not self.reportes:

            self.lista_reportes.controls = [
                ft.Container(
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No se encontraron reportes",
                        color=ft.Colors.BLACK_54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]

        else:

            self.lista_reportes.controls = [
                self._tarjeta_reporte(reporte)
                for reporte in self.reportes
            ]

        self.txt_pagina.value = (
            f"Página {self.pagina}"
        )

        self.btn_anterior.visible = (
            self.pagina > 1
        )

        self.btn_siguiente.visible = (
            self.hay_mas
        )

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
    def _id_reporte(reporte: dict):
        """Obtiene el id de un reporte."""

        for clave in (
            "id",
            "reporte_id",
            "id_reporte",
        ):
            if reporte.get(clave) is not None:
                return reporte[clave]

        return None

    @staticmethod
    def _fecha_reporte(reporte: dict):
        """Obtiene la fecha de un reporte."""

        return (
            reporte.get("fecha_reporte")
            or reporte.get("fecha_creacion")
            or reporte.get("fecha")
        )

    def _chip_estado(self, estado):
        """Arma el chip de estado de un reporte."""

        (
            texto_estado,
            color_estado,
            fondo_estado,
        ) = self.ESTADOS_REPORTE.get(
            estado,
            (
                estado or "—",
                ft.Colors.BLUE_GREY_400,
                ft.Colors.BLUE_GREY_50,
            ),
        )

        return ft.Container(
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
                weight=ft.FontWeight.W_500,
            ),
        )

    def _texto_roles(self, reporte: dict):
        """Texto 'Reporta: X → Reportado: Y' de un reporte."""

        reportante = self.ROLES.get(
            reporte.get("rol_reportante"),
            ("—",),
        )[0]

        reportado = self.ROLES.get(
            reporte.get("rol_reportado"),
            ("—",),
        )[0]

        return (
            f"Reporta: {reportante}  →  "
            f"Reportado: {reportado}"
        )

    def _tarjeta_reporte(
        self,
        reporte: dict,
    ):
        """Método para armar una card de reporte."""

        motivo = reporte.get(
            "motivo",
            "",
        )

        descripcion = reporte.get(
            "descripcion",
            "",
        )

        fecha = self._formatear_fecha(
            self._fecha_reporte(reporte)
        )

        estado = reporte.get(
            "estado"
        )

        controles = [
            ft.Row(
                vertical_alignment=(
                    ft.CrossAxisAlignment.START
                ),
                spacing=15,
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=4,
                        controls=[
                            ft.Text(
                                motivo,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK_87,
                            ),
                            ft.Text(
                                descripcion,
                                size=13,
                                color=ft.Colors.BLACK_54,
                                max_lines=2,
                                overflow=(
                                    ft.TextOverflow.ELLIPSIS
                                ),
                            ),
                            ft.Text(
                                self._texto_roles(reporte),
                                size=12,
                                color=ft.Colors.BLUE_GREY_400,
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                    ),
                    ft.Column(
                        horizontal_alignment=(
                            ft.CrossAxisAlignment.END
                        ),
                        spacing=8,
                        controls=[
                            self._chip_estado(estado),
                            ft.Text(
                                (
                                    "Reportado el "
                                    f"{fecha}"
                                ),
                                size=11,
                                color=ft.Colors.BLACK_45,
                            ),
                        ],
                    ),
                ],
            ),
        ]

        controles.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.OutlinedButton(
                        "REVISAR",
                        data={
                            "reporte": reporte,
                            "texto": "REVISAR",
                            "color": ft.Colors.BLUE_500,
                        },
                        on_click=self.abrir_revision,
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
                    ),
                ],
            )
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
                controls=controles,
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

    async def _cargar_resumen_usuario(
        self,
        rol,
        usuario_id,
    ):
        """Trae nombre y foto de un usuario según su rol."""

        if usuario_id is None or rol not in self.ROLES:
            return None

        try:

            if rol == "POSTULANTE":

                datos = (
                    await AdministradorService
                    .obtener_postulante_usuario_id(
                        page=self.page,
                        usuario_id=usuario_id,
                    )
                )

                nombre = (
                    f"{datos.get('nombre') or ''} "
                    f"{datos.get('apellido') or ''}"
                ).strip()

            else:

                datos = (
                    await AdministradorService
                    .obtener_empleador_usuario_id(
                        page=self.page,
                        usuario_id=usuario_id,
                    )
                )

                nombre = (
                    datos.get("nombre_negocio") or ""
                )

        except (
            ErrorNoEncontrado,
            ErrorServidor,
        ):

            return None

        return {
            "nombre": nombre or "Sin nombre",
            "foto": (
                datos.get("foto_perfil")
                or datos.get("foto_perfil_postulante")
                or datos.get("foto")
            ),
        }

    def _bloque_usuario(
        self,
        titulo: str,
        rol,
        resumen,
    ):
        """Bloque con foto, nombre y rol de una de las partes."""

        etiqueta_rol, icono = self.ROLES.get(
            rol,
            ("—", ft.Icons.PERSON),
        )

        foto = (
            resumen.get("foto")
            if resumen
            else None
        )

        nombre = (
            resumen["nombre"]
            if resumen
            else "No se pudo cargar el perfil"
        )

        return ft.Container(
            expand=True,
            padding=15,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
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
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                controls=[
                    ft.Text(
                        titulo,
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_GREY_400,
                    ),
                    ft.CircleAvatar(
                        radius=45,
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
                                size=40,
                                color=(
                                    ft.Colors.BLUE_GREY_400
                                ),
                            )
                        ),
                    ),
                    ft.Text(
                        nombre,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_87,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        bgcolor=ft.Colors.BLUE_GREY_50,
                        border_radius=20,
                        padding=ft.Padding(
                            left=12,
                            top=4,
                            right=12,
                            bottom=4,
                        ),
                        content=ft.Text(
                            etiqueta_rol,
                            size=12,
                            color=ft.Colors.BLUE_GREY_400,
                            weight=ft.FontWeight.W_500,
                        ),
                    ),
                ],
            ),
        )

    async def abrir_revision(self, e):
        """Carga los perfiles involucrados y abre el panel."""

        if self.accionando:
            return

        boton = e.control
        datos = boton.data
        reporte = datos["reporte"]

        self.accionando = True

        self._estado_boton(
            boton,
            True,
            datos["texto"],
            datos["color"],
        )

        try:

            reportante, reportado = await asyncio.gather(
                self._cargar_resumen_usuario(
                    reporte.get("rol_reportante"),
                    reporte.get("usuario_reportante_id"),
                ),
                self._cargar_resumen_usuario(
                    reporte.get("rol_reportado"),
                    reporte.get("usuario_reportado_id"),
                ),
            )

        except ErrorAutenticacion:

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

            return

        finally:

            self.accionando = False

            self._estado_boton(
                boton,
                False,
                datos["texto"],
                datos["color"],
            )

        self._mostrar_panel_revision(
            boton,
            datos,
            reportante,
            reportado,
        )

    def _mostrar_panel_revision(
        self,
        boton,
        datos: dict,
        reportante,
        reportado,
    ):
        """Muestra el reporte completo con quién reporta a quién.

        Se puede abrir en cualquier estado. Las acciones disponibles
        dependen del estado:
        - Pendiente: marcar como revisado o sancionar.
        - Revisado: sancionar.
        - Sancionado: solo ver el detalle.
        """

        reporte = datos["reporte"]

        estado = reporte.get("estado")

        fecha = self._formatear_fecha(
            self._fecha_reporte(reporte)
        )

        async def marcar_revisado(ev):

            self.page.pop_dialog()

            await self.ejecutar_accion(
                boton,
                datos,
                "REVISADO",
            )

        def sancionar(ev):

            if reporte.get("usuario_reportado_id") is None:

                self.mostrar_mensaje(
                    "No se pudo identificar al usuario reportado"
                )

                return

            self.page.pop_dialog()

            self._mostrar_dialogo_sancion(
                boton,
                datos,
                reportante,
                reportado,
            )

        contenido = ft.Column(
            expand=True,
            spacing=18,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    spacing=10,
                    vertical_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),
                    controls=[
                        self._bloque_usuario(
                            "REPORTANTE",
                            reporte.get("rol_reportante"),
                            reportante,
                        ),
                        ft.Icon(
                            ft.Icons.ARROW_FORWARD,
                            color=ft.Colors.BLUE_GREY_400,
                            size=28,
                        ),
                        self._bloque_usuario(
                            "REPORTADO",
                            reporte.get("rol_reportado"),
                            reportado,
                        ),
                    ],
                ),
                ft.Row(
                    alignment=(
                        ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    controls=[
                        self._chip_estado(
                            reporte.get("estado")
                        ),
                        ft.Text(
                            f"Reportado el {fecha}",
                            size=12,
                            color=ft.Colors.BLACK_54,
                        ),
                    ],
                ),
                ft.Container(
                    padding=15,
                    border_radius=15,
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=12,
                        color=ft.Colors.with_opacity(
                            0.08,
                            ft.Colors.BLACK,
                        ),
                        offset=ft.Offset(0, 5),
                    ),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                reporte.get(
                                    "motivo",
                                    "",
                                ),
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK_87,
                            ),
                            ft.Text(
                                reporte.get(
                                    "descripcion",
                                    "",
                                ),
                                size=14,
                                color=ft.Colors.BLACK_87,
                            ),
                        ],
                    ),
                ),
            ],
        )

        acciones = [
            ft.TextButton(
                "CERRAR",
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
        ]

        if estado == "PENDIENTE":

            acciones.append(
                ft.FilledButton(
                    "MARCAR REVISADO",
                    on_click=marcar_revisado,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.GREEN_600,
                        shape=ft.RoundedRectangleBorder(
                            radius=10,
                        ),
                    ),
                )
            )

        if estado in ("PENDIENTE", "REVISADO"):

            acciones.append(
                ft.FilledButton(
                    "SANCIONAR",
                    on_click=sancionar,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED_500,
                        shape=ft.RoundedRectangleBorder(
                            radius=10,
                        ),
                    ),
                )
            )

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    (
                        "Revisar reporte"
                        if estado == "PENDIENTE"
                        else "Detalle del reporte"
                    ),
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                content=ft.Container(
                    width=820,
                    height=560,
                    bgcolor=ft.Colors.WHITE,
                    content=contenido,
                ),
                actions=acciones,
            )
        )

    def _mostrar_dialogo_sancion(
        self,
        boton,
        datos: dict,
        reportante,
        reportado,
    ):
        """Pregunta qué hacer con el usuario reportado al sancionar."""

        nombre = (
            reportado["nombre"]
            if reportado
            else "el usuario reportado"
        )

        async def aplicar(medida: str):

            self.page.pop_dialog()

            await self.ejecutar_accion(
                boton,
                datos,
                "SANCIONADO",
                medida=medida,
            )

        async def desactivar(ev):

            await aplicar("DESACTIVAR")

        async def banear(ev):

            await aplicar("BANEAR")

        def cancelar(ev):

            self.page.pop_dialog()

            self._mostrar_panel_revision(
                boton,
                datos,
                reportante,
                reportado,
            )

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    "Sancionar reporte",
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                content=ft.Container(
                    width=460,
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Column(
                        tight=True,
                        spacing=12,
                        controls=[
                            ft.Text(
                                f"¿Qué querés hacer con {nombre}?",
                                size=15,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.BLACK_87,
                            ),
                            ft.Text(
                                "DESACTIVAR: la cuenta queda "
                                "desactivada.",
                                size=13,
                                color=ft.Colors.BLACK_54,
                            ),
                            ft.Text(
                                "BANEAR: la cuenta queda baneada y "
                                "no podrá volver a usarse.",
                                size=13,
                                color=ft.Colors.BLACK_54,
                            ),
                        ],
                    ),
                ),
                actions=[
                    ft.TextButton(
                        "CANCELAR",
                        on_click=cancelar,
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
                        "DESACTIVAR",
                        on_click=desactivar,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_500,
                            shape=ft.RoundedRectangleBorder(
                                radius=10,
                            ),
                        ),
                    ),
                    ft.FilledButton(
                        "BANEAR",
                        on_click=banear,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.RED_500,
                            shape=ft.RoundedRectangleBorder(
                                radius=10,
                            ),
                        ),
                    ),
                ],
            )
        )

    async def ejecutar_accion(
        self,
        boton,
        datos: dict,
        estado: str,
        medida: str | None = None,
    ):
        """Actualiza el estado del reporte en el backend."""

        if self.accionando:
            return

        reporte = datos["reporte"]

        self.accionando = True

        self._estado_boton(
            boton,
            True,
            datos["texto"],
            datos["color"],
        )

        exito = False
        medida_aplicada = False

        try:

            usuario_id = reporte.get(
                "usuario_reportado_id"
            )

            if medida == "BANEAR":

                await AdministradorService.banear_usuario(
                    self.page,
                    banear_usuario_id=usuario_id,
                )

                medida_aplicada = True

            elif medida == "DESACTIVAR":

                await AdministradorService.desactivar_usuario(
                    self.page,
                    desactivar_usuario_id=usuario_id,
                )

                medida_aplicada = True

            await AdministradorService.actualizar_reporte_estado(
                self.page,
                estado=estado,
                reporte_id=self._id_reporte(reporte),
            )

            exito = True

        except ErrorAutenticacion:

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route(
                "/login"
            )

        except ErrorNoEncontrado:

            self.mostrar_mensaje(
                "No se encontró el usuario o el reporte"
            )

        except ErrorServidor:

            if medida_aplicada:

                self.mostrar_mensaje(
                    "Se aplicó la medida al usuario, pero no se "
                    "pudo actualizar el reporte. Intentá nuevamente"
                )

            else:

                self.mostrar_mensaje(
                    "No se pudo completar la acción. "
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

        if not exito:
            return

        if medida == "BANEAR":

            self.mostrar_mensaje(
                "Reporte sancionado: usuario baneado"
            )

        elif medida == "DESACTIVAR":

            self.mostrar_mensaje(
                "Reporte sancionado: usuario desactivado"
            )

        elif estado == "REVISADO":

            self.mostrar_mensaje(
                "Reporte marcado como revisado"
            )

        else:

            self.mostrar_mensaje(
                "Reporte sancionado"
            )

        await self.cargar_resultados(
            self.page,
            self.offset,
            self.pagina,
        )

        if self.pagina_vacia and self.offsets_previos:

            if await self.cargar_resultados(
                self.page,
                self.offsets_previos[-1],
                self.pagina - 1,
            ):
                self.offsets_previos.pop()

    async def volver(self, e):
        """Método para volver al perfil personal del administrador."""

        await self.page.push_route(
            "/perfil-personal-administrador"
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