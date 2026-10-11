from sqlalchemy.orm import Session
from backend.app.models.conversacion import Conversacion
from backend.app.models.conexion_laboral import ConexionLaboral
from backend.app.models.empleador import Empleador
from backend.app.models.oferta_laboral import  OfertaLaboral
from backend.app.models.postulante import Postulante
from backend.app.models.usuario import Usuario

class ConversacionDAO:
    """Clase encargada del acceso a los datos de conversacion"""

    def __init__(self,db: Session):
        self.db = db


    def crear_conversacion(self, conversacion: Conversacion ):
        """Metodo para crear conversacion"""


        self.db.add(conversacion)
        self.db.commit()
        self.db.refresh(conversacion)

        return conversacion


    def traer_conversaciones_postulante(
        self,
        postulante_id: int,
    ):
        """Metodo para traer conversaciones de postulante"""

        return (
            self.db.query(Conversacion.id,
                          Empleador.nombre_negocio,
                          Empleador.foto_perfil,
                          OfertaLaboral.titulo,
                          )
            .join(ConexionLaboral,
                  Conversacion.conexion_laboral_id ==  ConexionLaboral.id)
            .join(Empleador,
                  ConexionLaboral.empleador_id == Empleador.id)
            .join(OfertaLaboral,
                  ConexionLaboral.oferta_id == OfertaLaboral.id)
            .join(
                Usuario,
                Empleador.usuario_id == Usuario.id
            )
            .filter(ConexionLaboral.postulante_id == postulante_id)
            .filter(ConexionLaboral.estado =="ACEPTADA")
            .filter(Usuario.estado =="ACTIVO")
        ).all()


    def traer_conversaciones_empleador(
        self,
        empleador_id: int,
        oferta_id: int | None = None
    ):
        """Metodo para traer conversaciones de empleador"""

        query =  (
            self.db.query(Conversacion.id,
                          Postulante.nombre,
                          Postulante.apellido,
                          Postulante.foto_perfil,
                          OfertaLaboral.titulo
                          )
            .join(ConexionLaboral,
                  Conversacion.conexion_laboral_id == ConexionLaboral.id
                  )
            .join(Postulante,
                  ConexionLaboral.postulante_id == Postulante.id)
            .join(
                Usuario,
                Postulante.usuario_id == Usuario.id
            )
            .join(OfertaLaboral,
                  ConexionLaboral.oferta_id == OfertaLaboral.id)
            .filter(ConexionLaboral.empleador_id == empleador_id)
            .filter(ConexionLaboral.estado =="ACEPTADA")
            .filter(Usuario.estado =="ACTIVO")

        )

        if oferta_id:

            query = query.filter(
                OfertaLaboral.id == oferta_id
            )

        return query.all()
