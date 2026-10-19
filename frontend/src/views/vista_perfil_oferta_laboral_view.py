import asyncio
import math
import flet as ft
from frontend.src.session.sesion import Sesion
from frontend.src.services.oferta_laboral_service import OfertaLaboralService
from frontend.src.services.postulante_service import PostulanteService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
    ErrorNoEncontrado,
)
# pylint: disable=E1121,E1123,E0401, E1101

class PerfilOfertaLaboralView(ft.View):
    ANCHO_COLUMNA = 320
    JORNADAS = {
        "COMPLETA": "Completa",
        "MEDIA_JORNADA": "Media jornada",
        "TEMPORAL": "Temporal",
        "A_CONVENIR": "A convenir",
    }
    TURNOS = {
        "MAÑANA": "Mañana",
        "TARDE": "Tarde",
        "NOCHE": "Noche",
        "A_CONVENIR": "A convenir",
    }
    TIPOS_SALARIO = {
        "FIJO": "Fijo",
        "RANGO": "Rango",
        "A_CONVENIR": "A convenir",
        "NO_INFORMAR": "No informado",
    }

    def __init__(self):
        super().__init__()
        self.route = "/perfil-oferta"
        self.padding = 0
        self.spacing = 0
        self.expand = True
        self.bgcolor = ft.Colors.BLUE_GREY_50
        self.oferta_id = None
        self.conexion = None
        self.cargando_oferta = False
        self.cargando_postulacion = False
        self.cargando_aceptacion = False
        self.bg_image = ft.Image(
            src="images/LaburAR_bg6.jpeg",
            fit=ft.BoxFit.COVER,
            expand=True,
        )
        self.avatar = ft.CircleAvatar(
            radius=35,
            bgcolor=ft.Colors.BLUE_GREY_100,
            content=ft.Icon(
                ft.Icons.BUSINESS,
                size=30,
                color=ft.Colors.BLUE_GREY_400,
            ),
        )
        self.txt_titulo = ft.Text(
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK_87,
            font_family="Inter-Bold",
        )
        self.txt_ubicacion = ft.Text(
            size=13,
            color=ft.Colors.BLACK_54,
        )
        self.txt_direccion = ft.Text(
            size=13,
            color=ft.Colors.BLACK_45,
        )
        self.btn_postularse = ft.OutlinedButton(
            "POSTULARSE",
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
            on_click=self.postularse,
        )
        self.btn_aceptar_solicitud = ft.OutlinedButton(
            "ACEPTAR SOLICITUD",
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
            on_click=self.confirmar_aceptar_solicitud,
        )
        self.btn_conversacion = ft.FilledButton(
            "CONVERSACIÓN",
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_500,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(
                    radius=10,
                ),
            ),
            on_click=self.abrir_conversacion,
        )
        self.txt_estado = ft.Text(
            color=ft.Colors.BLACK_54,
            size=13,
            weight=ft.FontWeight.W_500,
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
                                    self.txt_titulo,
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            self.txt_ubicacion,
                                            self.txt_direccion,
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.btn_postularse,
                            self.btn_aceptar_solicitud,
                            self.btn_conversacion,
                            self.txt_estado,
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
                        "DESCRIPCIÓN DE OFERTA LABORAL",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12,
                    ),
                    self.txt_descripcion,
                ],
            ),
        )
        self.contenido_jornada = ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.tarjeta_jornada = ft.Container(
            width=self.ANCHO_COLUMNA,
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
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Text(
                        "JORNADA",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12,
                    ),
                    self.contenido_jornada,
                ],
            ),
        )
        self.contenido_salario = ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.tarjeta_salario = ft.Container(
            width=self.ANCHO_COLUMNA,
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
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Text(
                        "SALARIO",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12,
                    ),
                    self.contenido_salario,
                ],
            ),
        )
        self.fila_habilidades = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8,
        )
        self.tarjeta_habilidades = ft.Container(
            width=self.ANCHO_COLUMNA,
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
                        "REQUISITOS",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_54,
                        font_family="Inter-Bold",
                        size=12,
                    ),
                    self.fila_habilidades,
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
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        self.tarjeta_descripcion,
                        ft.Column(
                            spacing=20,
                            controls=[
                                self.tarjeta_jornada,
                                self.tarjeta_salario,
                                self.tarjeta_habilidades,
                            ],
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
        self.ocultar_acciones()

    def _contenido_cargando(self, texto="Cargando..."):
        """Contenido visual para indicar que se esta cargando."""
        return ft.Row(
            tight=True,
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ProgressRing(
                    width=16,
                    height=16,
                    stroke_width=2,
                    color=ft.Colors.BLUE_500,
                ),
                ft.Text(
                    texto,
                    color=ft.Colors.BLUE_500,
                ),
            ],
        )

    def _contenido_cargando_blanco(self, texto="Cargando..."):
        """Contenido visual de carga para botones con fondo azul."""
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
                    texto,
                    color=ft.Colors.WHITE,
                ),
            ],
        )

    def _contenido_postulando(self):
        """Contenido visual del boton mientras se realiza la postulacion."""
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
                    "Postulando...",
                    color=ft.Colors.WHITE,
                ),
            ],
        )

    def _contenido_aceptando(self):
        """Contenido visual del boton mientras se acepta la solicitud."""
        return ft.Row(
            tight=True,
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ProgressRing(
                    width=16,
                    height=16,
                    stroke_width=2,
                    color=ft.Colors.BLUE_500,
                ),
                ft.Text(
                    "Aceptando...",
                    color=ft.Colors.BLUE_500,
                ),
            ],
        )

    async def cargar(
        self,
        page: ft.Page,
        oferta_id: int
    ):
        """Metodo para cargar la oferta laboral por su id."""
        if self.cargando_oferta:
            return
        self.cargando_oferta = True
        self.oferta_id = oferta_id
        self.conexion = None
        self.ocultar_acciones()
        self.txt_estado.value = "Cargando oferta..."
        self.txt_estado.visible = True
        page.update()
        try:
            datos = await OfertaLaboralService.obtener_oferta_laboral(
                page=page,
                oferta_laboral_id=oferta_id,
            )
            self.mostrar_datos(datos)
            self.txt_estado.visible = False
            if Sesion.rol(page) == "POSTULANTE":
                await self.verificar_estado_postulante(
                    page=page,
                    oferta_id=oferta_id
                )
        except ErrorAutenticacion:
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await page.push_route(
                "/login"
            )
        except ErrorNoEncontrado:
            self.mostrar_mensaje(
                "No se encontró la oferta laboral solicitada"
            )
        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo cargar la oferta. Intente nuevamente"
            )
        finally:
            self.cargando_oferta = False

    def ocultar_acciones(self):
        """Metodo para ocultar las acciones del encabezado."""
        self.btn_postularse.visible = False
        self.btn_aceptar_solicitud.visible = False
        self.btn_conversacion.visible = False
        self.txt_estado.visible = False

    async def verificar_estado_postulante(
        self,
        page: ft.Page,
        oferta_id: int
    ):
        """Metodo para verificar el estado del postulante respecto de la oferta."""
        self.ocultar_acciones()
        conexion = await PostulanteService.verificar_conexion_laboral(
            page=page,
            oferta_id=oferta_id
        )
        if conexion:
            self.conexion = conexion
            estado = conexion.get("estado")
            if estado == "ACEPTADA":
                self.btn_conversacion.visible = True
                return
            if estado == "PENDIENTE":
                self.btn_aceptar_solicitud.visible = True
                return
        postulacion = await PostulanteService.verificar_postulacion(
            page=page,
            oferta_id=oferta_id
        )
        if postulacion:
            estado = postulacion.get("estado")
            if estado == "ACEPTADA":
                self.btn_conversacion.visible = True
                return
            if estado == "PENDIENTE":
                self.txt_estado.value = "Pendiente"
                self.txt_estado.visible = True
                return
        self.btn_postularse.visible = True

    def mostrar_datos(self, datos: dict):
        """Metodo para mostrar los datos de la oferta laboral."""
        self.txt_titulo.value = datos.get(
            "titulo",
            "",
        )
        self.txt_ubicacion.value = datos.get(
            "ubicacion",
            "",
        )
        self.txt_direccion.value = datos.get(
            "direccion",
            "",
        )
        self.txt_descripcion.value = (
            datos.get("descripcion")
            or "Sin descripción"
        )
        self.contenido_jornada.controls = (
            self._campos_jornada(datos)
        )
        self.contenido_salario.controls = (
            self._campos_salario(datos)
        )
        foto = datos.get("foto_empleador")
        if foto:
            self.avatar.foreground_image_src = foto
            self.avatar.content = None
        else:
            self.avatar.foreground_image_src = None
            self.avatar.content = ft.Icon(
                ft.Icons.BUSINESS,
                size=30,
                color=ft.Colors.BLUE_GREY_400,
            )
        requisitos = datos.get("requisitos") or []
        if requisitos:
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
                        requisito,
                        color=ft.Colors.BLUE_900,
                        size=12,
                    ),
                )
                for requisito in requisitos
            ]
        else:
            self.fila_habilidades.controls = [
                ft.Text(
                    "No especificadas",
                    color=ft.Colors.BLACK_45,
                )
            ]
        self._igualar_alturas(datos)

    @staticmethod
    def _chip(texto: str):
        """Chip azul con un valor."""
        return ft.Container(
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
            content=ft.Text(
                texto,
                color=ft.Colors.BLUE_900,
                weight=ft.FontWeight.W_500,
                size=13,
                text_align=ft.TextAlign.CENTER,
            ),
        )

    def _fila_chips(self, textos: list):
        """Varios chips que se acomodan en filas."""
        return ft.Row(
            wrap=True,
            spacing=6,
            run_spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self._chip(str(texto))
                for texto in textos
            ],
        )

    @staticmethod
    def _campo(etiqueta: str, contenido):
        """Etiqueta pequeña con su valor debajo."""
        return ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    etiqueta,
                    size=11,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.BLACK_45,
                ),
                contenido,
            ],
        )

    @staticmethod
    def _formatear_hora(valor):
        """Convierte 08:00:00 en 08:00."""
        return str(valor)[:5] if valor else None

    def _formatear_horario(self, inicio, fin) -> str:
        """Arma el texto del horario laboral."""
        inicio = self._formatear_hora(inicio)
        fin = self._formatear_hora(fin)
        if inicio and fin:
            return f"{inicio} - {fin} hs"
        if inicio:
            return f"Desde {inicio} hs"
        if fin:
            return f"Hasta {fin} hs"
        return "No especificado"

    def _campos_jornada(self, datos: dict) -> list:
        """Campos del frame JORNADA."""
        jornada = self.JORNADAS.get(
            datos.get("jornada"),
            "No especificada",
        )
        turno = self.TURNOS.get(
            datos.get("turno"),
            "No especificado",
        )
        horario = self._formatear_horario(
            datos.get("hora_inicio"),
            datos.get("hora_fin"),
        )
        dias = datos.get("dias_laborales") or []
        return [
            self._campo(
                "Jornada",
                self._chip(jornada),
            ),
            self._campo(
                "Turno",
                self._chip(turno),
            ),
            self._campo(
                "Horario",
                self._chip(horario),
            ),
            self._campo(
                "Días laborales",
                (
                    self._fila_chips(dias)
                    if dias
                    else self._chip("No especificados")
                ),
            ),
        ]

    def _campos_salario(self, datos: dict) -> list:
        """Campos del frame SALARIO."""
        tipo = datos.get("salario_tipo")
        minimo = self.a_numero(
            datos.get("salario_minimo")
        )
        maximo = self.a_numero(
            datos.get("salario_maximo")
        )
        campos = [
            self._campo(
                "Tipo",
                self._chip(
                    self.TIPOS_SALARIO.get(
                        tipo,
                        "No informado",
                    )
                ),
            ),
        ]
        if tipo == "FIJO":
            campos.append(
                self._campo(
                    "Monto",
                    self._chip(
                        self.formatear_monto(minimo)
                    ),
                )
            )
        elif tipo == "RANGO":
            campos.append(
                self._campo(
                    "Mínimo",
                    self._chip(
                        self.formatear_monto(minimo)
                    ),
                )
            )
            campos.append(
                self._campo(
                    "Máximo",
                    self._chip(
                        self.formatear_monto(maximo)
                    ),
                )
            )
        return campos

    def _contar_filas(self, textos: list, espaciado: int) -> int:
        """Simula el wrap de los chips y devuelve la cantidad de filas.
        Ancho aprox. de un chip = 22 + 6.5 px por caracter.
        """
        ancho_util = self.ANCHO_COLUMNA - 30
        filas = 1
        ancho_fila = 0
        for texto in textos:
            ancho_chip = min(
                22 + 6.5 * len(str(texto)),
                ancho_util,
            )
            if ancho_fila == 0:
                ancho_fila = ancho_chip
            elif ancho_fila + espaciado + ancho_chip <= ancho_util:
                ancho_fila += espaciado + ancho_chip
            else:
                filas += 1
                ancho_fila = ancho_chip
        return filas

    def _alto_tarjeta_habilidades(self, requisitos: list):
        """Alto estimado de la tarjeta de habilidades."""
        if not requisitos:
            return 72
        filas = self._contar_filas(requisitos, 8)
        return 57 + 30 * filas + 8 * (filas - 1)

    def _alto_tarjeta_jornada(self, datos: dict):
        """Alto estimado de la tarjeta de jornada.
        Cabecera (padding + titulo + espacio) = 56.
        Cada campo simple = 48 (etiqueta + chip), con 10 px entre campos.
        """
        dias = datos.get("dias_laborales") or []
        if dias:
            filas = self._contar_filas(dias, 6)
            alto_dias = (
                18
                + 30 * filas
                + 6 * (filas - 1)
            )
        else:
            alto_dias = 48
        return (
            56
            + 48 * 3
            + alto_dias
            + 10 * 3
        )

    @staticmethod
    def _alto_tarjeta_salario(datos: dict):
        """Alto estimado de la tarjeta de salario."""
        tipo = datos.get("salario_tipo")
        if tipo == "FIJO":
            campos = 2
        elif tipo == "RANGO":
            campos = 3
        else:
            campos = 1
        return (
            56
            + 48 * campos
            + 10 * (campos - 1)
        )

    def _igualar_alturas(self, datos: dict):
        """Iguala la altura de la tarjeta de descripcion con la columna derecha.
        Columna derecha = jornada + salario + habilidades,
        con 20 px de espaciado entre cada una.
        """
        requisitos = datos.get("requisitos") or []
        alto_columna = (
            self._alto_tarjeta_jornada(datos)
            + 20
            + self._alto_tarjeta_salario(datos)
            + 20
            + self._alto_tarjeta_habilidades(requisitos)
        )
        texto = self.txt_descripcion.value or ""
        lineas = sum(
            max(1, math.ceil(len(parte) / 80))
            for parte in texto.split("\n")
        )
        alto_descripcion = 57 + 20 * lineas
        self.tarjeta_descripcion.height = max(
            alto_columna,
            alto_descripcion,
        )

    def formatear_monto(self, monto) -> str:
        """Metodo para dar formato a un monto de salario."""
        if monto is None:
            return "No informado"
        return f"${monto:,.0f}"

    def a_numero(self, valor):
        """Metodo para convertir un valor de salario a float de forma segura."""
        try:
            return float(valor) if valor is not None else None
        except (TypeError, ValueError):
            return None

    async def postularse(self, e):
        """Metodo para mostrar la confirmacion de postulacion."""
        if Sesion.rol(self.page) != "POSTULANTE":
            return
        if self.cargando_postulacion:
            return
        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    "Postularse",
                    color=ft.Colors.BLACK,
                ),
                content=ft.Text(
                    f"¿Querés postularte a la oferta "
                    f"{self.txt_titulo.value}?",
                    color=ft.Colors.BLACK,
                ),
                actions=[
                    ft.TextButton(
                        "CANCELAR",
                        on_click=lambda e: self.page.pop_dialog(),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_500,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(
                                radius=10,
                            ),
                        ),
                    ),
                    ft.TextButton(
                        "POSTULARME",
                        on_click=self.confirmar_postulacion,
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

    async def confirmar_postulacion(self, e):
        """Metodo para confirmar la postulacion."""
        if self.cargando_postulacion:
            return
        self.cargando_postulacion = True
        boton = e.control
        boton.disabled = True
        boton.content = self._contenido_postulando()
        self.page.update()
        try:
            await PostulanteService.crear_postulacion(
                page=self.page,
                oferta_id=self.oferta_id,
            )
            self.page.pop_dialog()
            self.btn_postularse.visible = False
            self.txt_estado.value = "Pendiente"
            self.txt_estado.visible = True
            self.update()
            self.mostrar_mensaje(
                "Te postulaste correctamente a la oferta"
            )
        except ErrorAutenticacion:
            self.page.pop_dialog()
            self.mostrar_dialogo_sesion_expirada()
            await asyncio.sleep(5)
            await self.page.push_route(
                "/login"
            )
        except ErrorNoEncontrado:
            self.page.pop_dialog()
            self.mostrar_mensaje(
                "No se encontró la oferta laboral"
            )
        except ErrorServidor:
            self.page.pop_dialog()
            self.mostrar_mensaje(
                "No se pudo realizar la postulación. "
                "Intente nuevamente"
            )
        finally:
            self.cargando_postulacion = False
            boton.disabled = False
            boton.content = ft.Text(
                "POSTULARME"
            )
            if boton.page is not None:
                boton.page.update()

    def confirmar_aceptar_solicitud(self, e):
        """Metodo para mostrar la confirmacion de aceptacion de contacto."""
        if not self.conexion:
            return
        if self.cargando_aceptacion:
            return
        nombre_empleador = self.conexion.get(
            "nombre_empleador",
            "el empleador",
        )
        nombre_oferta = self.conexion.get(
            "nombre_oferta",
            self.txt_titulo.value,
        )
        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    "Aceptar solicitud de contacto",
                    color=ft.Colors.BLACK_87,
                ),
                content=ft.Text(
                    f"Estarías aceptando la solicitud de contacto de "
                    f"{nombre_empleador} para la oferta "
                    f"{nombre_oferta}. ¿Estás seguro?",
                    color=ft.Colors.BLACK_87,
                ),
                actions=[
                    ft.TextButton(
                        "CANCELAR",
                        on_click=lambda e: self.page.pop_dialog(),
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLACK_54,
                        ),
                    ),
                    ft.TextButton(
                        "ACEPTAR",
                        on_click=self.aceptar_solicitud,
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_500,
                        ),
                    ),
                ],
            )
        )

    async def aceptar_solicitud(self, e):
        """Metodo para aceptar una solicitud de contacto."""
        if not self.conexion:
            return
        if self.cargando_aceptacion:
            return
        self.cargando_aceptacion = True
        boton = e.control
        boton.disabled = True
        boton.content = self._contenido_aceptando()
        self.page.update()
        try:
            await PostulanteService.actualizar_conexion_laboral(
                page=self.page,
                conexion_laboral_id=self.conexion["id"],
                estado="ACEPTADA",
            )
            self.conexion["estado"] = "ACEPTADA"
            self.page.pop_dialog()
            self.btn_aceptar_solicitud.visible = False
            self.btn_conversacion.visible = True
            self.update()
            self.mostrar_dialogo_conexion_aceptada()
        except ErrorAutenticacion:
            self.page.pop_dialog()
            self.mostrar_dialogo_sesion_expirada()
        except ErrorNoEncontrado:
            self.page.pop_dialog()
            self.mostrar_mensaje(
                "No se encontró la solicitud de contacto"
            )
        except ErrorServidor:
            self.page.pop_dialog()
            self.mostrar_mensaje(
                "No se pudo aceptar la solicitud de contacto"
            )
        finally:
            self.cargando_aceptacion = False

    def mostrar_dialogo_conexion_aceptada(self):
        """Informa que se creó la conexión laboral y cómo continuar."""
        empresa = self.conexion.get(
            "nombre_empleador",
            "la empresa",
        )
        puesto = self.conexion.get(
            "nombre_oferta",
            self.txt_titulo.value or "la oferta publicada",
        )
        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE_OUTLINE,
                            color=ft.Colors.GREEN_600,
                            size=28,
                        ),
                        ft.Text(
                            "¡Conexión laboral creada!",
                            color=ft.Colors.BLUE_GREY_900,
                        ),
                    ],
                    spacing=10,
                ),
                content=ft.Text(
                    f"Ahora tenés una conexión laboral con {empresa} "
                    f"para el puesto de {puesto}.\n\n"
                    "Entrá a tus conversaciones para hablar con la "
                    "empresa sobre la oferta, las tareas y la modalidad "
                    "de trabajo.",
                    color=ft.Colors.BLACK_87,
                ),
                actions=[
                    ft.TextButton(
                        "IR A CONVERSACIONES",
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_600,
                        ),
                        on_click=self.ir_a_conversaciones_desde_dialogo,
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
        )

    async def ir_a_conversaciones_desde_dialogo(self, e):
        """Cierra la confirmación y abre las conversaciones."""
        self.page.pop_dialog()
        await self.page.push_route("/mensajes")

    async def abrir_conversacion(self, e):
        """Metodo para abrir la conversacion laboral."""
        if not self.conexion:
            return
        if self.conexion.get("estado") != "ACEPTADA":
            return
        await self.page.push_route(
            "/mensajes"
        )

    async def volver(self, e):
        """Metodo para volver a la busqueda."""
        if Sesion.rol(self.page) == "ADMINISTRADOR":
            await self.page.push_route(
                "/perfil-personal-administrador"
            )
        else:
            await self.page.push_route(
                "/busqueda"
            )

    def mostrar_mensaje(self, mensaje):
        """Metodo para mostrar los mensajes de excepciones."""
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    mensaje
                )
            )
        )

    def mostrar_dialogo_sesion_expirada(self):
        """Metodo para mostrar el dialogo de sesion expirada."""
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
