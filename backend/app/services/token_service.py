from jose import jwt
from fastapi import HTTPException
from backend.app.core.config import JWT_KEY
from datetime import datetime,timezone


class TokenService:



    def crear_token(self,payload: dict):
        """Metodo que crea el token del usuario que inicia sesion"""

        token = jwt.encode(payload,JWT_KEY,algorithm="HS256")

        return token



    def verificar_token_recuperacion(self,token: str):
        """Metodo para verificarr el token de recuperacion"""

        payload = jwt.decode(token,JWT_KEY,algorithms="HS256")

        if payload["type"] != "password_reset":
            raise HTTPException(403,"No coincide el tipo de token")

        if payload["exp"] < datetime.now(timezone.utc):
            raise HTTPException(408, "Expiro el tiempo de autenticacion")

