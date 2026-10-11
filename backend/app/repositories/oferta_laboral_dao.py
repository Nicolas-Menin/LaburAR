from typing import Literal, List
from sqlalchemy.orm import Session
from backend.app.models.oferta_laboral import OfertaLaboral
from backend.app.models.empleador import Empleador
from backend.app.models.usuario import Usuario
from backend.app.models.conexion_laboral import ConexionLaboral
class OfertaLaboralDAO:
    """Clase encargada del acceso a los datos de oferta laboral"""

    def __init__(self,db: Session):
        self.db = db


    def crear_oferta_laboral(self,oferta_laboral: OfertaLaboral):
        """Metodo para crear oferta laboral"""

        self.db.add(oferta_laboral)
        self.db.commit()
        self.db.refresh(oferta_laboral)

        return oferta_laboral


    def actualizar_oferta(self, oferta_laboral: OfertaLaboral):
        """Metodo para actualizar los datos de la oferta laboral"""

        self.db.commit()
        self.db.refresh(oferta_laboral)

        return oferta_laboral


    def buscar_por_id(self,id_oferta_laboral: int):
        """Metodo para traer informacion de oferta laboral mediante id"""

        return self.db.query(OfertaLaboral).filter(
            OfertaLaboral.id == id_oferta_laboral
        ).first()

    def perfil_oferta_laboral(self,id_oferta_laboral: int):
        """Metodo para perfil de oferta laboral"""

        return (
            self.db.query(
                OfertaLaboral.titulo,
                OfertaLaboral.descripcion,
                Empleador.nombre_negocio,
                Empleador.foto_perfil.label("foto_empleador"),
                OfertaLaboral.ubicacion,
                OfertaLaboral.direccion,
                OfertaLaboral.requisitos,
                OfertaLaboral.rubro,
                OfertaLaboral.salario_tipo,
                OfertaLaboral.salario_minimo,
                OfertaLaboral.salario_maximo,
                OfertaLaboral.jornada,
                OfertaLaboral.turno,
                OfertaLaboral.dias_laborales,
                OfertaLaboral.hora_inicio,
                OfertaLaboral.hora_fin,
                OfertaLaboral.fecha_creacion
            ).join(
                Empleador,
                OfertaLaboral.empleador_id == Empleador.id
            ).filter(OfertaLaboral.id == id_oferta_laboral)
        ).first()

    def buscar_por_empleador(self,empleador_id: int,oferta_id:int):
        """Metodo para traer informacion de oferta laboral mediante id"""

        return self.db.query(OfertaLaboral).filter(
            OfertaLaboral.id == oferta_id
        ).filter(OfertaLaboral.empleador_id == empleador_id).first()

    def listar_ofertas_laborales(self,empleador_id: int,busqueda: str | None = None):
        """Metodo para traer ofertas laboraless de empleador"""

        query = (self.db.query(
            OfertaLaboral.id.label("id"),
            OfertaLaboral.titulo.label("titulo"),
            OfertaLaboral.ubicacion.label("ubicacion"),
            OfertaLaboral.direccion.label("direccion"),
            OfertaLaboral.estado.label("estado"),
            OfertaLaboral.descripcion.label("descripcion"),
            Empleador.foto_perfil.label("foto_perfil_empleador"),
            OfertaLaboral.fecha_creacion.label("fecha_creacion")
            ).join(Empleador,
                   OfertaLaboral.empleador_id == Empleador.id
            ).filter(OfertaLaboral.empleador_id == empleador_id)
        )


        if busqueda:
            query = query.filter(OfertaLaboral.titulo.ilike(f"%{busqueda}%"))

        return query.all()

    def verificar_conexion_por_oferta(self,empleador_id:int, postulante_id: int):
        """Metodo que verifica  que ofertas laborales NO poseen una conexion laboral"""
        conexiones_existentes = (
            self.db.query(ConexionLaboral.id)
            .filter(
                ConexionLaboral.oferta_id == OfertaLaboral.id,
                ConexionLaboral.postulante_id == postulante_id,
                ConexionLaboral.estado.in_(["PENDIENTE", "ACEPTADA"])
            ).exists()
        )

        return (self.db.query(
            OfertaLaboral.id.label("id"),
            OfertaLaboral.titulo.label("titulo"),
            OfertaLaboral.ubicacion.label("ubicacion"),
            OfertaLaboral.direccion.label("direccion"),
            OfertaLaboral.estado.label("estado"),
            OfertaLaboral.descripcion.label("descripcion"),
            Empleador.foto_perfil.label("foto_perfil_empleador"),
            OfertaLaboral.fecha_creacion.label("fecha_creacion")
            ).join(Empleador,
                   OfertaLaboral.empleador_id == Empleador.id)
            .filter(OfertaLaboral.empleador_id == empleador_id,~conexiones_existentes)
        )


    def filtrar_ofertas_laborales(
      self,
      busqueda: str | None = None,
      rubro: str | None = None,
      jornada: Literal["COMPLETA", "MEDIA_JORNADA", "TEMPORAL", "A_CONVENIR"] | None = None,
      turno:  Literal["MAÑANA", "TARDE", "NOCHE", "A_CONVENIR"] | None = None,
      dias_laborales: List[str] | None = None,
      offset: int = 0,
      limit: int = 10
    ):
        """Metodo para filtrar ofertas laborales"""


        query = self.db.query(
            OfertaLaboral.id.label("id"),
            OfertaLaboral.empleador_id.label("empleador_id"),
            OfertaLaboral.titulo.label("titulo"),
            Empleador.nombre_negocio.label("nombre_negocio"),
            OfertaLaboral.ubicacion.label("ubicacion"),
            OfertaLaboral.direccion.label("direccion"),
            OfertaLaboral.descripcion.label("descripcion"),
            Empleador.foto_perfil.label("foto_perfil_empleador")
        ).join(Empleador,
               OfertaLaboral.empleador_id == Empleador.id
            ).join(Usuario,
                   Empleador.usuario_id == Usuario.id
                ).filter(
                    Usuario.estado == "ACTIVO"
                ).filter(
                    OfertaLaboral.estado =="ACTIVA"
                )

        if busqueda:
            query = query.filter(
                OfertaLaboral.titulo.ilike(f"%{busqueda}%")
            )

        if rubro:
            query = query.filter(
                OfertaLaboral.rubro == rubro
            )

        if jornada:
            query = query.filter(
                OfertaLaboral.jornada == jornada
            )

        if turno:
            query = query.filter(
                OfertaLaboral.turno == turno
            )

        if dias_laborales:
            query = query.filter(
                OfertaLaboral.dias_laborales == dias_laborales
            )

        return query.offset(offset).limit(limit).all()