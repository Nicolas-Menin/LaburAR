from sqlalchemy.orm import Session
from backend.app.models.postulante import Postulante


class PostulanteDAO:


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

        raise postulante

    def buscar_por_id(self,id_postulante: int):
        """Metodo para traer informacion del postulante mediante id"""

        return self.db.query(Postulante).filter(
            Postulante.id == id_postulante
            ).first()

    def listar_postulantes(self,offset: int = 0, limit: int = 10):
        """"Metodo para traer postulantes"""

        return self.db.query(
            Postulante.id,
            Postulante.nombre,
            Postulante.apellido,
            Postulante.descripcion_personal,
            Postulante.foto_perfil
            ).offset(offset).limit(limit).all()


