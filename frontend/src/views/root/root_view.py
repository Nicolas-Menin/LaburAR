from urllib.parse import urlparse, parse_qs
import flet as ft
from frontend.src.views.empleador.registrar_empleador_view import RegistrarEmpleadorView
from frontend.src.views.postulante.registrar_postulante_view import RegistrarPostulanteView
from frontend.src.views.seleccion_usuario_view import SeleccionUsuariorView
from frontend.src.views.iniciar_sesion_view import IniciarSesionView
from frontend.src.views.busqueda_view import BusquedaView
from frontend.src.views.vista_perfil_oferta_laboral_view import PerfilOfertaLaboralView
from frontend.src.views.vista_perfil_postulante_view import PerfilPostulanteView
from frontend.src.views.vista_previa_empleador_view import PerfilEmpleadorView
from frontend.src.views.recuperar_contrasena_view import RecuperarContrasenaView
from frontend.src.views.restablecer_contrasena_view import RestablecerContrasenaView
from frontend.src.views.postulante.vista_perfil_personal_view import PerfilPersonalPostulanteView
from frontend.src.views.empleador.vista_perfil_personal_view import PerfilPersonalEmpleadorView
from frontend.src.views.postulante.editar_perfil import EditarPerfilPostulanteView
from frontend.src.views.postulante.postulaciones_view import PostulacionesView
from frontend.src.views.postulante.solicitudes_contacto_view import SolicitudesView
from frontend.src.views.empleador.editar_perfil import EditarPerfilEmpleadorView
from frontend.src.views.reporte_view import ReporteView
from frontend.src.views.mensajeria_view import MensajeriaView
from frontend.src.views.empleador.gestion_solicitudes_view import GestionSolicitudesView
from frontend.src.views.empleador.gestion_postulaciones_view import GestionPostulantesView
from frontend.src.views.empleador.gestion_ofertas_view import GestionOfertasView
from frontend.src.views.administrador.vista_perfil_personal_view import PerfilPersonalAdministradorView
from frontend.src.views.administrador.gestion_reportes_view import GestionReportesView
from frontend.src.views.administrador.gestion_usuarios_view import GestionUsuariosView
from frontend.src.session.sesion import Sesion

# pylint: disable=E1121,E1123,E0401, E1101


