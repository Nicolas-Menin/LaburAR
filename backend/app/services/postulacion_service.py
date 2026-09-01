from backend.app.models.postulacion import Postulacion
from backend.app.repositories.postulacion_dao import PostulacionDAO
from backend.app.schemas.postulacion_schemas import PostulacionCreate


class PostulacionService:
    """Service de Postulacion"""


    def __init__(self,postulacion_dao: PostulacionDAO):
        self.postulacion_dao = postulacion_dao



    def crear_postulacion(self,datos: PostulacionCreate):
        """Metodo para crear postulacion a oferta laboral"""

        postulacion = Postulacion(
            postulante_id = datos.postulante_id,
            oferta_id = datos.oferta_id,
            empleador_id = datos.empleador_id,
            estado = datos.estado
        )

        return self.postulacion_dao.crear_postulacion(postulacion)


    def listar_postulaciones_postulante(self,postulante_id: int,busqueda: str | None,offset: int):
        """Metodo para listar las postulaciones del postulante"""


        return self.postulacion_dao.filtrar_postulaciones_postulante(postulante_id,busqueda,offset)



    def listar_postulaciones_empleador(self,empleador_id: int,busqueda: str | None, offset: int,oferta_id: int | None):
        """Metodo para listar las postulaciones de ofertas laborales del empleador"""

        return self.postulacion_dao.filtrar_postulaciones_oferta_laboral(
           empleador_id,oferta_id,busqueda,offset)
