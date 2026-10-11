import flet as ft

from frontend.src.services.autenticacion_service import AutenticacionService
from frontend.src.excepciones.api_excepciones import (
    ErrorValidacion,
    ErrorServidor
)

# pylint: disable=E1121,E1123,E0401, E1101


class RegistrarPostulanteView(ft.View):

    LARGO_MINIMO_CONTRASENA = 8

    def __init__(self):
        super().__init__()

        self.route = "/registrar-postulante"
        self.padding = 0
        self.spacing = 0

        self.cargando = False

        self.nombre = ft.TextField(
            label="Nombre",
            width=155,
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
            on_change=lambda e: self._limpiar_error("nombre"),
        )

        self.apellido = ft.TextField(
            label="Apellido",
            width=155,
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
            on_change=lambda e: self._limpiar_error("apellido"),
        )

        self.email = ft.TextField(
            label="Email",
            width=320,
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
            on_change=lambda e: self._limpiar_error("email"),
        )

        self.ubicacion = ft.Dropdown(
            label="Ubicación",
            width=320,
            options=[
                ft.DropdownOption(
                    text="Punta Alta",
                    style=ft.ButtonStyle(
                        color={
                            ft.ControlState.DEFAULT: ft.Colors.BLACK,
                        }
                    )
                )
            ],
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
        )

        self.ubicacion.on_change = (
            lambda e: self._limpiar_error("ubicacion")
        )
        self.ubicacion.on_select = (
            lambda e: self._limpiar_error("ubicacion")
        )

        self.contrasena = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=320,
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
            on_change=lambda e: self._limpiar_error("contrasena"),
        )

        self.confirmar_contrasena = ft.TextField(
            label="Confirmar contraseña",
            password=True,
            can_reveal_password=True,
            width=320,
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
            on_change=lambda e: self._limpiar_error("confirmar"),
        )

        self.error_nombre = self._crear_texto_error(155)
        self.error_apellido = self._crear_texto_error(155)
        self.error_email = self._crear_texto_error(320)
        self.error_ubicacion = self._crear_texto_error(320)
        self.error_contrasena = self._crear_texto_error(320)
        self.error_confirmar = self._crear_texto_error(320)

        self._campos = {
            "nombre": (self.nombre, self.error_nombre),
            "apellido": (self.apellido, self.error_apellido),
            "email": (self.email, self.error_email),
            "ubicacion": (self.ubicacion, self.error_ubicacion),
            "contrasena": (self.contrasena, self.error_contrasena),
            "confirmar": (
                self.confirmar_contrasena,
                self.error_confirmar,
            ),
        }

        self.boton_registrar = ft.Button(
            content=ft.Text(
                "REGISTRAR CUENTA",
                size=16,
                font_family="Inter-Medium"
            ),
            width=320,
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(
                    radius=15
                ),
            ),
            on_click=self.registrar_postulante
        )

        self.boton_volver = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_size=24,
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_500,
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                elevation=4,
                shadow_color=ft.Colors.BLACK
            ),
            tooltip="Volver",
            on_click=self.ir_seleccionar_usuario_view
        )

        self.bg_image = ft.Image(
            src="images/LaburAR_bg1.png",
            fit=ft.BoxFit.COVER,
            expand=True
        )

        self.controls = [
            ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        content=self.bg_image
                    ),
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=(
                                ft.CrossAxisAlignment.CENTER
                            ),
                            controls=[
                                ft.Container(
                                    width=400,
                                    padding=40,
                                    border_radius=20,
                                    bgcolor=ft.Colors.with_opacity(
                                        0.95,
                                        ft.Colors.WHITE
                                    ),
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=20,
                                        color=ft.Colors.with_opacity(
                                            0.10,
                                            ft.Colors.BLACK
                                        ),
                                        offset=ft.Offset(0, 10),
                                    ),
                                    content=ft.Column(
                                        tight=True,
                                        horizontal_alignment=(
                                            ft.CrossAxisAlignment.CENTER
                                        ),
                                        spacing=15,
                                        controls=[
                                            ft.Text(
                                                "Perfil Postulante",
                                                size=28,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.BLACK_87,
                                                font_family="Inter-Bold"
                                            ),
                                            ft.Container(height=10),
                                            ft.Row(
                                                alignment=(
                                                    ft.MainAxisAlignment.CENTER
                                                ),
                                                vertical_alignment=(
                                                    ft.CrossAxisAlignment.START
                                                ),
                                                spacing=10,
                                                controls=[
                                                    ft.Column(
                                                        tight=True,
                                                        spacing=4,
                                                        controls=[
                                                            self.nombre,
                                                            self.error_nombre,
                                                        ],
                                                    ),
                                                    ft.Column(
                                                        tight=True,
                                                        spacing=4,
                                                        controls=[
                                                            self.apellido,
                                                            self.error_apellido,
                                                        ],
                                                    ),
                                                ]
                                            ),
                                            ft.Column(
                                                tight=True,
                                                spacing=4,
                                                controls=[
                                                    self.email,
                                                    self.error_email,
                                                ],
                                            ),
                                            ft.Column(
                                                tight=True,
                                                spacing=4,
                                                controls=[
                                                    self.ubicacion,
                                                    self.error_ubicacion,
                                                ],
                                            ),
                                            ft.Column(
                                                tight=True,
                                                spacing=4,
                                                controls=[
                                                    self.contrasena,
                                                    self.error_contrasena,
                                                ],
                                            ),
                                            ft.Column(
                                                tight=True,
                                                spacing=4,
                                                controls=[
                                                    self.confirmar_contrasena,
                                                    self.error_confirmar,
                                                ],
                                            ),
                                            ft.Container(height=5),
                                            self.boton_registrar
                                        ]
                                    )
                                )
                            ],
                        ),
                    ),
                    ft.Container(
                        top=20,
                        left=20,
                        content=self.boton_volver
                    )
                ]
            )
        ]

    @staticmethod
    def _crear_texto_error(ancho: int):
        """Texto rojo que aparece debajo de un campo con error."""

        return ft.Container(
            width=ancho,
            visible=False,
            padding=ft.Padding(
                left=12,
                top=0,
                right=0,
                bottom=0,
            ),
            content=ft.Text(
                "",
                size=12,
                color=ft.Colors.RED,
            ),
        )

    @staticmethod
    def _marcar_error(campo, contenedor_error, mensaje):
        """Muestra u oculta el mensaje de error de un campo."""

        campo.border_color = (
            ft.Colors.RED
            if mensaje
            else ft.Colors.BLUE_GREY_200
        )

        contenedor_error.content.value = mensaje or ""
        contenedor_error.visible = bool(mensaje)

    def _actualizar_campos(self):
        """Redibuja los campos y sus mensajes de error."""

        for campo, contenedor_error in self._campos.values():
            for control in (campo, contenedor_error):
                try:
                    control.update()
                except RuntimeError:
                    pass

    def _limpiar_error(self, clave: str):
        """Quita el error de un campo apenas el usuario lo modifica."""

        campo, contenedor_error = self._campos[clave]

        if contenedor_error.visible:
            self._marcar_error(
                campo,
                contenedor_error,
                None,
            )

            for control in (campo, contenedor_error):
                try:
                    control.update()
                except RuntimeError:
                    pass

    def _validar_campos(self):
        """Valida todos los campos y muestra el mensaje de cada error."""

        nombre = (self.nombre.value or "").strip()
        apellido = (self.apellido.value or "").strip()
        email = (self.email.value or "").strip()
        contrasena = self.contrasena.value or ""
        confirmar = self.confirmar_contrasena.value or ""

        errores = {}

        errores["nombre"] = (
            None if nombre
            else "Ingresá tu nombre"
        )

        errores["apellido"] = (
            None if apellido
            else "Ingresá tu apellido"
        )

        if not email:
            errores["email"] = "Ingresá tu email"
        elif "@" not in email:
            errores["email"] = "El email debe contener @"
        else:
            errores["email"] = None

        errores["ubicacion"] = (
            None if self.ubicacion.value
            else "Seleccioná tu ubicación"
        )

        if not contrasena.strip():
            errores["contrasena"] = "Ingresá tu contraseña"
        elif len(contrasena) < self.LARGO_MINIMO_CONTRASENA:
            errores["contrasena"] = (
                "La contraseña debe tener al menos "
                f"{self.LARGO_MINIMO_CONTRASENA} caracteres"
            )
        else:
            errores["contrasena"] = None

        if not confirmar:
            errores["confirmar"] = "Confirmá tu contraseña"
        elif confirmar != contrasena:
            errores["confirmar"] = "Las contraseñas no coinciden"
        else:
            errores["confirmar"] = None

        for clave, mensaje in errores.items():
            campo, contenedor_error = self._campos[clave]

            self._marcar_error(
                campo,
                contenedor_error,
                mensaje,
            )

        self._actualizar_campos()

        return not any(errores.values())

    def _refrescar(self):
        """Actualiza la vista si todavía está en pantalla."""

        try:
            self.update()
        except RuntimeError:
            pass

    def _bloquear(self, bloquear: bool):
        """Habilita o deshabilita todo mientras hay una acción en curso."""

        self.cargando = bloquear

        for campo, _ in self._campos.values():
            campo.disabled = bloquear

        self.boton_registrar.disabled = bloquear
        self.boton_volver.disabled = bloquear

    def _mostrar_cargando(self, cargando):
        """Cambia el botón al estado de carga."""

        self._bloquear(cargando)

        if cargando:
            self.boton_registrar.content = ft.Row(
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.ProgressRing(
                        width=20,
                        height=20,
                        stroke_width=2,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        "REGISTRANDO...",
                        color=ft.Colors.WHITE,
                        size=16,
                        font_family="Inter-Medium"
                    ),
                ]
            )
        else:
            self.boton_registrar.content = ft.Text(
                "REGISTRAR CUENTA",
                size=16,
                font_family="Inter-Medium"
            )

        self._refrescar()

    async def registrar_postulante(self, e):
        """Método para registrar postulante."""

        if self.cargando:
            return

        if not self._validar_campos():
            self._refrescar()
            return

        self._mostrar_cargando(True)

        try:
            await AutenticacionService.registrar_postulante(
                page=self.page,
                email=self.email.value,
                contrasena=self.contrasena.value,
                nombre=self.nombre.value,
                apellido=self.apellido.value,
                ubicacion=self.ubicacion.value
            )

            self._vaciar_campos()

            await self.page.push_route("/login")

        except ErrorValidacion:
            self.mostrar_mensaje(
                "Los datos ingresados no son válidos"
            )

        except ErrorServidor:
            self.mostrar_mensaje(
                "No se pudo registrar la cuenta. Intente nuevamente"
            )

        finally:
            self._mostrar_cargando(False)

    async def ir_seleccionar_usuario_view(self, e):
        if self.cargando:
            return

        self._vaciar_campos()
        await self.page.push_route("/seleccionar-usuario")

    def mostrar_mensaje(self, mensaje):
        """Método para mostrar los mensajes de excepciones."""

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje)
            )
        )

    def _vaciar_campos(self):
        """Método para vaciar los campos y quitar los errores."""

        self.nombre.value = ""
        self.apellido.value = ""
        self.email.value = ""
        self.ubicacion.value = None
        self.contrasena.value = ""
        self.confirmar_contrasena.value = ""

        for campo, contenedor_error in self._campos.values():
            self._marcar_error(
                campo,
                contenedor_error,
                None,
            )