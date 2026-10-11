from typing import List
from fastapi import APIRouter, Depends,Query
from backend.app.services.oferta_laboral_service import OfertaLaboralService
from backend.app.dependencies.oferta_laboral import obtener_oferta_laboral_service
from backend.app.schemas.oferta_laboral_schemas import OfertaLaboralSearch, OfertaLaboralFiltro,OfertaLaboralPerfil


#ROUTER DE OFERTA LABORAL
oferta_laboral_router = APIRouter(prefix="/oferta-laboral",tags=["Oferta Laboral"])


@oferta_laboral_router.get("/buscar-ofertas-laborales", response_model=List[OfertaLaboralSearch])
async def buscar_oferta_laborales(
    busqueda: str | None = None,
    filtros: OfertaLaboralFiltro = Depends(),
    dias_laborales: List[str] | None = Query(default=None),
    offset: int = 0,
    oferta_laboral_service: OfertaLaboralService = Depends(obtener_oferta_laboral_service)
):
    """Funcion para buscar ofertas laborales mediante filtros"""

    return oferta_laboral_service.buscar_ofertas_laborales(
        offset=offset,
        busqueda=busqueda,
        filtros=filtros,
        dias_laborales=dias_laborales
    )

@oferta_laboral_router.get("/{oferta_laboral_id}",response_model=OfertaLaboralPerfil)
async def obtener_oferta_laboral_por_id(
    oferta_laboral_id: int,
    oferta_laboral_service: OfertaLaboralService = Depends(obtener_oferta_laboral_service)
):
    """Funcion para obtener el detalle de una oferta laboral por su id"""

    return oferta_laboral_service.obtener_por_oferta_id(oferta_laboral_id)