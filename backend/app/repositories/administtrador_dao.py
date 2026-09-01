from typing import Literal
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.models.empleador import Empleador
from backend.app.models.postulante import Postulante
from backend.app.models.usuario import Usuario

class AdministradorDAO:


    def __init__(self, db: Session):
        self.db = db


    def listar_usuarios(
        self,
        rol: Literal["POSTULANTE","EMPLEADOR"],
        busqueda: str | None = None,
        offset: int = 0,
        limit: int = 10
        ):
        """Metodo para listar y buscar usuarios por rol"""

        if rol == "POSTULANTE":

            query = (self.db.query(
                Postulante.id,
                Postulante.nombre,
                Postulante.apellido,
                Usuario.estado,
                Usuario.fecha_creacion
                )
                .join(Usuario,
                      Postulante.usuario_id == Usuario.id)
            )

            if busqueda:
                query = query.filter(
                    or_(Postulante.nombre.ilike(f"½{busqueda}%"),
                        Postulante.apellido.ilike(f"½{busqueda}%"),
                    )
                )

        elif rol == "EMPLEADOR":

            query = (
                self.db.query(
                    Empleador.id,
                    Empleador.nombre_negocio,
                    Usuario.estado,
                    Usuario.fecha_creacion
                )
                .join(
                    Usuario,
                    Empleador.usuario_id == Usuario.id
                )
            )

            if busqueda:
                query = query.filter(
                    Empleador.nombre_negocio.ilike(f"½{busqueda}%")

                )



        return query.offset(offset).limit(limit).all()
