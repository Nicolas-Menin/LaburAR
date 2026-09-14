from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.db.base import Base
from backend.app.db.session import engine
from backend.app.core.config import API_URL
from backend.app.routers.administrador_router import administrador_router
from backend.app.routers.autenticacion_router import autenticacion_router
from backend.app.routers.empleador_router import empleador_router
from backend.app.routers.mensaje_router import mensaje_router
from backend.app.routers.oferta_laboral_router import oferta_laboral_router
from backend.app.routers.postulante_router import postulante_router
from backend.app.routers.reporte_router import reporte_router
from backend.app.routers.conversacion_router import conversacion_router

# DECORADOR PARA MANEJAR LOS ARRANQUES Y CIERRE DE LA APP
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Funcion para manejar el arranque de la app"""

    try:

        Base.metadata.create_all(engine)
        print("app iniciando")
        yield

    finally:
        print("app cerrandose.")

# API DE LA APP LaburAR
laburar_api = FastAPI(
    title="LaburAR API",
    version = "1.0.0",
    lifespan=lifespan
)

# MIDDLEWARE DE LA API (PARA ACEPTAR METODOS HTTP DE UN ORIGEN ESPECIFICO)
laburar_api.add_middleware(
    CORSMiddleware,
    allow_origins=API_URL,
    allow_methods =["*"],
    allow_headers=["*"]
)

#INCLUIMOS LOS ROUTERS CREADOS
laburar_api.include_router(administrador_router)
laburar_api.include_router(autenticacion_router)
laburar_api.include_router(empleador_router)
laburar_api.include_router(mensaje_router)
laburar_api.include_router(oferta_laboral_router)
laburar_api.include_router(postulante_router)
laburar_api.include_router(reporte_router)
laburar_api.include_router(conversacion_router)
