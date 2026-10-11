import flet as ft
# pylint: disable=E1121,E1123,E0401, E1101

class SeleccionUsuariorView(ft.View):

    def __init__(self):
        super().__init__()

        self.route = "/seleccionar-usuario"

        self.padding = 0
        self.spacing = 0

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
                        content=ft.Container(
                            width=400,
                            height=380,
                            padding=40,
                            border_radius=20,
                            bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.WHITE),
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=20,
                                color=ft.Colors.with_opacity(0.10, ft.Colors.BLACK),
                                offset=ft.Offset(0, 10),
                            ),
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                                controls=[
                                    ft.Text(
                                        "Elige tipo de usuario",
                                        size=28,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLACK_87,
                                        font_family="Inter-Bold"
                                    ),
                                    ft.Text(
                                        "¿Cómo deseas usar LaburAR?",
                                        size=16,
                                        color=ft.Colors.BLACK_54,
                                        font_family="Inter-Regular"
                                    ),

                                    ft.Container(height=5),

                                    ft.Button(
                                        content=ft.Text("SOY POSTULANTE", size=16, font_family="Inter-Medium"),
                                        width=320,
                                        height=50,
                                        style=ft.ButtonStyle(
                                            color=ft.Colors.WHITE,
                                            bgcolor=ft.Colors.BLUE_500,
                                            shape=ft.RoundedRectangleBorder(radius=15),
                                        ),
                                        on_click=self.ir_registro_postulante_view
                                    ),

                                    ft.Button(
                                        content=ft.Text("SOY EMPLEADOR", size=16, font_family="Inter-Medium"),
                                        width=320,
                                        height=50,
                                        style=ft.ButtonStyle(
                                            color=ft.Colors.BLUE_500,
                                            bgcolor=ft.Colors.WHITE,
                                            side=ft.BorderSide(2, ft.Colors.BLUE_500),
                                            shape=ft.RoundedRectangleBorder(radius=15),
                                        ),
                                        on_click=self.ir_registro_empleador_view
                                    )
                                ]
                            )
                        )
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
                                shadow_color=ft.Colors.BLACK
                            ),
                            tooltip="Volver",
                            on_click=self.ir_iniciar_sesion_view
                        )
                    )
                ]
            )
        ]

    async def ir_registro_postulante_view(self, e):
        await self.page.push_route("/registrar-postulante")

    async def ir_registro_empleador_view(self, e):
        await self.page.push_route("/registrar-empleador")

    async def ir_iniciar_sesion_view(self,e):
        await self.page.push_route("/login")