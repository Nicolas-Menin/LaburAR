from typing import Literal
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


class TokenResponse(BaseModel):
    """Contrato de respuesta de token"""
    access_token: str

    token_type: Literal["bearer"]

    rol: Literal["postulante","empleador","administrador"]

class UsuarioAdministrador(BaseModel):
    """Contrato para visualizar y gestionar usuarios por administrador"""

    usuario_id: int

    tipo: Literal["POSTULANTE", "EMPLEADOR"]

    estado: Literal["ACTIVO","DESACTIVADO","BANEADO"]

    foto_perfil: HttpUrl | None