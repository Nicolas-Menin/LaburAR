from backend.app.repositories.conexion_laboral_dao import ConexionLaboralDAO
from backend.app.schemas.conexion_laboral_schemas import ConexionLaboralCreate
from backend.app.models.conexion_laboral import ConexionLaboral



class ConexionLaboralService:
    """Service de las conexiones laborales entre postulante y empleador"""

    def __init__(self,
                conexion_laboral_dao: ConexionLaboralDAO
        ):

        self.conexion_laboral_dao = conexion_laboral_dao


    def crear_conexion_laboral(self, datos: ConexionLaboralCreate):
        """Metodo para crear una conexion laboral entre postulante y empleador"""

        conexion_laboral = ConexionLaboral(
            postulante_id = datos.postulante_id,
            empleador_id = datos.empleador_id,
            oferta_id = datos.oferta_id,
            tipo = datos.tipo,
            estado = datos.estado,
            fecha_conexion = datos.fecha_conexion
        )


        return self.conexion_laboral_dao.crear_conexion_laboral_postulante(conexion_laboral)


    def traer_conexiones_laborales_postulante(self,id_postulante: int, busqueda: str | None = None):
        """Metodo para traer la lista de conexiones laborales del postulante"""


        return self.conexion_laboral_dao.listar_conexiones_laborales_postulante(id_postulante,busqueda)


    def traer_conexiones_laborales_empleador(self,id_empleador: int,busqueda: str | None = None):
        """"Metodo para traer la lista de conexiones laborales del empleador"""

        return self.conexion_laboral_dao.listar_conexiones_laborales_empleador(id_empleador,busqueda)
