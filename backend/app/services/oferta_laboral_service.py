from typing import List
from fastapi import HTTPException
from backend.app.repositories.oferta_laboral_dao import OfertaLaboralDAO
from backend.app.schemas.oferta_laboral_schemas import OfertaLaboralFiltro



class OfertaLaboralService:
    """Service de Oferta Laboral"""

    def __init__(self,oferta_laboral_dao: OfertaLaboralDAO):
        self.oferta_laboral_dao = oferta_laboral_dao



    def buscar_ofertas_laborales(self,
                                 filtros:OfertaLaboralFiltro,
                                 offset: int = 0,
                                 busqueda: str | None = None,
                                 dias_laborales: List[str] = None,
                                 ):
        """Metodo para buscar ofertas laborales"""

        return self.oferta_laboral_dao.filtrar_ofertas_laborales(
            busqueda= busqueda,
            rubro = filtros.rubro
                if filtros.rubro else None,
            jornada = filtros.jornada
                if filtros.jornada else None,
            turno = filtros.turno
                if filtros.turno else None,
            dias_laborales = dias_laborales
                if dias_laborales else None,
            offset=offset
        )

    def obtener_por_oferta_id(self,oferta_id:int):
        """Metodo para obtener datos de oferta laboral mediante su id"""

        oferta = self.oferta_laboral_dao.perfil_oferta_laboral(oferta_id)

        if not oferta:
            raise HTTPException(404, "Oferta laboral no encontrada")

        return oferta