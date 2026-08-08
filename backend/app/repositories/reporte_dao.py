from sqlalchemy.orm import Session
from backend.app.models.reporte import Reporte



class ReporteDAO:

    def __init__(self,db: Session):
        self.db = db


    def crear_reporte(self,reporte: Reporte):
        """Metodo para crear reporte"""

        self.db.add(reporte)
        self.db.commit()
        self.db.refresh(reporte)

        return reporte


    def actualizar_reporte(self, reporte: Reporte):
        """Metodo para actualizar el reporte"""
        self.db.commit()
        self.db.refresh(reporte)

        return reporte