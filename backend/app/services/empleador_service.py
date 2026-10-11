from typing import Literal
from fastapi import HTTPException
from backend.app.repositories.empleador_dao import EmpleadorDAO
from backend.app.schemas.empleador_schemas import EmpleadorUpdate, EmpleadorFiltro
from backend.app.services.cloudinary_service import CloudinaryService
from backend.app.services.postulacion_service import PostulacionService
from backend.app.repositories.oferta_laboral_dao import OfertaLaboralDAO
from backend.app.schemas.oferta_laboral_schemas import OfertaLaboralCreate,OfertaLaboralUpdate
from backend.app.models.oferta_laboral import OfertaLaboral


class EmpleadorService:
    """Service de Empleador"""

    def __init__(self,
                empleador_dao:  EmpleadorDAO,
                cloudinary_service: CloudinaryService,
                postulacion_service: PostulacionService,
                oferta_laboral_dao: OfertaLaboralDAO
                ):
        self.empleador_dao = empleador_dao
        self.cloudinary_service = cloudinary_service
        self.postulacion_service = postulacion_service
        self.oferta_laboral_dao = oferta_laboral_dao

    def actualizar_empleador(
        self,
        datos: EmpleadorUpdate,
        usuario_id: int,
        ):
        """Metodo para actualizar los datos del empleador"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "Empleado no encontrado")

        if datos.nombre_negocio is not None:
            empleador.nombre_negocio = datos.nombre_negocio

        if datos.direccion is not None:
            empleador.direccion = datos.direccion

        if datos.ubicacion is not None:
            empleador.ubicacion = datos.ubicacion

        if datos.descripcion is not None:
            empleador.descripcion = datos.descripcion

        if datos.rubro is not None:
            empleador.rubro = datos.rubro

        if datos.foto_perfil is not None:
            foto_url = self.cloudinary_service.actualizar_foto_perfil(datos.foto_perfil,usuario_id)
            empleador.foto_perfil = foto_url

        return self.empleador_dao.actualizar_empleador(empleador)


    def perfil_empleador(self,usuario_id: int):
        """Metodo para mostrar perfil del empleador"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "Empleador no encontrado")

        return self.empleador_dao.perfil_empleador(empleador.id)

    def obtener_por_empleador_id(self,empleador_id:int):
        """Metodo para obtener datos de empleador mediante su id"""


        empleador = self.empleador_dao.perfil_empleador(empleador_id)

        if not empleador:
            raise HTTPException(404, "Empleador no encontrado")

        return empleador

    def buscar_por_usuario_id(self,usuario_id:int):
        """Metodo para buscar postulante mediante el id del usuario"""

        return self.empleador_dao.buscar_por_id(usuario_id)

    def buscar_empleadores(self,
                           filtros: EmpleadorFiltro,
                           busqueda: str | None = None,
                           offset: int = 0):
        """Metodo para filtrar empleadores"""


        return (self.empleador_dao.filtrar_empleadores(
                busqueda= busqueda
                        if busqueda else None,
                direccion= filtros.direccion
                        if filtros.direccion else None,
                ubicacion = filtros.ubicacion
                        if filtros.ubicacion else None,
                rubro= filtros.rubro
                        if  filtros.rubro else None,
                offset=offset
            )
        )


    def filtrar_postulaciones_oferta_laboral(self,
                                             usuario_id: int,
                                             offset: int = 0,
                                             busqueda: str | None = None,
                                             oferta_id: int | None = None
                                             ):

        """Metodo para filtrar postulaciones de oferta laboral"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "Empleador no encontrado")

        return self.postulacion_service.listar_postulaciones_empleador(
            empleador.id,
            busqueda,
            offset,
            oferta_id
        )

    def actualizar_estado_postulacion(
        self,
        usuario_id: int,
        oferta_id: int,
        postulacion_id: int,
        estado: Literal["ACEPTADA", "RECHAZADA"]
    ):
        """Metodo para actualizar el estado de postulacion de una oferta laboral"""

        return self.postulacion_service.actualizar_estado_postulacion(
            usuario_id,
            postulacion_id,
            oferta_id,
            estado
        )

    def crear_oferta_laboral(self,datos: OfertaLaboralCreate,usuario_id: int):
        """Metodo para crear oferta laboral"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "Empleador no encontrado")

        oferta_laboral = OfertaLaboral(
            titulo = datos.titulo,
            empleador_id= empleador.id,
            descripcion = datos.descripcion,
            requisitos = datos.requisitos,
            ubicacion = datos.ubicacion,
            direccion = datos.direccion,
            rubro = datos.rubro,
            estado = datos.estado,
            salario_tipo = datos.salario_tipo,
            salario_minimo = datos.salario_minimo
                if datos.salario_minimo else None,
            salario_maximo = datos.salario_maximo
                if datos.salario_maximo else None,
            jornada = datos.jornada,
            turno = datos.turno,
            dias_laborales = datos.dias_laborales
                if datos.dias_laborales else None,
            hora_inicio = datos.hora_inicio,
            hora_fin = datos.hora_fin
        )

        return self.oferta_laboral_dao.crear_oferta_laboral(oferta_laboral)

    def listar_ofertas_laborales(self,usuario_id: int,busqueda: str | None = None):

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "No existe este empleador")

        return self.oferta_laboral_dao.listar_ofertas_laborales(empleador.id,busqueda)

    def verificar_conexion_por_oferta(self,usuario_id:int, postulante_id: int):
        """Metodo que verifica  que ofertas laborales NO poseen una conexion laboral"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "No existe este empleador")


        return self.oferta_laboral_dao.verificar_conexion_por_oferta(empleador.id,postulante_id)


    def actualizar_oferta_laboral(self,datos: OfertaLaboralUpdate,oferta_laboral_id:int,usuario_id: int):
        """Metodo para actualizar los datos de la oferta laboral"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "No existe este empleador")

        oferta_laboral = self.oferta_laboral_dao.buscar_por_empleador(empleador.id,oferta_laboral_id)

        if not oferta_laboral:
            raise HTTPException(404,"No existe la oferta laboral de este empleador")

        if datos.titulo is not None:
            oferta_laboral.titulo = datos.titulo

        if datos.descripcion is not None:
            oferta_laboral.descripcion = datos.descripcion

        if datos.requisitos is not None:
            oferta_laboral.requisitos = datos.requisitos

        if datos.ubicacion is not None:
            oferta_laboral.ubicacion = datos.ubicacion

        if datos.direccion is not None:
            oferta_laboral.direccion = datos.direccion

        if datos.rubro is not None:
            oferta_laboral.rubro = datos.rubro

        if datos.estado is not None:
            oferta_laboral.estado = datos.estado

        if datos.salario_tipo is not None:
            oferta_laboral.salario_tipo = datos.salario_tipo

        if datos.salario_maximo is not None:
            oferta_laboral.salario_maximo = datos.salario_maximo

        if datos.salario_minimo is not None:
            oferta_laboral.salario_minimo = datos.salario_minimo

        if datos.dias_laborales is not None:
            oferta_laboral.dias_laborales = datos.dias_laborales

        if datos.hora_inicio is not None:
            oferta_laboral.hora_inicio = datos.hora_inicio

        if datos.hora_fin is not None:
            oferta_laboral.hora_fin = datos.hora_fin

        return self.oferta_laboral_dao.actualizar_oferta(oferta_laboral)
