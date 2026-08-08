from sqlalchemy.orm import Session
from backend.app.models.empleador import Empleador
from backend.app.models.postulante import Postulante

class AdministradorDAO:


    def __init__(self, db: Session):
        self.db = db



    def listar_postulante(self,offset: int = 0, limit: int = 10):
        """Metodo para listar postulantes desde el panel administrador"""


        return self.db.query(Postulante).offset(offset).limit(limit).all()


    def listar_empleador(self,offset: int = 0, limit: int = 10):
        """Metodo para listar empleadores desde el panel administrador"""

        return self.db.query(Empleador).offset(offset).limit(limit).all()
