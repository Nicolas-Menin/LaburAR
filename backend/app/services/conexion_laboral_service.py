from typing import Literal
from fastapi import HTTPException
from backend.app.repositories.conexion_laboral_dao import ConexionLaboralDAO
from backend.app.models.conexion_laboral import ConexionLaboral
from backend.app.models.conversacion import Conversacion
from backend.app.repositories.postulante_dao import PostulanteDAO
from backend.app.repositories.empleador_dao import EmpleadorDAO
from backend.app.repositories.oferta_laboral_dao import OfertaLaboralDAO
from backend.app.repositories.postulacion_dao import PostulacionDAO
from backend.app.repositories.conversacion_dao import ConversacionDAO

class ConexionLaboralService:
    """Service de Conexiones Laborales"""

    def __init__(self,
                conexion_laboral_dao: ConexionLaboralDAO,
                oferta_laboral_dao: OfertaLaboralDAO,
                postulante_dao: PostulanteDAO,
                empleador_dao: EmpleadorDAO,
                postulacion_dao: PostulacionDAO,
                conversacion_dao: ConversacionDAO
        ):

        self.conexion_laboral_dao = conexion_laboral_dao
        self.postulante_dao = postulante_dao
        self.empleador_dao = empleador_dao
        self.oferta_laboral_dao = oferta_laboral_dao
        self.postulacion_dao = postulacion_dao
        self.conversacion_dao = conversacion_dao


    def crear_conexion_laboral(self, usuario_id:int, oferta_id:int,postulante_id:int):
        """Metodo para crear una conexion laboral entre postulante y empleador"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "El empleador no existe")

        oferta = self.oferta_laboral_dao.buscar_por_empleador(empleador.id,oferta_id)

        if not oferta:
            raise HTTPException(404, "La oferta laboral no existe o no pertenece al empleador")

        postulante = self.postulante_dao.buscar_por_id(postulante_id)

        if not postulante:
            raise HTTPException(404, "El postulante no existe")

        conexion = self.conexion_laboral_dao.buscar_conexion_laboral(postulante.id,empleador.id,oferta_id)

        if conexion and conexion.estado != "RECHAZADA":
            raise HTTPException(409, "Ya existe una solicitud o conexion laboral")

        if conexion:
            conexion.estado = "PENDIENTE"
            return self.conexion_laboral_dao.actualizar_conexion_laboral(conexion)

        conexion_laboral = ConexionLaboral(
            postulante_id = postulante_id,
            empleador_id = empleador.id,
            oferta_id = oferta.id,
            estado = "PENDIENTE",
        )


        return self.conexion_laboral_dao.crear_conexion_laboral(conexion_laboral)

    def crear_conexion_laboral_postulacion(
        self,
        usuario_id:int,
        oferta_id:int,
        postulante_id: int,
        estado: str
        ):
        """Metodo para crear conexion laboral mediante una postulacion"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "No existe el empleador")

        oferta = self.oferta_laboral_dao.buscar_por_id(oferta_id)

        if not oferta:
            raise HTTPException(404, "La oferta laboral no exite")

        if oferta.empleador_id != empleador.id:
            raise HTTPException(403, "La oferta laboral no pertence a este empleador")


        postulacion = self.postulacion_dao.buscar_postulacion(postulante_id,oferta_id)

        if not postulacion:
            raise HTTPException(404, "No existe una postulacion para esta oferta")

        if postulacion.estado != "PENDIENTE":
            raise HTTPException(409, "La postulacion no se encuentra pendiente")

        conexion = self.conexion_laboral_dao.buscar_conexion_laboral(
            postulante_id,
            empleador.id,
            oferta.id
        )

        if conexion:

            conexion.estado = estado

            conexion_laboral = self.conexion_laboral_dao.actualizar_conexion_laboral(conexion)

        else:

            conexion_laboral = ConexionLaboral(
                postulante_id = postulante_id,
                empleador_id = empleador.id,
                oferta_id = oferta.id,
                estado = estado,
            )

            conexion_laboral = self.conexion_laboral_dao.crear_conexion_laboral(conexion_laboral)


        if conexion_laboral.estado == "ACEPTADA" and not conexion_laboral.conversacion:
            conversacion = Conversacion(
                conexion_laboral_id= conexion_laboral.id
            )

            self.conversacion_dao.crear_conversacion(conversacion)

        postulacion.estado = conexion_laboral.estado
        self.postulacion_dao.actualizar_postulacion(postulacion)

        return conexion_laboral

    def actualizar_conexion_laboral_estado(
        self,
        usuario_id:int,
        conexion_laboral_id:int,
        estado: Literal["ACEPTADA","RECHAZADA"],
        ):
        """Método para actualizar el estado de una conexión laboral."""


        conexion_laboral = self.conexion_laboral_dao.buscar_por_id(conexion_laboral_id)

        if not conexion_laboral:

            raise HTTPException(404,"La conexion laboral no existe")

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404, "El postulante no existe")

        if postulante.id != conexion_laboral.postulante_id:
            raise HTTPException(403, "La conexion no le pertenece a este postulante")

        conexion_laboral.estado = estado

        # VERIFICA SI EXISTE LA POSTULACION
        postulacion = self.postulacion_dao.buscar_postulacion(postulante.id,conexion_laboral.oferta_id)

        # SI EXISTE ENTONCES LE CAMBIA EL ESTADO YA SEA RECHAZADA O ACEPTADA Y ACTUALIZA LA POSTULACION
        if postulacion:
            postulacion.estado = conexion_laboral.estado
            self.postulacion_dao.actualizar_postulacion(postulacion)

        # VERIFICA SI EL ESTADO DE CONEXION LABORAL YA ESTE ACEPTADO
        # Y SI ES QUE POR ESA CONEXION NO HAY UNA CONVERSACION CREADA
        if conexion_laboral.estado == "ACEPTADA"  and not conexion_laboral.conversacion:
            conversacion = Conversacion(
                conexion_laboral_id= conexion_laboral_id
            )

            self.conversacion_dao.crear_conversacion(conversacion)


        return self.conexion_laboral_dao.actualizar_conexion_laboral(conexion_laboral)




    def traer_conexiones_laborales_postulante(self,usuario_id: int,offset:int, busqueda: str | None = None):
        """Metodo para traer la lista de conexiones laborales del postulante"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404, "El postulante no existe")

        return self.conexion_laboral_dao.listar_conexiones_laborales_postulante(postulante.id,busqueda,offset)


    def traer_conexiones_laborales_empleador(self,usuario_id: int,offset:int,busqueda: str | None = None):
        """"Metodo para traer la lista de conexiones laborales del empleador"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        return self.conexion_laboral_dao.listar_conexiones_laborales_empleador(empleador.id,busqueda,offset)


    def verificar_conexion_laboral_postulante(self,usuario_id: int,oferta_id:int):
        """Metodo para verificar si el postulante posee una conexion laboral"""

        postulante = self.postulante_dao.buscar_por_id(usuario_id)

        if not postulante:
            raise HTTPException(404, "El postulante no existe")

        return self.conexion_laboral_dao.obtener_conexion_laboral_postulante(postulante.id,oferta_id)

    def verificar_conexion_laboral_empleador(self,usuario_id: int,postulante_id: int, oferta_id: int | None = None):
        """Método para verificar si el empleador posee una conexión laboral"""

        empleador = self.empleador_dao.buscar_por_id(usuario_id)

        if not empleador:
            raise HTTPException(404, "No existe el empleador")

        return self.conexion_laboral_dao.obtener_conexion_laboral_empleador(postulante_id,empleador.id,oferta_id)
