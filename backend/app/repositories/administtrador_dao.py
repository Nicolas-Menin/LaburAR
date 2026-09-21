from typing import Literal
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.models.empleador import Empleador
from backend.app.models.postulante import Postulante
from backend.app.models.usuario import Usuario

class AdministradorDAO:
    """Clase encargada del acceso a los datos de administrador"""

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
                Usuario.id.label("usuario_id"),
                Postulante.id.label("postulante_id"),
                Postulante.nombre.label("nombre_postulante"),
                Postulante.apellido.label("apellido_postulante"),
                Usuario.rol.label("rol"),
                Usuario.estado.label("estado"),
                Usuario.fecha_creacion.label("fecha_creacion"),
                Postulante.foto_perfil.label("foto_perfil")
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
                    Usuario.id.label("usuario_id"),
                    Empleador.id.label("empleador_id"),
                    Empleador.nombre_negocio.label("nombre_negocio"),
                    Usuario.rol.label("rol"),
                    Usuario.estado.label("estado"),
                    Usuario.fecha_creacion.label("fecha_creacion"),
                    Empleador.foto_perfil.label("foto_perfil")
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

    def actualizar_estado_usuario(self,usuario: Usuario):
        """Metodo para cambiar el estado de usuario"""

        self.db.commit()
        self.db.refresh(usuario)

        return usuario
