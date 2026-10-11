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


class GestionUsuariosView(ft.View):

    ROL_ADMINISTRADOR = "ADMINISTRADOR"

    def __init__(
        self,
        perfil_postulante,
        perfil_empleador,
    ):
        super().__init__()

        self.perfil_postulante = perfil_postulante
        self.perfil_empleador = perfil_empleador

        self.route = "/gestion-usuarios"
        self.padding = 0
        self.spacing = 0
        self.bgcolor = ft.Colors.TRANSPARENT
        self.expand = True

        self.bg_image = ft.Image(
            src="images/LaburAR_bg3.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.usuarios = []
        self.cargando = False
        self.navegando = False
        self.accionando = False
        self.consulta_actual = ""
        self.filtro_actual = "POSTULANTE"

        self.tamano_pagina = 10
        self.offset = 0
        self.pagina = 1
        self.cantidad_actual = 0
        self.offsets_previos = []
        self.hay_mas = False

        self.botones_por_usuario = {}

        self.FILTROS_USUARIO = {
            "POSTULANTE": (
                "POSTULANTES",
                ft.Icons.PERSON_OUTLINE,
            ),
            "EMPLEADOR": (
                "EMPLEADORES",
                ft.Icons.STOREFRONT,
            ),
        }

        self.ESTADOS_USUARIO = {
            "ACTIVO": (
                "Activo",
                ft.Colors.GREEN_600,
                ft.Colors.GREEN_50,
            ),
            "DESACTIVADO": (
                "Desactivado",
                ft.Colors.BLUE_500,
                ft.Colors.BLUE_50,
            ),
            "BANEADO": (
                "Baneado",
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
            "GESTIÓN DE USUARIOS",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK_87,
            text_align=ft.TextAlign.CENTER,
            font_family="Inter-Bold",
        )

        self.txt_busqueda = ft.TextField(
            hint_text="Buscar usuario",
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

        self.filtros = ft.OutlinedButton(
            content=ft.Text(
                self.FILTROS_USUARIO[
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

        self.fila_filtros = ft.Row(
            width=760,
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.filtros,
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

        self.lista_usuarios = ft.Column(
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
                self.lista_usuarios,
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
            )
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

            self.lista_usuarios.controls = []

            await self._acceso_denegado(page)

            return

        self.consulta_actual = ""
        self.txt_busqueda.value = ""
        self.offsets_previos = []

        self.filtro_actual = "POSTULANTE"

        self.filtros.content = ft.Text(
            self.FILTROS_USUARIO[
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
        """Método para traer una página de usuarios."""

        self.cargando = True

        self.lista_usuarios.controls = [
            self.indicador_carga
        ]

        self.update()

        try:

            resultados = (
                await AdministradorService.buscar_usuarios(
                    page,
                    filtro=self.filtro_actual,
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

            self.lista_usuarios.controls = [
                ft.Container(
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No se pudieron cargar los "
                        "usuarios. Intentá nuevamente",
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

        self.usuarios = (
            resultados or []
        )

        self.cantidad_actual = len(
            self.usuarios
        )

        self.hay_mas = (
            self.cantidad_actual
            >= self.tamano_pagina
        )

        self.mostrar_usuarios()

        self.cargando = False

        return True

    async def abrir_panel(self, e):
        """Abre el diálogo para elegir postulantes o empleadores."""

        if self.cargando:
            return

        opciones = []

        for clave, (texto, icono) in (
            self.FILTROS_USUARIO.items()
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
                    "Filtrar por tipo de usuario",
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
        """Aplica el tipo de usuario elegido y recarga."""

        self.filtro_actual = e.control.data

        self.filtros.content = ft.Text(
            self.FILTROS_USUARIO[
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

    def mostrar_usuarios(self):
        """Método para mostrar los usuarios."""

        self.botones_por_usuario = {}

        if not self.usuarios:

            self.lista_usuarios.controls = [
                ft.Container(
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No se encontraron usuarios",
                        color=ft.Colors.BLACK_54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]

        else:

            self.lista_usuarios.controls = [
                self._tarjeta_usuario(usuario)
                for usuario in self.usuarios
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
    def _nombre_usuario(usuario: dict):
        """Nombre a mostrar según el rol del usuario."""

        if usuario.get("rol") == "EMPLEADOR":

            return (
                usuario.get("nombre_negocio")
                or "Negocio sin nombre"
            )

        return (
            f"{usuario.get('nombre_postulante') or ''} "
            f"{usuario.get('apellido_postulante') or ''}"
        ).strip() or "Usuario sin nombre"

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

    def _tarjeta_usuario(
        self,
        usuario: dict,
    ):
        """Método para armar una card de usuario."""

        nombre = self._nombre_usuario(usuario)

        foto = usuario.get(
            "foto_perfil"
        )

        fecha = self._formatear_fecha(
            usuario.get(
                "fecha_creacion"
            )
        )

        estado = usuario.get(
            "estado"
        )

        es_empleador = (
            usuario.get("rol") == "EMPLEADOR"
        )

        (
            texto_estado,
            color_estado,
            fondo_estado,
        ) = self.ESTADOS_USUARIO.get(
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
                "usuario": usuario,
                "texto": "VER PERFIL",
                "color": ft.Colors.BLUE_500,
            },
            on_click=self.ver_perfil_usuario,
            style=self._boton_estilo(
                ft.Colors.BLUE_500
            ),
        )

        botones = [boton_perfil]

        if estado == "ACTIVO":

            botones.append(
                ft.OutlinedButton(
                    "DESACTIVAR",
                    data={
                        "usuario": usuario,
                        "accion": "DESACTIVAR",
                        "texto": "DESACTIVAR",
                        "color": ft.Colors.BLUE_500,
                    },
                    on_click=self.confirmar_accion,
                    style=self._boton_estilo(
                        ft.Colors.BLUE_500
                    ),
                )
            )

        if estado in ("ACTIVO", "DESACTIVADO"):

            botones.append(
                ft.OutlinedButton(
                    "BANEAR",
                    data={
                        "usuario": usuario,
                        "accion": "BANEAR",
                        "texto": "BANEAR",
                        "color": ft.Colors.RED_500,
                    },
                    on_click=self.confirmar_accion,
                    style=self._boton_estilo(
                        ft.Colors.RED_500
                    ),
                )
            )

        if estado == "DESACTIVADO":

            botones.append(
                ft.OutlinedButton(
                    "ACTIVAR",
                    data={
                        "usuario": usuario,
                        "accion": "ACTIVAR",
                        "texto": "ACTIVAR",
                        "color": ft.Colors.GREEN_600,
                    },
                    on_click=self.confirmar_accion,
                    style=self._boton_estilo(
                        ft.Colors.GREEN_600
                    ),
                )
            )

        self.botones_por_usuario[
            usuario.get("usuario_id")
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
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(
                    0.06,
                    ft.Colors.BLACK,
                ),
                offset=ft.Offset(0, 3),
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
                                        (
                                            ft.Icons.STOREFRONT
                                            if es_empleador
                                            else ft.Icons.PERSON
                                        ),
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
                                        nombre,
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
                                            "Creado el "
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
        usuario_id,
        bloquear: bool,
    ):
        """Deshabilita/habilita los demás botones de la card."""

        for otro in self.botones_por_usuario.get(
            usuario_id,
            [],
        ):
            if otro is boton:
                continue

            otro.disabled = bloquear

            try:
                otro.update()
            except RuntimeError:
                pass

    async def ver_perfil_usuario(self, e):
        """Carga el perfil del usuario y recién ahí navega."""

        if self.navegando or self.accionando:
            return

        boton = e.control
        datos = boton.data
        usuario = datos["usuario"]

        self.navegando = True

        self._estado_boton(
            boton,
            True,
            datos["texto"],
            datos["color"],
        )

        self._bloquear_hermanos(
            boton,
            usuario.get("usuario_id"),
            True,
        )

        try:

            if usuario.get("rol") == "EMPLEADOR":

                await self.perfil_empleador.cargar(
                    self.page,
                    usuario["empleador_id"],
                )

                ruta = "/perfil-empleador"

            else:

                await self.perfil_postulante.cargar(
                    self.page,
                    usuario["postulante_id"],
                )

                ruta = "/perfil-postulante"

            await self.page.push_route(ruta)

        except ErrorAutenticacion:

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route("/login")

        except ErrorNoEncontrado:

            self.mostrar_mensaje(
                "No se encontró el perfil solicitado"
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
                usuario.get("usuario_id"),
                False,
            )

    def confirmar_accion(self, e):
        """Pide confirmación antes de activar, desactivar o banear."""

        if self.navegando or self.accionando:
            return

        boton = e.control
        datos = boton.data
        usuario = datos["usuario"]

        accion = datos["accion"]

        nombre = self._nombre_usuario(usuario)

        async def confirmar(ev):

            self.page.pop_dialog()

            await self.ejecutar_accion(
                boton,
                datos,
            )

        if accion == "BANEAR":

            titulo = "Banear usuario"

            mensaje = (
                f"¿Seguro que querés banear a {nombre}? "
                "No podrá volver a usar su cuenta."
            )

            texto_confirmar = "BANEAR"
            color_confirmar = ft.Colors.RED_500

        elif accion == "DESACTIVAR":

            titulo = "Desactivar usuario"

            mensaje = (
                f"¿Seguro que querés desactivar a {nombre}?"
            )

            texto_confirmar = "DESACTIVAR"
            color_confirmar = ft.Colors.BLUE_500

        else:

            titulo = "Activar usuario"

            mensaje = (
                f"¿Seguro que querés activar nuevamente "
                f"a {nombre}?"
            )

            texto_confirmar = "ACTIVAR"
            color_confirmar = ft.Colors.GREEN_600

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    titulo,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                content=ft.Text(
                    mensaje,
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
                        texto_confirmar,
                        on_click=confirmar,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=color_confirmar,
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
    ):
        """Llama al backend para activar, desactivar o banear."""

        if self.accionando:
            return

        usuario = datos["usuario"]
        accion = datos["accion"]

        self.accionando = True

        self._estado_boton(
            boton,
            True,
            datos["texto"],
            datos["color"],
        )

        self._bloquear_hermanos(
            boton,
            usuario.get("usuario_id"),
            True,
        )

        exito = False

        try:

            if accion == "BANEAR":

                await AdministradorService.banear_usuario(
                    self.page,
                    banear_usuario_id=usuario["usuario_id"],
                )

            elif accion == "DESACTIVAR":

                await AdministradorService.desactivar_usuario(
                    self.page,
                    desactivar_usuario_id=usuario["usuario_id"],
                )

            elif accion == "ACTIVAR":

                await AdministradorService.activar_usuario(
                    self.page,
                    activar_usuario_id=usuario["usuario_id"],
                )

            exito = True

        except ErrorAutenticacion:

            self.mostrar_dialogo_sesion_expirada()

            await asyncio.sleep(5)

            await self.page.push_route("/login")

        except ErrorNoEncontrado:

            self.mostrar_mensaje(
                "No se encontró el usuario"
            )

        except ErrorServidor:

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

                self._bloquear_hermanos(
                    boton,
                    usuario.get("usuario_id"),
                    False,
                )

        if exito:

            if accion == "BANEAR":

                usuario["estado"] = "BANEADO"

            elif accion == "DESACTIVAR":

                usuario["estado"] = "DESACTIVADO"

            elif accion == "ACTIVAR":

                usuario["estado"] = "ACTIVO"

            self.mostrar_usuarios()

            if accion == "BANEAR":

                mensaje = "Usuario baneado"

            elif accion == "DESACTIVAR":

                mensaje = "Usuario desactivado"

            else:

                mensaje = "Usuario activado"

            self.mostrar_mensaje(mensaje)

    async def volver(self, e):
        """Método para volver al perfil personal del administrador."""

        await self.page.push_route(
            "/perfil-personal-administrador"
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