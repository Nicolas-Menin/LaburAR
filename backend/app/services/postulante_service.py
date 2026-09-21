from typing import List
from fastapi import HTTPException
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.estudio_dao import EstudiosDAO
from backend.app.repositories.experiencia_laboral_dao import ExperienciaLaboralDAO
from backend.app.repositories.habilidad_dao import HabilidadDAO
from backend.app.models.habilidad import Habilidad
from backend.app.schemas.habilidad_schemas import HabilidadCreate
from backend.app.schemas.postulante_schemas import PostulanteUpdate,PostulanteFiltro
from backend.app.schemas.estudio_schemas import EstudioCreate,EstudioUpdate
from backend.app.services.cloudinary_service import CloudinaryService
from backend.app.models.estudio import Estudio
from backend.app.models.experiencia_laboral import ExperienciaLaboral
from backend.app.schemas.experiencia_laboral_schemas import ExperienciaLaboralCreate, ExperienciaLaboralUpdate
from backend.app.services.postulacion_service import PostulacionService

class PostulanteService:
    """Service de Postulante"""


    def __init__(self,
                postulante_dao: PostulanteDAO,
                estudio_dao: EstudiosDAO,
                experiencia_laboral_dao: ExperienciaLaboralDAO,
                habilidad_dao: HabilidadDAO,
                cloudinary_service: CloudinaryService,
                postulacion_service: PostulacionService
        ):

        self.postulante_dao = postulante_dao
        self.estudio_dao = estudio_dao
        self.experiencia_laboral_dao = experiencia_laboral_dao
        self.habilidad_dao = habilidad_dao
        self.cloudinary_service = cloudinary_service
        self.postulacion_service = postulacion_service



    def actualizar_postulante(
            self,
            datos: PostulanteUpdate,
            usuario_id: int,
            foto_perfil: str | None = None,
            cv: str | None = None
            ):
        """Metodo para actualizar los datos del postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404, "Postulante no encontrado")

        if datos.nombre is not None:
            postulante.nombre = datos.nombre

        if datos.apellido is not None:
            postulante.apellido = datos.apellido

        if datos.ubicacion is not None:
            postulante.ubicacion = datos.ubicacion

        if datos.descripcion_personal is not None:
            postulante.descripcion_personal = datos.descripcion_personal

        if  foto_perfil is not None:
            url_foto_perfil = self.cloudinary_service.actualizar_foto_perfil(foto_perfil,usuario_id)
            postulante.foto_perfil = url_foto_perfil

        if cv is not None:
            url_cv = self.cloudinary_service.actualizar_cv_postulante(cv,usuario_id)
            postulante.cv_url = url_cv

        if datos.disponibilidad is not None:
            postulante.disponibilidad = datos.disponibilidad


        return self.postulante_dao.actualizar_postulante(postulante)


    def perfil_postulante(self, usuario_id: int):
        """Metodo para mostrar perfil del postulante"""

        return self.postulante_dao.buscar_por_id(usuario_id)


    def buscar_postulantes(self,
                           filtro:PostulanteFiltro,
                           habilidades: List[str],
                           offset: int = 0
                           ):
        """Metodo para filtrar postulantes"""

        return (self.postulante_dao.filtrar_postulantes(
            busqueda=filtro.busqueda
                if filtro.busqueda else None,
            ubicacion=  filtro.ubicacion
                if filtro.ubicacion else None,
            estudios = filtro.estudios
                if filtro.estudios else None,
            habilidades = habilidades
                if habilidades else None,
            experiencias_laborales = filtro.experiencias_laborales
                if filtro.experiencias_laborales else None,
            disponibilidad = filtro.disponibilidad
                if filtro.disponibilidad else None,
            offset=offset
            )
        )


    def crear_estudio(self,datos: EstudioCreate,usuario_id: int):
        """Metodo para crear un estudio del postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404, "Postulante no encontrado")

        estudio = Estudio(
            postulante_id = postulante.id,
            titulo = datos.titulo,
            institucion = datos.institucion,
            fecha_inicio = datos.fecha_inicio,
            fecha_fin = datos.fecha_fin,
            estado = datos.estado,
            nivel = datos.nivel
        )

        return self.estudio_dao.crear_estudio(estudio)

    def actualizar_estudio(
            self,
            datos: EstudioUpdate,
            usuario_id: int,
            estudio_id: int
            ):
        """Metodo para actualizar estudio del postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404,"Postulante no encontrado")

        estudio = self.estudio_dao.buscar_estudio_id(estudio_id,postulante.id)

        if not estudio:
            raise HTTPException(404,"Estudio no encontrado")

        if datos.titulo is not None:
            estudio.titulo = datos.titulo

        if datos.institucion is not None:
            estudio.institucion = datos.institucion

        if datos.fecha_inicio is not None:
            estudio.fecha_inicio = datos.fecha_inicio

        if datos.fecha_fin is not None:
            estudio.fecha_fin = datos.fecha_fin

        if datos.nivel is not None:
            estudio.nivel = datos.nivel

        if datos.estado is not None:
            estudio.estado = datos.estado

        return self.estudio_dao.actualizar_estudio(estudio)

    def eliminar_estudio(self, estudio_id: int,usuario_id:int):
        """Metodo para eliminar estudio del postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404,"Postulante no encontrado")

        estudio = self.estudio_dao.buscar_estudio_id(estudio_id,postulante.id)

        if not estudio:
            raise HTTPException(404,"Estudio no encontrado")

        return self.estudio_dao.eliminar_estudio(estudio)

    def crear_experiencia_laboral(self, datos: ExperienciaLaboralCreate,usuario_id: int):
        """Metodo para crear experiencia laboral del postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404,"Postulante no encontrado")

        experiencia_laboral = ExperienciaLaboral(
            postulante_id = postulante.id,
            empresa = datos.empresa,
            puesto = datos.puesto,
            fecha_inicio = datos.fecha_inicio,
            descripcion= datos.descripcion,
            area  = datos.area
        )

        return self.experiencia_laboral_dao.crear_experiencia_laboral(experiencia_laboral)

    def actualizar_experiencia_laboral(
        self,
        datos: ExperienciaLaboralUpdate,
        usuario_id: int,
        experiencia_laboral_id: int
        ):
        """Metodo para actualizar experiencia laboral del postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404,"Postulante no encontrado")

        experiencia_laboral = self.experiencia_laboral_dao.buscar_por_id(experiencia_laboral_id,postulante.id)

        if not experiencia_laboral:
            raise HTTPException(404,"Experiencia laboral no encontrado")

        if postulante.id != experiencia_laboral.postulante_id:
            raise HTTPException(403,"Permiso denegado: No coinciden los id del postulante")

        if datos.empresa is not None:
            experiencia_laboral.empresa = datos.empresa

        if datos.puesto is not None:
            experiencia_laboral.puesto = datos.puesto

        if datos.fecha_inicio is not None:
            experiencia_laboral.fecha_inicio = datos.fecha_inicio

        if datos.fecha_fin is not None:
            experiencia_laboral.fecha_fin = datos.fecha_fin

        if datos.descripcion is not None:
            experiencia_laboral.descripcion = datos.descripcion

        if datos.area is not None:
            experiencia_laboral.area = datos.area


        return self.experiencia_laboral_dao.actualizar_experiencia_laboral(experiencia_laboral)


    def eliminar_experiencia_laboral(
        self,
        experiencia_laboral_id: int,
        usuario_id: int
        ):
        """Metodo para eliminar experiencia laboral del postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404,"Postulante no encontrado")

        experiencia_laboral = self.experiencia_laboral_dao.buscar_por_id(
            experiencia_laboral_id,postulante.id)

        if not experiencia_laboral:
            raise HTTPException(404,"Experiencia laboral no encontrada")

        return self.experiencia_laboral_dao.eliminar_experiencia_laboral(experiencia_laboral)


    def crear_habilidad(self, datos: HabilidadCreate,usuario_id: int):
        """Metodo para crear habilidad de postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404, "Postulante no encontrado")

        habilidad = Habilidad(
            postulante_id= postulante.id,
            nombre = datos.nombre
        )

        return self.habilidad_dao.crear_habilidad(habilidad)

    def eliminar_habilidad(
        self,
        habilidad_id: int,
        usuario_id: int
        ):
        """Metodo para eliminar una habilidad del postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404, "Postulante no encontrado")

        habilidad = self.habilidad_dao.buscar_por_id(habilidad_id,postulante.id)

        if not habilidad:
            raise HTTPException(404, "Habilidad no encontrada")

        return self.habilidad_dao.eliminar_habilidad(habilidad)



    def filtrar_postulaciones(self,
                              usuario_id:int,
                              offset: int,
                              busqueda: str | None = None):
        """Metodo para mostrar las postulaciones del postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404, "Postulante no encontrado")

        return self.postulacion_service.listar_postulaciones_postulante(postulante.id,busqueda,offset)
