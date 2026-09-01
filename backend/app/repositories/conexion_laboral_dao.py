from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.models.conexion_laboral import ConexionLaboral
from backend.app.models.postulante import Postulante
from backend.app.models.empleador import Empleador
from backend.app.models.oferta_laboral import OfertaLaboral

class ConexionLaboralDAO:

    def __init__(self,db: Session):
        self.db = db

    def crear_conexion_laboral_postulante(self, conexion_laboral: ConexionLaboral):
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
            ConexionLaboral.id,
            Empleador.id,
            OfertaLaboral.id,
            Empleador.nombre_negocio,
            OfertaLaboral.titulo,
            ConexionLaboral.estado,
            ConexionLaboral.fecha_conexion,
            ConexionLaboral.estado
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
                ConexionLaboral.id,
                Postulante.id,
                OfertaLaboral.id,
                Postulante.nombre,
                Postulante.apellido,
                OfertaLaboral.titulo,
                ConexionLaboral.estado
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