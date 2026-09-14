from backend.app.repositories.conversacion_dao import ConversacionDAO
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.empleador_dao import EmpleadorDAO
from backend.app.repositories.mensaje_dao import MensajeDAO


class ConversacionService:
    """Service de Conversacion"""

    def __init__(self,
                 conversacion_dao: ConversacionDAO,
                 postulante_dao: PostulanteDAO,
                 empleador_dao: EmpleadorDAO,
                 mensaje_dao: MensajeDAO
                 ):
        self.conversacion_dao = conversacion_dao
        self.postulante_dao = postulante_dao
        self.empleador_dao = empleador_dao
        self.mensaje_dao = mensaje_dao


    def traer_conversacion_postulante(
        self,
        usuario_id: int,
    ):
        """Metodo para traer conversaciones de postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)


        conversaciones = self.conversacion_dao.traer_conversaciones_postulante(postulante.id)

        return [{

                "conversacion_id": conversacion.id,
                "nombre_empleador": conversacion.nombre_negocio,
                "foto_perfil": conversacion.foto_perfil,
                "nombre_oferta": conversacion.titulo,
                "cantidad_mensajes_no_leidos": self.mensaje_dao.contar_mensajes_no_leidos(usuario_id,conversacion.id)

            }
                for conversacion in conversaciones
        ]


    def traer_conversacion_empleador(
        self,
        usuario_id: int,
    ):
        """Metodo para traer conversaciones de empleador"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)


        conversaciones = self.conversacion_dao.traer_conversaciones_empleador(empleador.id)

        return [{

                "conversacion_id": conversacion.id,
                "nombre": conversacion.nombre,
                "apellido": conversacion.apellido,
                "foto_perfil": conversacion.foto_perfil,
                 "nombre_oferta": conversacion.titulo,
                "cantidad_mensajes_no_leidos": self.mensaje_dao.contar_mensajes_no_leidos(usuario_id,conversacion.id)

            }
                for conversacion in conversaciones
        ]