class RootView:

    def __init__(self, page: ft.Page):
        self.page = page

        self.page.padding = 0
        self.page.spacing = 0

        self.page.on_route_change = self.route_change
        self.page.on_resize = self.handle_size
        self.page.on_disconnect = self._pagina_desconectada

        self.page.title = "LaburAR"
        self.page.bgcolor = "#f52d2d"

        self.registrar_postulante = RegistrarPostulanteView()
        self.registrar_empleador = RegistrarEmpleadorView()
        self.seleccion_usuario = SeleccionUsuariorView()
        self.iniciar_sesion = IniciarSesionView()
        self.perfil_postulante = PerfilPostulanteView()
        self.perfil_oferta = PerfilOfertaLaboralView()
        self.recuperar_contrasena = RecuperarContrasenaView()
        self.editar_perfil_empleador = EditarPerfilEmpleadorView()
        self.editar_perfil_postulante = EditarPerfilPostulanteView()
        self.gestion_reportes = GestionReportesView()
        self.gestion_solicitudes = GestionSolicitudesView(
            self.perfil_postulante
        )
        self.gestion_postulantes = GestionPostulantesView(
            self.perfil_postulante
        )
        self.gestion_ofertas = GestionOfertasView(
            self.perfil_oferta
        )
        self.perfil_empleador = PerfilEmpleadorView(
            perfil_oferta=self.perfil_oferta
        )
        self.perfil_personal_empleador = PerfilPersonalEmpleadorView(
            self.editar_perfil_empleador,
            self.gestion_solicitudes,
            self.gestion_postulantes,
            self.gestion_ofertas,
            self.perfil_empleador
        )
        self.mensajeria = MensajeriaView()
        self.postulaciones = PostulacionesView(
            self.perfil_empleador,
            self.perfil_oferta
        )
        self.solicitudes = SolicitudesView(
            self.perfil_empleador
        )
        self.perfil_personal_postulante = PerfilPersonalPostulanteView(
            self.editar_perfil_postulante,
            self.postulaciones,
            self.solicitudes,
            self.perfil_postulante
        )
        self.busqueda = BusquedaView(
            self.perfil_postulante,
            self.perfil_empleador,
            self.perfil_oferta,
            self.perfil_personal_postulante,
            self.perfil_personal_empleador
        )
        self.gestion_usuarios = GestionUsuariosView(
            self.perfil_postulante,
            self.perfil_empleador,
        )
        self.perfil_personal_admin = PerfilPersonalAdministradorView(
            self.gestion_usuarios,
            self.gestion_reportes
        )


        self.page.fonts = {
            "Inter-Regular": "fonts/Inter_18pt-Regular.ttf",
            "Inter-Medium": "fonts/Inter_18pt-Medium.ttf",
            "Inter-Bold": "fonts/Inter_18pt-Bold.ttf"
        }

        self.page.theme = ft.Theme(
            font_family="Inter-Regular",
            page_transitions=ft.PageTransitionsTheme(
                linux=ft.PageTransitionTheme.ZOOM,
                windows=ft.PageTransitionTheme.ZOOM
            )
        )

        self.RUTAS_PUBLICAS = {
            "/login",
            "/registrar-empleador",
            "/registrar-postulante",
            "/seleccionar-usuario",
            "/recuperar-contraseña",
            "/restablecer-contraseña"
        }

    async def route_change(self, view):
        """Metodo para cambiar de View"""

        print(f"RUTA RECIBIDA: {view.route}")
        route = view.route.split("?")[0]
        print(f"RUTA PROCESADA: {route}")

        if route == "/":
            await self.page.push_route("/login")
            return

        if route != "/busqueda":
            self.busqueda.detener_verificacion_mensajes()

        if route != "/mensajes":
            self.mensajeria.detener_verificacion_conversaciones()

        self.page.views.clear()
        print(f"RUTA PUBLICA: {route in self.RUTAS_PUBLICAS}")
        if route not in self.RUTAS_PUBLICAS:
            token = Sesion.token(self.page)

            if token is None or Sesion.token_vencido(self.page):
                Sesion.cerrar(self.page)
                self.mostrar_dialogo_sesion_expirada()
                await self.page.push_route("/login")
                return

        views = {
            "/login": self.iniciar_sesion,
            "/registrar-empleador": self.registrar_empleador,
            "/registrar-postulante": self.registrar_postulante,
            "/seleccionar-usuario": self.seleccion_usuario,
            "/busqueda": self.busqueda,
            "/perfil-postulante": self.perfil_postulante,
            "/perfil-empleador": self.perfil_empleador,
            "/perfil-oferta": self.perfil_oferta,
            "/mensajes": self.mensajeria,
            "/recuperar-contraseña": self.recuperar_contrasena,
            "/perfil-personal-postulante": self.perfil_personal_postulante,
            "/perfil-personal-empleador": self.perfil_personal_empleador,
            "/editar-perfil-postulante": self.editar_perfil_postulante,
            "/postulaciones": self.postulaciones,
            "/solicitudes": self.solicitudes,
            "/editar-perfil-empleador": self.editar_perfil_empleador,
            "/gestion-solicitudes": self.gestion_solicitudes,
            "/gestion-postulantes": self.gestion_postulantes,
            "/gestion-ofertas": self.gestion_ofertas,
            "/perfil-personal-administrador": self.perfil_personal_admin,
            "/gestion-usuarios": self.gestion_usuarios,
            "/gestion-reportes": self.gestion_reportes
        }



        if route == "/reporte":
            usuario_reportado_id = self.obtener_usuario_reportado(view)

            self.page.views.append(
                ReporteView(
                    usuario_reportado_id=int(usuario_reportado_id)
                )
            )
        elif route == "/restablecer-contraseña":
            token = self.obtener_token_recuperacion(view)

            self.page.views.append(
                RestablecerContrasenaView(token=token)
            )

        elif route in views:
            self.page.views.append(views[route])

        self.page.update()
        self.handle_size(None)

    def handle_size(self, _):
        """Maneja el tamaño de la imagen de fondo"""

        if not self.page.views:
            return

        current_view = self.page.views[-1]

        if hasattr(current_view, "bg_image"):
            current_view.bg_image.width = self.page.width
            current_view.bg_image.height = self.page.height

        self.page.update()

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
                            on_click=lambda e:
                            self.page.pop_dialog(),
                        )
                    ],
                )
            )

    def obtener_token_recuperacion(self,view):

        url = urlparse(view.route)
        parametros = parse_qs(url.query)

        token = parametros.get("token", [None])[0]

        return token

    def obtener_usuario_reportado(self, view):
        """Obtiene el ID del usuario reportado desde la URL."""

        url = urlparse(view.route)
        parametros = parse_qs(url.query)

        return parametros.get("usuario_reportado_id", [None])[0]

    def _pagina_desconectada(self, e):
        self.busqueda.detener_verificacion_mensajes()
        self.mensajeria.detener_verificacion_conversaciones()