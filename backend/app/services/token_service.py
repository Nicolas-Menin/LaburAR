from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import HTTPException
from backend.app.core.config import JWT_KEY


class TokenService:
    """Service de Token"""


    def crear_token(self,payload: dict):
        """Metodo que crea el token del usuario que inicia sesion"""

        token = jwt.encode(payload,JWT_KEY,algorithm="HS256")

        return token



    def verificar_token_recuperacion(self,token: str):
        """Metodo para verificarr el token de recuperacion"""

        try:

            payload = jwt.decode(token,JWT_KEY,algorithms="HS256")



        except ExpiredSignatureError as exc:
            raise HTTPException(408, "Expiro el tiempo de autenticacion") from exc

        if payload["type"] != "password_reset":
            raise HTTPException(403,"No coincide el tipo de token")

        return payload


    def decodificar_token(self,token: str):
        """Metodo para decodifciar el token"""
        try:
            usuario = jwt.decode(token,JWT_KEY,algorithms="HS256")

        except JWTError as exc:
            raise HTTPException(401,"Token invalid") from exc
        return usuario["user"]
