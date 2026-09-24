from typing import Literal, List
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from backend.app.schemas.usuario_schemas import UsuarioCreate
from backend.app.schemas.habilidad_schemas import HabilidadPerfil
from backend.app.schemas.estudio_schemas import EstudioPerfil
from backend.app.schemas.experiencia_laboral_schemas import ExperienciaLaboralPerfil

class PostulanteCreate(BaseModel):
    """Contrato que crea un postulante"""

    nombre: str = Field(
        min_length=2,
        max_length=50,
        description="Nombre de postulante"
    )

    apellido: str = Field(
        min_length=2,
        max_length=50,
        description="Apellido de postulante"
        )

    ubicacion: str = Field(
        min_length=2,
        max_length=100,
        description="Ubicacion del postulante"
    )

    descripcion_personal: str | None = Field(
        default=None,
        description="Descripcion personal del postulante"
    )

    foto_perfil: HttpUrl | None = Field(
        default=None,
        description="Foto de perfil de postulante"
    )

    cv_url: HttpUrl | None = Field(
        default=None,
        description="Curriculum vitae de postulante"
    )

    disponibilidad: Literal["JORNADA_COMPLETA","MEDIA_JORNADA",
                            "FINES_SEMANA","A_CONVENIR"] = Field(
                                description="Disponibilidad laboral del postulante"
                            )


class RegistroPostulante(BaseModel):
    """Contrato de registro de postulante y de usuario"""

    usuario: UsuarioCreate

    postulante: PostulanteCreate


class PostulanteUpdate(BaseModel):
    """Contrato que actualiza los datos del postulante"""

    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        description="Nombre de postulante"
    )

    apellido: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        description="Apellido de postulante"
    )

    ubicacion: str | None = Field(
        default=None,
        max_length=100,
        description="Ubicacion del postulante"
    )

    descripcion_personal: str | None = Field(
        default=None,
        description="Descripcion personal del postulante"
    )

    disponibilidad:  Literal["JORNADA_COMPLETA","MEDIA_JORNADA",
                            "FINES_SEMANA","A_CONVENIR"] | None = Field(
                                default=None,
                                description="Disponibilidad laboral del postulante"
                            )

class PostulantePerfil(BaseModel):
    """Contrato que muestra el perfil completo del postulante."""
    model_config = ConfigDict(from_attributes=True)

    id: int

    nombre: str

    apellido: str

    ubicacion: str

    descripcion_personal: str | None = Field(
        default=None,
        description="Descripcion personal del postulante"
    )

    foto_perfil: HttpUrl | None = Field(
        default=None,
        description="Foto de perfil de postulante"
    )

    habilidades: List[HabilidadPerfil]  | None = None

    estudios: List[EstudioPerfil] | None = None

    experiencias_laborales: List[ExperienciaLaboralPerfil] | None = None

    disponibilidad:  Literal[
        "JORNADA_COMPLETA",
        "MEDIA_JORNADA",
        "FINES_SEMANA",
        "A_CONVENIR"
    ]


class PostulanteSearch(BaseModel):
    """Contrato de busqueda de postulante"""
    id: int

    nombre: str

    apellido: str

    descripcion_personal: str | None = Field(
        default=None,
        description="Descripcion personal del postulante"
    )

    foto_perfil: HttpUrl | None = Field(
            default=None,
            description="Foto de perfil de postulante"
        )

class PostulanteFiltro(BaseModel):
    """Contrato de filtro de postulantes"""

    busqueda: str | None = None

    ubicacion: str | None = None

    estudios: str | None = None

    experiencias_laborales: str | None = None

    disponibilidad:  Literal[
        "JORNADA_COMPLETA",
        "MEDIA_JORNADA",
        "FINES_SEMANA",
        "A_CONVENIR"
    ] | None = None