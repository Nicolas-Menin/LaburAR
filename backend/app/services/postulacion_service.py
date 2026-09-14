from fastapi import HTTPException
from backend.app.models.postulacion import Postulacion
from backend.app.repositories.postulacion_dao import PostulacionDAO
from backend.app.repositories.oferta_laboral_dao import OfertaLaboralDAO
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.empleador_dao import EmpleadorDAO
class PostulacionService:
    """Service de Postulacion"""


    def __init__(self,postulacion_dao: PostulacionDAO,
                 oferta_laboral_dao: OfertaLaboralDAO,
                 postulante_dao: PostulanteDAO,
                 empleador_dao: EmpleadorDAO
                 ):
        self.postulacion_dao = postulacion_dao
        self.oferta_laboral_dao = oferta_laboral_dao
        self.postulante_dao = postulante_dao
        self.empleador_dao = empleador_dao


    def crear_postulacion(self,usuario_id:int, oferta_id: int ):
        """Metodo para crear postulacion a oferta laboral"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        oferta = self.oferta_laboral_dao.buscar_por_id(oferta_id)

        postulacion = self.verificar_postulacion(usuario_id,oferta.id)

        if postulacion:

            if postulacion.estado != "RECHAZADA":
                raise HTTPException(409,"El postulante ya esta postulado a esta oferta laboral")

            postulacion.estado =  "PENDIENTE"

            return self.postulacion_dao.actualizar_postulacion(postulacion)

        nueva_postulacion = Postulacion(
            postulante_id = postulante.id,
            oferta_id = oferta.id,
            empleador_id = oferta.empleador_id,
            estado = "PENDIENTE"
         )

        return self.postulacion_dao.crear_postulacion(nueva_postulacion)


    def listar_postulaciones_postulante(self,postulante_id: int,busqueda: str | None,offset: int):
        """Metodo para listar las postulaciones del postulante"""


        return self.postulacion_dao.filtrar_postulaciones_postulante(postulante_id,busqueda,offset)



    def listar_postulaciones_empleador(self,empleador_id: int,busqueda: str | None, offset: int,oferta_id: int | None):
        """Metodo para listar las postulaciones de ofertas laborales del empleador"""

        return self.postulacion_dao.filtrar_postulaciones_oferta_laboral(
           empleador_id,oferta_id,busqueda,offset)


    def verificar_postulacion(self,usuario_id: int, oferta_id: int):
        """Metodo para verificar si un postulante ya esta postulado a una oferta laboral"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        return  self.postulacion_dao.buscar_postulacion(
            postulante_id=postulante.id,
            oferta_id=oferta_id
        )