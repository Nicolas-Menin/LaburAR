from typing import Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class UsuarioCreate(BaseModel):
    """Contrato donde se crea el usuario"""

    email: EmailStr = Field(
        description="Correo electronico de usuario"
    )

    password: str = Field(
        min_length=8,
        max_length=100,
        description="Contraseña del usuario"
    )

class UsuarioLogin(BaseModel):
    """Contrato donde el usuario inicia sesion"""

    email: EmailStr = Field(
        description="Correo electronico de usuario"
    )

    password: str = Field(
        min_length=8,
        max_length=100,
        description="Contraseña del usuario"
    )

class UsuarioEmail(BaseModel):
    """Contrato para restablecer contraseña mediante email"""

    email: EmailStr

class UsuarioResetPassword(BaseModel):
    """Contrato para restablecer contraseña"""

    password: int = Field(
         min_length=8,
         max_length=100,
         description="Nueva contraseña de usuario"
    )

class TokenResponse(BaseModel):
    """Contrato de respuesta de token"""
    access_token: str

    token_type: Literal["Bearer"]

    rol: Literal["POSTULANTE","EMPLEADOR","ADMINISTRADOR"]

class UsuarioAdministrador(BaseModel):
    """Contrato para visualizar y gestionar usuarios por administrador"""

    usuario_id: int

    postulante_id: int | None = None

    empleador_id: int | None = None

    nombre_postulante: str | None = None

    apellido_postulante: str | None = None

    nombre_negocio: str | None = None

    rol: Literal["POSTULANTE", "EMPLEADOR"]

    estado: Literal["ACTIVO","DESACTIVADO","BANEADO"]

    fecha_creacion: datetime

    foto_perfil: HttpUrl | None = None

