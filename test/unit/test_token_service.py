from datetime import datetime, timezone, timedelta

import pytest
from backend.app.services.token_service import TokenService
from backend.app.core.config import JWT_KEY
from jose import jwt
from fastapi import HTTPException

def test_crear_token_correctamente():
    service = TokenService()

    payload = {
        "user": 1,
        "rol": "POSTULANTE"
    }

    token = service.crear_token(payload)

    assert isinstance(token, str)

    resultado = jwt.decode(
        token,
        JWT_KEY,
        algorithms="HS256"
    )

    assert resultado["user"] == 1
    assert resultado["rol"] == "POSTULANTE"


def test_verificar_token_recuperacion_correctamente():
    service = TokenService()

    payload = {
        "user": 1,
        "type": "password_reset",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
    }

    token = service.crear_token(payload)

    resultado = service.verificar_token_recuperacion(token)

    assert resultado["user"] == 1
    assert resultado["type"] == "password_reset"


def test_verificar_token_recuperacion_tipo_incorrecto():
    service = TokenService()

    payload = {
        "user": 1,
        "type": "login",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
    }

    token = service.crear_token(payload)

    with pytest.raises(Exception) as excepcion:
        service.verificar_token_recuperacion(token)

    assert excepcion.value.status_code == 403


def test_verificar_token_recuperacion_expirado():
    service = TokenService()

    payload = {
        "user": 1,
        "type": "password_reset",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=10)
    }

    token = service.crear_token(payload)

    with pytest.raises(HTTPException) as excepcion:
        service.verificar_token_recuperacion(token)

    assert excepcion.value.status_code == 408


def test_decodificar_token_correctamente():
    service = TokenService()

    payload = {
        "user": 25,
        "rol": "EMPLEADOR"
    }

    token = service.crear_token(payload)

    resultado = service.decodificar_token(token)

    assert resultado == 25