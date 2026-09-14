from typing import List
from fastapi import APIRouter, Depends
from backend.app.services.oferta_laboral_service import OfertaLaboralService
from backend.app.dependencies.oferta_laboral import obtener_oferta_laboral_service
from backend.app.schemas.oferta_laboral_schemas import OfertaLaboralSearch, OfertaLaboralFiltro


#ROUTER DE OFERTA LABORAL
oferta_laboral_router = APIRouter(prefix="/oferta-laboral",tags=["Oferta Laboral"])


@oferta_laboral_router.get("/buscar-ofertas-laborales", response_model=List[OfertaLaboralSearch])
async def buscar_oferta_laborales(
    busqueda: str | None = None,
    filtros:  OfertaLaboralFiltro = Depends(),
    oferta_laboral_service: OfertaLaboralService = Depends(obtener_oferta_laboral_service)
):
    """Funcion para buscar ofertas laborales mediante filtros"""


    return oferta_laboral_service.buscar_ofertas_laborales(
        busqueda=busqueda,
        filtros=filtros
    )
