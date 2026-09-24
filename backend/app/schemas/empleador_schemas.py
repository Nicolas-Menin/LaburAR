from typing import List
from pydantic import BaseModel, Field, HttpUrl,ConfigDict
from backend.app.schemas.usuario_schemas import UsuarioCreate
from backend.app.schemas.oferta_laboral_schemas import OfertaLaboralEmpleador


class EmpleadorCreate(BaseModel):
    """Contrato que crea un empleador."""

    nombre_negocio: str = Field(
        min_length=2,
        max_length=100,
        description="Nombre del negocio o empleador"
    )

    direccion: str = Field(
        min_length= 2,
        max_length=100,
        description="Direccion en donde se encuentra el negocio"
    )

    ubicacion: str = Field(
        min_length= 2,
        max_length=100,
        description="Ubicacion en donde se encuentra el negocio"
    )

    descripcion: str | None = Field(
        default=None,
        description="Descripcion del negocio o empleador"
    )

    rubro: str | None = Field(
        default=None,
        description="Rubro del negocio o empleador"
    )

    foto_perfil: HttpUrl | None = Field(
        default=None,
        description="Foto de perfil de negocio o empleador"
    )


class RegistroEmpleador(BaseModel):
    """Contrato de registro de empleador."""

    usuario: UsuarioCreate

    empleador: EmpleadorCreate


class EmpleadorUpdate(BaseModel):
    """Contrato que actualiza lod datos del empleador,"""

    nombre_negocio: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="Nombre del negocio o empleador"
    )

    direccion: str | None  = Field(
        default=None,
        min_length= 2,
        max_length=100,
        description="Direccion en donde se encuentra el negocio"
    )

    ubicacion: str | None = Field(
        default=None,
        min_length= 2,
        max_length=100,
        description="Ubicacion en donde se encuentra el negocio"
    )

    descripcion: str | None = Field(
        default=None,
        description="Descripcion del negocio o empleador"
    )

    rubro: str | None = Field(
        default=None,
        description="Rubro del negocio o empleador"
    )



class EmpleadorPerfil(BaseModel):
    """Contrato que muestra el perfil completo del empleador."""
    model_config = ConfigDict(from_attributes=True)

    id: int

    nombre_negocio: str

    direccion: str

    ubicacion: str

    descripcion: str | None = Field(
        default=None,
        description="Descripcion del negocio o empleador"
    )

    rubro: str | None = Field(
        default=None,
        description="Rubro del negocio o empleador"
    )

    foto_perfil: HttpUrl | None = Field(
        default=None,
        description="Foto de perfil de negocio o empleador"
    )

    ofertas_laborales: List[OfertaLaboralEmpleador] | None = None


class EmpleadorSearch(BaseModel):
    """Contrato  de busqueda de empleador."""

    id: int

    nombre_negocio: str

    descripcion: str | None = Field(
        default=None,
        description="Descripcion del negocio o empleador"
    )

    foto_perfil: HttpUrl | None = Field(
        default=None,
        description="Foto de perfil de negocio o empleador"
    )

class EmpleadorFiltro(BaseModel):
    """Contrato de filtro de empleadores"""

    direccion: str | None = None

    ubicacion: str | None = None

    rubro: str | None = None
