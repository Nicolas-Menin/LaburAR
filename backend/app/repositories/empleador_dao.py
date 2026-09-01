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


    def buscar_por_id(self,usuario_id: int):
        """Metodo para traer informacion del empleador mediante id"""


        return self.db.query(Empleador).filter(Empleador.usuario_id == usuario_id).first()

    def listar_empleadores(self,offset: int = 0, limit: int = 10):
        """Metodo para traer empleadores """

        return self.db.query(
            Empleador.id,
            Empleador.nombre_negocio,
            Empleador.descripcion,
            Empleador.foto_perfil
        ).offset(offset).limit(limit).all()


    def filtrar_empleadores(
        self,
        busqueda: str | None = None,
        direccion: str | None = None,
        ubicacion: str | None = None,
        rubro: str | None = None,
        offset: int = 0,
        limit: int = 10
        ):
        """Metodo para filtrar empleadores"""


        query = self.db.query(Empleador)

        if busqueda:
            query = query.filter(Empleador.nombre_negocio.ilike(busqueda))

        if direccion:
            query = query.filter(Empleador.direccion.ilike(direccion))

        if ubicacion:
            query = query.filter(Empleador.ubicacion == ubicacion)

        if rubro:
            query = query.filter(Empleador.rubro.ilike(rubro))


        return (
            query.distinct().offset(offset).limit(limit).all()
        )