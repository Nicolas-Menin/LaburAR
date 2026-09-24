from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.models.postulante import Postulante
from backend.app.models.estudio import Estudio
from backend.app.models.experiencia_laboral import ExperienciaLaboral
from backend.app.models.habilidad import Habilidad
from backend.app.models.usuario import Usuario

class PostulanteDAO:
    """Clase encargada del acceso a los datos de postulante"""

    def __init__(self,db: Session):
        self.db = db



    def crear_postulante(self,postulante: Postulante):
        """Metodo para crear postulante"""

        self.db.add(postulante)
        self.db.commit()
        self.db.refresh(postulante)

        return postulante


    def actualizar_postulante(self, postulante: Postulante):
        """Metodo para actualizar los datos del postulante"""

        self.db.commit()
        self.db.refresh(postulante)

        return postulante

    def buscar_por_id(self,usuario_id: int):
        """Metodo para traer informacion del postulante mediante id"""

        return self.db.query(Postulante).filter(
            Postulante.usuario_id == usuario_id
            ).first()

    def listar_postulantes(self,offset: int = 0, limit: int = 10):
        """"Metodo para traer postulantes"""

        return (self.db.query(
            Postulante.id,
            Postulante.nombre,
            Postulante.apellido,
            Postulante.descripcion_personal,
            Postulante.foto_perfil
            ).offset(offset).limit(limit).all()
        )

    def filtrar_postulantes(
            self,
            busqueda: str | None = None,
            ubicacion: str | None = None,
            estudios: str | None = None,
            habilidades: list[str] | None = None,
            experiencias_laborales: str | None = None,
            disponibilidad: str | None = None,
            offset: int = 0,
            limit: int = 10,
        ):
        """Metodo para filtrar postulantes"""

        query = self.db.query(Postulante).join(
            Usuario, Postulante.usuario_id == Usuario.id
        ).filter(Usuario.estado == "ACTIVO")

        if busqueda is not None:
            query = query.filter(
                or_(
                    Postulante.nombre.ilike(f"%{busqueda}%"),
                    Postulante.apellido.ilike(f"%{busqueda}%")
                )
            )

        if ubicacion is not None:
            query = query.filter(
                Postulante.ubicacion.ilike(f"%{ubicacion}%")
            )

        if estudios is not None:
            query = (
                query
                .join(Postulante.estudios)
                .filter(
                    Estudio.titulo.ilike(f"%{estudios}%")
                )
            )

        if experiencias_laborales is not None:
            query = (
                query
                .join(Postulante.experiencias_laborales)
                .filter(
                    ExperienciaLaboral.puesto.ilike(
                        f"%{experiencias_laborales}%"
                    )
                )
            )

        if habilidades is not None:
            query = (
                query
                .join(Postulante.habilidades)
                .filter(
                    Habilidad.nombre.in_(habilidades)
                )
            )

        if disponibilidad is not None:
            query = (
                query
                .filter(Postulante.disponibilidad.like(f"{disponibilidad}"))
            )


        return query.distinct().offset(offset).limit(limit).all()
