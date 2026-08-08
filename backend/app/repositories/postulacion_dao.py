from sqlalchemy.orm import Session
from backend.app.models.postulacion import Postulacion
from backend.app.models.oferta_laboral import OfertaLaboral
from backend.app.models.empleador import Empleador
from backend.app.models.postulante import Postulante


class PostulacionDAO:


    def __init__(self,db: Session):
        self.db = db


    def crear_postulacion(self,postulacion: Postulacion):
        """Metodo para crear postulacion del postulante"""

        self.db.add(postulacion)
        self.db.commit()
        self.db.refresh(postulacion)

        return postulacion

    def listar_postulaciones_postulante(self,id_postulante: int):
        """Metodo para listar las postulaciones del postulante"""
        return (self.db.query(
            Postulacion.oferta_id,
            Postulacion.oferta_id,
            Empleador.id,
            OfertaLaboral.titulo,
            Empleador.nombre_negocio,
            Empleador.foto_perfil,
            Postulacion.estado,
            Postulacion.fecha_postulacion
            )
            .join(
                Empleador,
                Postulacion.empleador_id == Empleador.id
            )
            .join(
                OfertaLaboral,
                Postulacion.oferta_id == OfertaLaboral.id
            )
            .filter(Postulacion.postulante_id == id_postulante)
            .all()
        )

    def listar_postulaciones_empleador(self,id_empleador: int):
        """Metodo para visualizar las postulaciones a ofertas laborales del empleador"""
        return (self.db.query(
            Postulacion.id,
            Postulante.id,
            OfertaLaboral.titulo,
            Postulante.nombre,
            Postulante.apellido,
            Postulante.foto_perfil,
            Postulacion.estado,
            Postulacion.fecha_postulacion
        )
        .join(
            Postulante,
            Postulacion.postulante_id == Postulante.id
        )
        .join(
            OfertaLaboral,
            Postulacion.oferta_id == OfertaLaboral.id
        )
        .filter(Postulacion.empleador_id == id_empleador)
        .all()
        )