from sqlalchemy.orm import Session
from backend.app.models.habilidad import Habilidad



class HabilidadDAO:
    """Clase encargada del acceso a los datos de habilidad de postulante"""

    def __init__(self,db: Session):
        self.db = db


    def crear_habilidad(self,habilidad: Habilidad):
        """Metodo para crear habilidad del postulante"""

        self.db.add(habilidad)
        self.db.commit()
        self.db.refresh(habilidad)

        return habilidad

    def eliminar_habilidad(self,habilidad: Habilidad):
        """Metodo para eliminar habilidad del postulante"""

        self.db.delete(habilidad)
        self.db.commit()

