from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.models.postulacion import Postulacion
from backend.app.models.oferta_laboral import OfertaLaboral
from backend.app.models.empleador import Empleador
from backend.app.models.postulante import Postulante


class PostulacionDAO:
    """Clase encargada del acceso a los datos de postulacion"""

    def __init__(self,db: Session):
        self.db = db


    def crear_postulacion(self,postulacion: Postulacion):
        """Metodo para crear postulacion del postulante"""

        self.db.add(postulacion)
        self.db.commit()
        self.db.refresh(postulacion)

        return postulacion

    def filtrar_postulaciones_postulante(
        self,
        id_postulante: int,
        busqueda: str | None = None,
        offset: int = 0,
        limit: int = 10
        ):
        """Metodo para filtrar las postulaciones del postulante"""

        query = (self.db.query(
            Postulacion.id,
            Postulacion.oferta_id,
            Empleador.id,
            OfertaLaboral.titulo,
            Empleador.nombre_negocio,
            Empleador.foto_perfil,
            Postulacion.estado,
            Postulacion.fecha_postulacion,
            Postulacion.estado
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

        )

        if busqueda:
            query = query.filter(
                OfertaLaboral.titulo.ilike(f"%{busqueda}%")
            )

        return query.offset(offset).limit(limit).all()


    def filtrar_postulaciones_oferta_laboral(
        self,
        id_empleador: int,
        oferta_id: int | None = None,
        busqueda: str | None = None,
        offset: int = 0,
        limit: int = 10
        ):
        """Metodo para listar las postulaciones de ofertas laborales de empleador"""


        query = (self.db.query(
                Postulacion.id.label("postulacion_id"),
                Postulante.id.label("postulante_id"),
                OfertaLaboral.id.label("oferta_id"),
                OfertaLaboral.titulo,
                Postulante.nombre,
                Postulante.apellido,
                Postulante.foto_perfil,
                Postulacion.estado,
                Postulacion.fecha_postulacion,
                Postulacion.estado
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
        )

        if busqueda:
            query = query.filter(
                or_(Postulante.nombre.ilike(f"%{busqueda}%"),
                    Postulante.apellido.ilike(f"%{busqueda}%")
                )
            )

        if oferta_id:
            query = query.filter(
                Postulacion.oferta_id == oferta_id
            )


        return query.offset(offset).limit(limit).all()


    def buscar_postulacion(self,postulante_id: int,oferta_id: int):
        """Metodo para buscar postulacion de postulante"""


        return (self.db.query(
            Postulacion
            )
            .filter(Postulacion.postulante_id == postulante_id)
            .filter(Postulacion.oferta_id == oferta_id)
        ).first()

    def actualizar_postulacion(self,postulacion: Postulacion):
        """Metodo para actualizar postulacion de postulante"""

        self.db.commit()
        self.db.refresh(postulacion)

        return postulacion