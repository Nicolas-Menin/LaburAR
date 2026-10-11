import asyncio

import flet as ft

from frontend.src.services.autenticacion_service import AutenticacionService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
    ErrorNoEncontrado,
    ErrorValidacion,
)

# pylint: disable=E1121,E1123,E0401,E1101


class RestablecerContrasenaView(ft.View):

    LARGO_MINIMO_CONTRASENA = 8

    def __init__(self, token: str = None):
        super().__init__()

        self.route = "/restablecer-contraseña"
        self.padding = 0
        self.spacing = 0
        self.token = token

        self.cargando = False

        self.bg_image = ft.Image(
            src="images/LaburAR_bg1.png",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.txt_titulo = ft.Text(
            "RESTABLECER CONTRASEÑA",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
            font_family="Inter-Bold",
            text_align=ft.TextAlign.CENTER,
        )

        self.txt_explicativo = ft.Text(
            "Ingresá y confirmá tu nueva contraseña "
            "para actualizar el acceso a tu cuenta.",
            size=13,
            color=ft.Colors.BLACK_54,
            text_align=ft.TextAlign.CENTER,
        )

        self.txt_nueva_contrasena = ft.TextField(
            label="Nueva contraseña",
            hint_text="Ingresá tu nueva clave",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK_OUTLINED,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            focused_border_color=ft.Colors.BLUE_500,
        )

        self.txt_confirmar_contrasena = ft.TextField(
            label="Confirmar nueva contraseña",
            hint_text="Repetí tu nueva clave",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK_RESET_OUTLINED,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            focused_border_color=ft.Colors.BLUE_500,
        )

        self.btn_restablecer = ft.FilledButton(
            "RESTABLECER CONTRASEÑA",
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(left=20, top=15, right=20, bottom=15),
            ),
            width=360,
            on_click=self.restablecer_contrasena,
        )

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
            tooltip="Volver al Login",
            on_click=self.volver,
        )

        self.tarjeta_central = ft.Container(
            width=420,
            height=500,
            padding=30,
            bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.WHITE),
            border_radius=15,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=18,
                controls=[
                    ft.Icon(
                        ft.Icons.PASSWORD_OUTLINED,
                        size=48,
                        color=ft.Colors.BLUE_500,
                    ),
                    self.txt_titulo,
                    self.txt_explicativo,
                    self.txt_nueva_contrasena,
                    self.txt_confirmar_contrasena,
                    ft.Container(height=5),
                    self.btn_restablecer,
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
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                        content=self.tarjeta_central,
                    ),
                    ft.Container(
                        top=20,
                        left=20,
                        content=self.btn_volver,
                    ),
                ],
            )
        ]

    def _mostrar_cargando(self, cargando: bool):
        """Muestra la espera en el botón y bloquea el formulario."""

        self.cargando = cargando

        self.txt_nueva_contrasena.disabled = cargando
        self.txt_confirmar_contrasena.disabled = cargando
        self.btn_volver.disabled = cargando
        self.btn_restablecer.disabled = cargando

        if cargando:

            self.btn_restablecer.content = ft.Row(
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.ProgressRing(
                        width=18,
                        height=18,
                        stroke_width=2,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        "RESTABLECIENDO...",
                        color=ft.Colors.WHITE,
                    ),
                ],
            )

        else:

            self.btn_restablecer.content = ft.Text(
                "RESTABLECER CONTRASEÑA",
                color=ft.Colors.WHITE,
            )

        try:
            self.update()
        except RuntimeError:
            pass

    def _vaciar_campos(self):
        """Limpia los campos para que no queden contraseñas en la vista."""

        self.txt_nueva_contrasena.value = ""
        self.txt_confirmar_contrasena.value = ""

    async def restablecer_contrasena(self, e):
        """Método para procesar el cambio de contraseña."""

        if self.cargando:
            return

        nueva_clave = self.txt_nueva_contrasena.value or ""
        confirmar_clave = self.txt_confirmar_contrasena.value or ""

        if not nueva_clave.strip() or not confirmar_clave.strip():
            self.mostrar_mensaje("Por favor, completá todos los campos")
            return

        if len(nueva_clave) < self.LARGO_MINIMO_CONTRASENA:
            self.mostrar_mensaje(
                "La contraseña debe tener al menos "
                f"{self.LARGO_MINIMO_CONTRASENA} caracteres"
            )
            return

        if nueva_clave != confirmar_clave:
            self.mostrar_mensaje("Las contraseñas no coinciden")
            return

        if not self.token:
            self.mostrar_mensaje(
                "El enlace de recuperación no es válido"
            )
            return

        self._mostrar_cargando(True)

        try:
            await AutenticacionService.restablecer_contrasena(
                page=self.page,
                token=self.token,
                nueva_contrasena=nueva_clave,
            )

            self._vaciar_campos()

            self.mostrar_mensaje("¡Contraseña restablecida con éxito!")
            await asyncio.sleep(1.5)
            await self.page.push_route("/login")

        except ErrorAutenticacion:
            self.mostrar_mensaje("El enlace de recuperación venció o es inválido")

        except ErrorValidacion:
            self.mostrar_mensaje("La contraseña ingresada no es válida")

        except ErrorServidor:
            self.mostrar_mensaje("Error en el servidor. Intente más tarde")

        except ErrorNoEncontrado:
            self.mostrar_mensaje("Ocurrió un error inesperado")

        finally:
            self._mostrar_cargando(False)

    async def volver(self, e):
        """Método para volver a la pantalla de inicio de sesión."""

        if self.cargando:
            return

        await self.page.push_route("/login")

    def mostrar_mensaje(self, mensaje: str):
        """Método auxiliar para mostrar notificaciones SnackBar."""
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje)
            )
        )