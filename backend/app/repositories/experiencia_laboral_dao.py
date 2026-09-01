from sqlalchemy.orm import Session
from backend.app.models.experiencia_laboral import ExperienciaLaboral


class ExperienciaLaboralDAO:

    def __init__(self, db: Session):
        self.db = db


    def crear_experiencia_laboral(self,experiencia_laboral: ExperienciaLaboral):
        """Metodo para crear experiencia laboral del postulante"""

        self.db.add(experiencia_laboral)
        self.db.commit()
        self.db.refresh(experiencia_laboral)

        return  experiencia_laboral


    def actualizar_experiencia_laboral(self,experiencia_laboral: ExperienciaLaboral):
        """Metodo para actualizar los datos de la experiencia laboral"""

        self.db.commit()
        self.db.refresh(experiencia_laboral)

        return experiencia_laboral


    def eliminar_experiencia_laboral(self,experiencia_laboral: ExperienciaLaboral):
        """Metodo para eliminar experiencias laborales del postulante"""

        self.db.delete(experiencia_laboral)
        self.db.commit()


    def buscar_por_id(self,experiencia_laboral_id: int,postulante_id :int):
        """Metodo para traer experiencia laboral mediante id"""


        return (
            self.db.query(ExperienciaLaboral)
            .filter(ExperienciaLaboral.id == experiencia_laboral_id)
            .filter(ExperienciaLaboral.postulante_id == postulante_id )
        ).first()

