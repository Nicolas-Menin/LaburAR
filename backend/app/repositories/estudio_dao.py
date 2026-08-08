from sqlalchemy.orm import Session
from backend.app.models.estudio import Estudio


class EstudiosDAO:

    def __init__(self, db: Session):
        self.db = db


    def crear_estudio(self,estudio: Estudio):
        """Metodo para crear estudio del postulante"""

        self.db.add(estudio)
        self.db.commit()
        self.db.refresh(estudio)

        return estudio


    def actualizar_estudio(self,estudio:Estudio):
        """Metodo para actualizar los datos del estudio"""


        self.db.commit()
        self.db.refresh(estudio)

        return estudio


    def eliminar_estudio(self,estudio: Estudio):
        """Metodo para eliminar estudio del postulante"""


        self.db.delete(estudio)
        self.db.commit()


