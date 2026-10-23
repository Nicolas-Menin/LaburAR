import flet as ft

from frontend.src.services.autenticacion_service import AutenticacionService
from frontend.src.excepciones.api_excepciones import (
    ErrorAutenticacion,
    ErrorServidor,
    ErrorValidacion,
)
from frontend.src.session.sesion import Sesion

# pylint: disable=E1121,E1123,E0401,E1101


class IniciarSesionView(ft.View):
    LARGO_MINIMO_CONTRASENA = 8


    NOMBRE_APP = "LaburAR"
    EMAIL_CONTACTO = "laburarapp@gmail.com"
    FECHA_ACTUALIZACION = "Octubre de 2026"

    def __init__(self):
        super().__init__()

        self.route = "/login"
        self.padding = 0
        self.spacing = 0
        self.expand = True
        self.cargando = False

        self.email = ft.TextField(
            label="Email",
            width=320,
            border=ft.InputBorder.OUTLINE,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK_87,
            border_color=ft.Colors.BLUE_GREY_200,
            focused_border_color=ft.Colors.BLUE_500,
            on_change=self._limpiar_error_email,
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
            on_change=self._limpiar_error_contrasena,
        )

        self.error_email = self._crear_texto_error()
        self.error_contrasena = self._crear_texto_error()

        self.boton_iniciar_sesion = ft.Button(
            "INICIAR SESIÓN",
            width=320,
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(radius=15),
            ),
            on_click=self.iniciar_sesion,
        )

        self.boton_recuperar = ft.TextButton(
            "¿Olvidaste tu contraseña?",
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_600,
            ),
            on_click=self.ir_recuperar_contrasena,
        )

        self.boton_registrarse = ft.OutlinedButton(
            "REGISTRARSE",
            width=320,
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_500,
                side=ft.BorderSide(
                    2,
                    ft.Colors.BLUE_500,
                ),
                shape=ft.RoundedRectangleBorder(radius=15),
            ),
            on_click=self.seleccionar_usuario_view,
        )

        self.boton_terminos = ft.TextButton(
            "Términos y condiciones",
            icon=ft.Icons.DESCRIPTION_OUTLINED,
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_900,
                bgcolor=ft.Colors.with_opacity(
                    0.85,
                    ft.Colors.WHITE,
                ),
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(
                    left=14,
                    top=10,
                    right=14,
                    bottom=10,
                ),
            ),
            on_click=self.abrir_terminos,
        )

        self.bg_image = ft.Image(
            src="images/LaburAR_bg1.png",
            fit=ft.BoxFit.COVER,
            expand=True,
        )

        self.logo = ft.Image(
            src="images/LaburAR_logo.png",
            width=320,
            height=140,
            fit=ft.BoxFit.CONTAIN,
        )

        self.tarjeta_login = ft.Container(
            width=420,
            padding=40,
            border_radius=20,
            bgcolor=ft.Colors.with_opacity(
                0.95,
                ft.Colors.WHITE,
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
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text(
                        "Iniciar Sesión",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK_87,
                        font_family="Inter-Bold",
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
                            self.contrasena,
                            self.error_contrasena,
                        ],
                    ),
                    ft.Container(
                        alignment=ft.Alignment.CENTER,
                        width=320,
                        content=self.boton_recuperar,
                    ),
                    self.boton_iniciar_sesion,
                    self.boton_registrarse,
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
                        left=0,
                        top=0,
                        right=0,
                        height=130,
                        alignment=ft.Alignment.CENTER,
                        padding=ft.Padding(
                            left=20,
                            top=10,
                            right=20,
                            bottom=10,
                        ),
                        content=self.logo,
                    ),
                    ft.Container(
                        left=0,
                        top=0,
                        right=0,
                        bottom=0,
                        alignment=ft.Alignment.CENTER,
                        content=self.tarjeta_login,
                    ),
                    ft.Container(
                        left=20,
                        bottom=20,
                        content=self.boton_terminos,
                    ),
                ],
            )
        ]

    @staticmethod
    def _crear_texto_error():
        """Texto rojo que aparece debajo de un campo con error."""

        return ft.Container(
            width=320,
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

        for control in (
            self.email,
            self.error_email,
            self.contrasena,
            self.error_contrasena,
        ):
            try:
                control.update()
            except RuntimeError:
                pass

    def _limpiar_error_email(self, e):
        """Quita el error del email apenas el usuario escribe."""

        if self.error_email.visible:
            self._marcar_error(
                self.email,
                self.error_email,
                None,
            )
            self._actualizar_campos()

    def _limpiar_error_contrasena(self, e):
        """Quita el error de la contraseña apenas el usuario escribe."""

        if self.error_contrasena.visible:
            self._marcar_error(
                self.contrasena,
                self.error_contrasena,
                None,
            )
            self._actualizar_campos()

    def _validar_campos(self):
        """Valida email y contraseña."""

        email = (self.email.value or "").strip()
        contrasena = self.contrasena.value or ""

        if not email:
            error_email = "Ingresá tu email"
        elif "@" not in email:
            error_email = "El email debe contener @"
        else:
            error_email = None

        if not contrasena.strip():
            error_contrasena = "Ingresá tu contraseña"
        elif len(contrasena) < self.LARGO_MINIMO_CONTRASENA:
            error_contrasena = (
                "La contraseña debe tener al menos "
                f"{self.LARGO_MINIMO_CONTRASENA} caracteres"
            )
        else:
            error_contrasena = None

        self._marcar_error(
            self.email,
            self.error_email,
            error_email,
        )

        self._marcar_error(
            self.contrasena,
            self.error_contrasena,
            error_contrasena,
        )

        self._actualizar_campos()

        return not error_email and not error_contrasena

    def _refrescar(self):
        """Actualiza la vista si todavía está en pantalla."""

        try:
            self.update()
        except RuntimeError:
            pass

    def _bloquear(self, bloquear: bool):
        """Habilita o deshabilita todo mientras hay una acción en curso."""

        self.cargando = bloquear
        self.email.disabled = bloquear
        self.contrasena.disabled = bloquear
        self.boton_iniciar_sesion.disabled = bloquear
        self.boton_recuperar.disabled = bloquear
        self.boton_registrarse.disabled = bloquear
        self.boton_terminos.disabled = bloquear

    @staticmethod
    def _contenido_cargando(
        texto: str,
        color,
        tamano: int = 16,
    ):
        """Spinner con texto para mostrar dentro de un botón."""

        return ft.Row(
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.ProgressRing(
                    width=tamano,
                    height=tamano,
                    stroke_width=2,
                    color=color,
                ),
                ft.Text(
                    texto,
                    color=color,
                ),
            ],
        )

    def _mostrar_cargando(self, cargando):
        """Cambia el botón de inicio de sesión al estado de carga."""

        self._bloquear(cargando)

        if cargando:
            self.boton_iniciar_sesion.content = (
                self._contenido_cargando(
                    "INICIANDO SESIÓN...",
                    ft.Colors.WHITE,
                    tamano=20,
                )
            )
        else:
            self.boton_iniciar_sesion.content = ft.Text(
                "INICIAR SESIÓN",
                color=ft.Colors.WHITE,
            )

        self._refrescar()

    async def _navegar(
        self,
        ruta: str,
        boton,
        texto: str,
        color,
    ):
        """Navega a otra vista mostrando espera en el botón tocado."""

        if self.cargando:
            return

        self._bloquear(True)

        boton.content = self._contenido_cargando(
            "CARGANDO...",
            color,
        )

        self._refrescar()

        try:
            await self.page.push_route(ruta)
        finally:
            self._bloquear(False)

            boton.content = ft.Text(
                texto,
                color=color,
            )

            self._refrescar()


    @staticmethod
    def _seccion_terminos(titulo: str, parrafos: list):
        """Arma una sección (título y párrafos) de los términos."""

        controles = [
            ft.Text(
                titulo,
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK_87,
            ),
        ]

        for parrafo in parrafos:
            controles.append(
                ft.Text(
                    parrafo,
                    size=13,
                    color=ft.Colors.BLACK_54,
                )
            )

        return ft.Column(
            spacing=6,
            controls=controles,
        )

    def abrir_terminos(self, e):
        """Muestra los términos y condiciones de uso."""

        if self.cargando:
            return

        app = self.NOMBRE_APP

        secciones = [
            self._seccion_terminos(
                "1. Aceptación",
                [
                    f"Al registrarte y usar {app} aceptás estos "
                    "términos y condiciones. Si no estás de acuerdo, "
                    "te pedimos que no uses la aplicación.",
                ],
            ),
            self._seccion_terminos(
                "2. Objeto del servicio",
                [
                    f"{app} es una plataforma que conecta a "
                    "postulantes con empleadores: permite publicar "
                    "ofertas laborales, postularse, contactarse y "
                    "conversar.",
                    f"{app} no forma parte de la relación laboral que "
                    "puedan acordar los usuarios ni garantiza empleo "
                    "o contratación.",
                ],
            ),
            self._seccion_terminos(
                "3. Registro y cuenta",
                [
                    "Los datos que ingreses deben ser verdaderos y "
                    "estar actualizados.",
                    "Sos responsable de mantener la confidencialidad "
                    "de tu contraseña (mínimo "
                    f"{self.LARGO_MINIMO_CONTRASENA} caracteres) y de "
                    "toda la actividad realizada desde tu cuenta.",
                ],
            ),
            self._seccion_terminos(
                "4. Conducta y contenido",
                [
                    "Está prohibido publicar información falsa, ofertas "
                    "engañosas o discriminatorias, acosar a otros "
                    "usuarios, suplantar identidades o enviar mensajes "
                    "no deseados.",
                    "Cualquier usuario puede reportar conductas "
                    "indebidas. Los administradores revisan los "
                    "reportes y pueden desactivar o banear las cuentas "
                    "que incumplan estos términos.",
                ],
            ),
            self._seccion_terminos(
                "5. Protección de datos personales "
                "(Ley N.º 25.326)",
                [
                    "El tratamiento de los datos personales se rige "
                    "por la Ley N.º 25.326 de Protección de los Datos "
                    "Personales (Habeas Data) y su decreto "
                    "reglamentario N.º 1558/2001.",
                    "Datos que se recopilan: email, nombre y apellido, "
                    "ubicación, foto de perfil, CV, estudios, "
                    "experiencias laborales, habilidades, "
                    "disponibilidad y mensajes. En el caso de los "
                    "empleadores: nombre del negocio, dirección, "
                    "rubro y descripción.",
                    "Finalidad: hacer posible el funcionamiento de la "
                    "plataforma (perfiles, búsquedas, postulaciones, "
                    "contacto, mensajería y moderación). Los datos no "
                    "se usan para fines incompatibles con esa "
                    "finalidad.",
                    "Consentimiento: al registrarte prestás tu "
                    "consentimiento libre, expreso e informado para el "
                    "tratamiento de tus datos con esa finalidad.",
                    "Cesión: los datos no se ceden a terceros, salvo "
                    "que lo autorices o que una ley lo exija.",
                    "Seguridad y confidencialidad: se aplican medidas "
                    "técnicas y organizativas para proteger los datos, "
                    "y quienes los tratan están obligados a guardar "
                    "confidencialidad.",
                    "La Agencia de Acceso a la Información Pública "
                    "(AAIP), como órgano de control de la Ley N.º "
                    "25.326, atiende las denuncias y los reclamos por "
                    "incumplimientos de las normas de protección de "
                    "datos personales.",
                ],
            ),
            self._seccion_terminos(
                "6. Visibilidad de la información",
                [
                    "Tu perfil y tus publicaciones son visibles para "
                    "los demás usuarios según su rol (por ejemplo, los "
                    "empleadores pueden ver los perfiles de los "
                    "postulantes). Los mensajes solo son visibles para "
                    "los participantes de la conversación.",
                ],
            ),
            self._seccion_terminos(
                "7. Limitación de responsabilidad",
                [
                    f"{app} no verifica la veracidad de los perfiles ni "
                    "de las ofertas. Los acuerdos entre usuarios son "
                    "de su exclusiva responsabilidad.",
                ],
            ),
            self._seccion_terminos(
                "8. Modificaciones",
                [
                    "Estos términos pueden actualizarse. La versión "
                    "vigente es la que se muestra en la aplicación.",
                ],
            ),
            self._seccion_terminos(
                "9. Contacto",
                [
                    "Para ejercer tus derechos o hacer consultas "
                    f"escribinos a {self.EMAIL_CONTACTO}.",
                ],
            ),
            ft.Text(
                f"Última actualización: {self.FECHA_ACTUALIZACION}",
                size=11,
                color=ft.Colors.BLACK_45,
                italic=True,
            ),
        ]

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                bgcolor=ft.Colors.WHITE,
                title=ft.Text(
                    "Términos y condiciones",
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                ),
                content=ft.Container(
                    width=640,
                    height=480,
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Column(
                        expand=True,
                        spacing=16,
                        scroll=ft.ScrollMode.AUTO,
                        controls=secciones,
                    ),
                ),
                actions=[
                    ft.TextButton(
                        "CERRAR",
                        on_click=lambda ev: self.page.pop_dialog(),
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

    async def seleccionar_usuario_view(self, e):
        await self._navegar(
            "/seleccionar-usuario",
            self.boton_registrarse,
            "REGISTRARSE",
            ft.Colors.BLUE_500,
        )

    async def iniciar_sesion(self, e):
        """Método para iniciar sesión en la app."""

        if self.cargando:
            return

        if not self._validar_campos():
            self.update()
            return

        self._mostrar_cargando(True)

        try:
            await AutenticacionService.iniciar_sesion(
                page=self.page,
                email=self.email.value,
                contrasena=self.contrasena.value,
            )

            await Sesion.persistir(self.page)

            self._vaciar_campos()
            rol = self.__obtener_rol()

            if rol in ["POSTULANTE", "EMPLEADOR"]:
                await self.page.push_route("/busqueda")
            elif rol == "ADMINISTRADOR":
                await self.page.push_route(
                    "/perfil-personal-administrador"
                )

        except ErrorAutenticacion as error:
            mensaje = str(error)

            if "baneado" in mensaje.lower():
                self.mostrar_mensaje(
                    "Tu cuenta se encuentra baneada"
                )
            elif "desactivado" in mensaje.lower():
                self.mostrar_mensaje(
                    "Tu cuenta se encuentra desactivada"
                )
            else:
                self.mostrar_mensaje(
                    "Email o contraseña incorrectos"
                )

        except ErrorValidacion:
            self.mostrar_mensaje(
                "Los datos ingresados no son válidos"
            )

        except ErrorServidor:
            self.mostrar_mensaje(
                "Error en el servidor"
            )

        finally:
            self._mostrar_cargando(False)

    async def ir_recuperar_contrasena(self, e):
        await self._navegar(
            "/recuperar-contrasena",
            self.boton_recuperar,
            "¿Olvidaste tu contraseña?",
            ft.Colors.BLUE_600,
        )

    def mostrar_mensaje(self, mensaje):
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje)
            )
        )

    def _vaciar_campos(self):
        """Método para vaciar los campos."""

        self.email.value = ""

        self._marcar_error(
            self.email,
            self.error_email,
            None,
        )

        self.contrasena.value = ""

        self._marcar_error(
            self.contrasena,
            self.error_contrasena,
            None,
        )

    def __obtener_rol(self):
        """Método para verificar el rol del usuario."""

        if Sesion.rol(self.page) in [
            "POSTULANTE",
            "EMPLEADOR",
            "ADMINISTRADOR",
        ]:
            return Sesion.rol(self.page)

        return None