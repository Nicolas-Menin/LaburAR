from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.models.conexion_laboral import ConexionLaboral
from backend.app.models.postulante import Postulante
from backend.app.models.empleador import Empleador
from backend.app.models.oferta_laboral import OfertaLaboral

class ConexionLaboralDAO:
    """Clase encargada del acceso a los datos de conexion laboral"""

    def __init__(self,db: Session):
        self.db = db

    def crear_conexion_laboral(self, conexion_laboral: ConexionLaboral):
        """Metodo para crear conexiones laborales"""

        self.db.add(conexion_laboral)
        self.db.commit()
        self.db.refresh(conexion_laboral)

        return conexion_laboral

    def actualizar_conexion_laboral(self, conexion_laboral: ConexionLaboral):
        """Metodo para actualizar la conexion laboral"""

        self.db.commit()
        self.db.refresh(conexion_laboral)

        return conexion_laboral


    def listar_conexiones_laborales_postulante(
        self,
        id_postulante: int,
        busqueda: str | None = None,
        offset: int = 0,
        limit: int = 10
        ):
        """Metodo para traer conexiones laborales del postulante"""

        query = (self.db.query(
            ConexionLaboral.id.label("id"),
            Empleador.id.label("empleador_id"),
            OfertaLaboral.id.label("oferta_id"),
            Empleador.nombre_negocio.label("nombre_empleador"),
            OfertaLaboral.titulo.label("nombre_oferta"),
            ConexionLaboral.estado.label("estado"),
            ConexionLaboral.fecha_conexion.label("fecha_conexion")
            )
            .join(
                Empleador,
                ConexionLaboral.empleador_id == Empleador.id
            )
            .join(
                OfertaLaboral,
                ConexionLaboral.oferta_id == OfertaLaboral.id
            )
            .filter(ConexionLaboral.postulante_id == id_postulante)
        )

        if busqueda:
            query = query.filter(
                OfertaLaboral.titulo.ilike(f"%{busqueda}%")
            )

        return query.offset(offset).limit(limit).all()

    def listar_conexiones_laborales_empleador(
        self,
        id_empleador: int,
        busqueda: str | None = None,
        offset: int = 0,
        limit: int = 10
        ):
        """Metodo para traer conexiones laborales del empleador"""


        query =  (self.db.query(
                ConexionLaboral.id.label("id"),
                Postulante.id.label("postulante_id"),
                OfertaLaboral.id.label("oferta_id"),
                Postulante.nombre.label("nombre_postulante"),
                Postulante.apellido.label("apellido_postulante"),
                OfertaLaboral.titulo.label("nombre_oferta"),
                ConexionLaboral.estado.label("estado"),
                ConexionLaboral.fecha_conexion.label("fecha_conexion")
            )
            .join(
                Postulante,
                ConexionLaboral.postulante_id == Postulante.id
            )
            .join(
                OfertaLaboral,
                ConexionLaboral.oferta_id == OfertaLaboral.id
            )
            .filter(ConexionLaboral.empleador_id == id_empleador)
        )

        if busqueda:
            query = query.filter(
                or_(
                    Postulante.nombre.ilike(f"%{busqueda}%"),
                    Postulante.apellido.ilike(f"%{busqueda}%")
                )
            )

        return query.offset(offset).limit(limit).all()


    def buscar_por_id(self,conexion_laboral_id:int):
        """Metodo para buscar conexion laboral mediante id"""


        return (self.db.query(ConexionLaboral)
                .filter(ConexionLaboral.id == conexion_laboral_id)
                .first())


    def obtener_conexion_laboral_postulante(self,postulante_id:int, oferta_id:int):
        """Metodo para buscar conexion laboral de postulante"""


        return (self.db.query(
            ConexionLaboral.id.label("id"),
            Empleador.id.label("empleador_id"),
            OfertaLaboral.id.label("oferta_id"),
            Empleador.nombre_negocio.label("nombre_empleador"),
            OfertaLaboral.titulo.label("nombre_oferta"),
            ConexionLaboral.estado.label("estado"),
            ConexionLaboral.fecha_conexion.label("fecha_conexion")

                              )
                .join(OfertaLaboral,
                      ConexionLaboral.oferta_id == OfertaLaboral.id)
                .join(Empleador,
                      ConexionLaboral.empleador_id == Empleador.id)
                .filter(ConexionLaboral.postulante_id == postulante_id)
                .filter(ConexionLaboral.oferta_id== oferta_id)
                .first())

    def obtener_conexion_laboral_empleador(self,postulante_id: int,empleador_id:int, oferta_id:int | None = None):
        """Metodo para buscar conexion laboral de postulante"""


        return (self.db.query(
            ConexionLaboral.id.label("id"),
            Postulante.id.label("postulante_id"),
            OfertaLaboral.id.label("oferta_id"),
            Postulante.nombre.label("nombre_postulante"),
            Postulante.apellido.label("apellido_postulante"),
            OfertaLaboral.titulo.label("nombre_oferta"),
            ConexionLaboral.estado.label("estado"),
            ConexionLaboral.fecha_conexion.label("fecha_conexion")

                            )
            .join(OfertaLaboral,
                    ConexionLaboral.oferta_id == OfertaLaboral.id)
            .join(Postulante,
                    ConexionLaboral.postulante_id == Postulante.id)
            .filter(ConexionLaboral.empleador_id == empleador_id)
            .filter(ConexionLaboral.oferta_id== oferta_id)
            .filter(ConexionLaboral.postulante_id == postulante_id)
            .first())

    def buscar_conexion_laboral(
        self,
        postulante_id: int,
        empleador_id:int,
        oferta_id: int | None = None,
        ):
        """Metodo para buscar conexion laboral"""

        query =  (self.db.query(ConexionLaboral)
                .filter(ConexionLaboral.postulante_id == postulante_id)
                .filter(ConexionLaboral.empleador_id == empleador_id)
        )
        if oferta_id is not None:
            query = query.filter(ConexionLaboral.oferta_id == oferta_id)

        return query.first()