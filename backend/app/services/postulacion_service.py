from typing import Literal
from fastapi import HTTPException
from backend.app.models.postulacion import Postulacion
from backend.app.repositories.postulacion_dao import PostulacionDAO
from backend.app.repositories.oferta_laboral_dao import OfertaLaboralDAO
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.empleador_dao import EmpleadorDAO
from backend.app.repositories.conexion_laboral_dao import ConexionLaboralDAO
from backend.app.repositories.conversacion_dao import ConversacionDAO
from backend.app.models.conexion_laboral import ConexionLaboral
from backend.app.models.conversacion import Conversacion

class PostulacionService:
    """Service de Postulacion"""


    def __init__(self,postulacion_dao: PostulacionDAO,
                 oferta_laboral_dao: OfertaLaboralDAO,
                 postulante_dao: PostulanteDAO,
                 empleador_dao: EmpleadorDAO,
                 conexion_laboral_dao: ConexionLaboralDAO,
                 conversacion_dao: ConversacionDAO
                 ):
        self.postulacion_dao = postulacion_dao
        self.oferta_laboral_dao = oferta_laboral_dao
        self.postulante_dao = postulante_dao
        self.empleador_dao = empleador_dao
        self.conexion_laboral_dao = conexion_laboral_dao
        self.conversacion_dao = conversacion_dao


    def crear_postulacion(self,usuario_id:int, oferta_id: int ):
        """Metodo para crear postulacion a oferta laboral"""
        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404,"Postulante no encontrado")

        oferta = self.oferta_laboral_dao.buscar_por_id(oferta_id)

        if not oferta:
            raise HTTPException(404, "Oferta laboral no encontrada")

        postulacion = self.postulacion_dao.obtener_postulacion_por_postulante_y_oferta(
            postulante.id,
            oferta.id)

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

        if not postulante:
            raise HTTPException(404, "Postulante no encontrado")

        return  self.postulacion_dao.obtener_postulacion(
            postulante_id=postulante.id,
            oferta_id=oferta_id
        )

    def actualizar_estado_postulacion(self,usuario_id: int,
                               postulacion_id: int,
                               oferta_id:int,
                               estado: Literal["ACEPTADA", "RECHAZADA"]
                               ):


        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "Empleador no encontrador")

        postulacion = self.postulacion_dao.buscar_postulacion_empleador(empleador.id,oferta_id,postulacion_id)

        if not postulacion:
            raise HTTPException(404, "Postulacion no encontrada")

        postulante = self.postulante_dao.buscar_por_postulante_id(postulacion.postulante_id)

        if not postulante:
            raise HTTPException(404,"Postulante no encontrado")

        postulacion.estado = estado

        if postulacion.estado == "ACEPTADA":

            conexion = self.conexion_laboral_dao.buscar_conexion_laboral(
                postulante_id=postulante.id,
                empleador_id=empleador.id,
                oferta_id=oferta_id
            )
            if not conexion:

                conexion_laboral = ConexionLaboral(
                    postulante_id = postulante.id,
                    empleador_id = empleador.id,
                    oferta_id = oferta_id,
                    estado = "ACEPTADA"
                )

                self.conexion_laboral_dao.crear_conexion_laboral(conexion_laboral)

                conversacion = Conversacion(
                    conexion_laboral_id = conexion_laboral.id
                )

                self.conversacion_dao.crear_conversacion(
                    conversacion=conversacion
                )

            else:

                conexion.estado = estado

                self.conexion_laboral_dao.actualizar_conexion_laboral(
                    conexion_laboral=conexion
                )


        return self.postulacion_dao.actualizar_postulacion(postulacion)
