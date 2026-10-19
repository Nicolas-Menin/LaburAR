import asyncio
import flet as ft
from frontend.src.services.autenticacion_service import AutenticacionService
from frontend.src.excepciones.api_excepciones import (
    ErrorServidor,
    ErrorAutenticacion,
    ErrorNoEncontrado,
)

# pylint: disable=E1121,E1123,E0401,E1101


class RecuperarContrasenaView(ft.View):

    def __init__(self):
        super().__init__()

        self.route = "/recuperar-contrasena"
        self.padding = 0
        self.spacing = 0
        self.enviando = False

        self.bg_image = ft.Image(
            src="images/LaburAR_bg1.png",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.txt_titulo = ft.Text(
            "RECUPERAR CONTRASEÑA",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
            font_family="Inter-Bold",
            text_align=ft.TextAlign.CENTER,
        )

        self.txt_explicativo = ft.Text(
            "Ingresá tu correo electrónico registrado para "
            "recibir el enlace de recuperación de contraseña.",
            size=13,
            color=ft.Colors.BLACK_54,
            text_align=ft.TextAlign.CENTER,
        )

        self.txt_email = ft.TextField(
            label="Correo electrónico",
            hint_text="ejemplo@correo.com",
            keyboard_type=ft.KeyboardType.EMAIL,
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            text_style=ft.TextStyle(
                color=ft.Colors.BLACK
            ),
            focused_border_color=ft.Colors.BLUE_500,
        )

        self.btn_recuperar = ft.FilledButton(
            content=ft.Row(
                controls=[
                    ft.Text("RECUPERAR CONTRASEÑA"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(
                    left=20,
                    top=15,
                    right=20,
                    bottom=15,
                ),
            ),
            width=360,
            on_click=self.enviar_recuperacion,
        )

        self.tarjeta_central = ft.Container(
            width=420,
            height=400,
            padding=30,
            bgcolor=ft.Colors.with_opacity(
                0.95,
                ft.Colors.WHITE,
            ),
            border_radius=15,
            border=ft.Border.all(
                1,
                ft.Colors.BLUE_GREY_100,
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.with_opacity(
                    0.12,
                    ft.Colors.BLACK,
                ),
                offset=ft.Offset(0, 8),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=18,
                controls=[
                    ft.Icon(
                        ft.Icons.LOCK_RESET_OUTLINED,
                        size=48,
                        color=ft.Colors.BLUE_500,
                    ),
                    self.txt_titulo,
                    self.txt_explicativo,
                    self.txt_email,
                    ft.Container(height=5),
                    self.btn_recuperar,
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
                        content=ft.IconButton(
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
                    ),
                ],
            )
        ]

    async def enviar_recuperacion(self, e):
        """Envía el correo y evita solicitudes duplicadas."""

        if self.enviando:
            return

        email = (self.txt_email.value or "").strip()

        if not email:
            self.mostrar_mensaje(
                "Por favor, ingresá tu correo electrónico"
            )
            return

        self.enviando = True
        self.btn_recuperar.disabled = True
        self.btn_recuperar.content = ft.Row(
            controls=[
                ft.ProgressRing(
                    width=18,
                    height=18,
                    stroke_width=2,
                    color=ft.Colors.WHITE,
                ),
                ft.Text("ENVIANDO CORREO..."),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        self.page.update()

        try:
            await AutenticacionService.recuperar_contrasena(
                page=self.page,
                email=email,
            )

            self.mostrar_dialogo_recuperacion_exitosa()

        except ErrorNoEncontrado:
            self.mostrar_mensaje(
                "El correo ingresado no se encuentra registrado"
            )

        except ErrorAutenticacion:
            self.mostrar_mensaje(
                "No se pudo procesar la solicitud"
            )

        except ErrorServidor:
            self.mostrar_mensaje(
                "Error en el servidor. Intente más tarde"
            )

        finally:
            self.enviando = False
            self.btn_recuperar.disabled = False
            self.btn_recuperar.content = ft.Row(
                controls=[
                    ft.Text("RECUPERAR CONTRASEÑA"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
            self.page.update()

    def mostrar_dialogo_recuperacion_exitosa(self):
        """Muestra la confirmación del envío del correo."""

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
                            "¡Correo enviado!",
                            color=ft.Colors.BLUE_GREY_900,
                        ),
                    ],
                    spacing=10,
                ),
                content=ft.Text(
                    "Se envió un correo electrónico con las "
                    "instrucciones para recuperar tu contraseña.",
                    color=ft.Colors.BLACK_87,
                ),
                actions=[
                    ft.TextButton(
                        "ACEPTAR",
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_500,
                            color=ft.Colors.WHITE,
                            shape=ft.RoundedRectangleBorder(
                                radius=10
                            ),
                        ),
                        on_click=self.ir_a_login_desde_dialogo,
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
        )

    async def ir_a_login_desde_dialogo(self, e):
        """Cierra el diálogo y vuelve al inicio de sesión."""

        self.page.pop_dialog()
        await self.page.push_route("/login")

    async def volver(self, e):
        """Vuelve a la pantalla de inicio de sesión."""

        await self.page.push_route("/login")

    def mostrar_mensaje(self, mensaje: str):
        """Muestra mensajes de error y validación."""

        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje)
            )
        )
