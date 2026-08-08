from sqlalchemy.orm import Session
from backend.app.models.empleador import Empleador


class EmpleadorDAO:

    def __init__(self, db: Session):
        self.db = db

    def crear_empleador(self, empleador:Empleador):
        """Metodo para crear empleador"""

        self.db.add(empleador)
        self.db.commit()
        self.db.refresh(empleador)

        return empleador


    def actualizar_empleador(self,empleador:Empleador):
        """Metodo para actualizar empleador"""
        self.db.commit()
        self.db.refresh(empleador)

        return empleador


    def buscar_por_id(self,id_empleador: int):
        """Metodo para traer informacion del empleador mediante id"""


        return self.db.query(Empleador).filter(Empleador.id == id_empleador).first()

    def listar_empleadores(self,offset: int = 0, limit: int = 10):
        """Metodo para traer empleadores """

        return self.db.query(
            Empleador.id,
            Empleador.nombre_negocio,
            Empleador.descripcion,
            Empleador.foto_perfil
        ).offset(offset).limit(limit).all()


