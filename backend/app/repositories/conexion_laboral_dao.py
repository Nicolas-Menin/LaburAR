from sqlalchemy.orm import Session
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


    def listar_conexiones_laborales_postulante(self,id_postulante: int):
        """Metodo para traer conexiones laborales del postulante"""

        return (self.db.query(
            ConexionLaboral.id,
            Empleador.id,
            OfertaLaboral.id,
            Empleador.nombre_negocio,
            OfertaLaboral.titulo,
            ConexionLaboral.estado,
            ConexionLaboral.fecha_conexion
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
            .all()
        )

    def listar_conexiones_laborales_empleado(self,id_empleado: int):
        """Metodo para traer conexiones laborales del empleador"""

        return (
            self.db.query(
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
            .filter(ConexionLaboral.empleador_id == id_empleado)
            .all()
        )