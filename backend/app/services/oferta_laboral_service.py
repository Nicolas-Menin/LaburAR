from backend.app.repositories.oferta_laboral_dao import OfertaLaboralDAO
from backend.app.schemas.oferta_laboral_schemas import OfertaLaboralFiltro



class OfertaLaboralService:


    def __init__(self,oferta_laboral_dao: OfertaLaboralDAO):
        self.oferta_laboral_dao = oferta_laboral_dao



    def buscar_ofertas_laborales(self, datos:OfertaLaboralFiltro):
        """Metodo para buscar ofertas laborales"""

        return self.oferta_laboral_dao.filtrar_ofertas_laborales(
            busqueda= datos.busqueda
                if datos.busqueda else None,
            rubro = datos.rubro
                if datos.rubro else None,
            jornada = datos.jornada
                if datos.jornada else None,
            turno = datos.turno
                if datos.turno else None,
            dias_laborales = datos.dias_laborales
                if datos.dias_laborales else None
        )
