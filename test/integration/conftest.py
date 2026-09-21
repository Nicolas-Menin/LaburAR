import pytest
from fastapi.testclient import TestClient

from backend.app.main import laburar_api
from backend.app.db.session import SessionLocal
from backend.app.dependencies.database import obtener_sesion_bd

@pytest.fixture
def obtener_bd():
    db = SessionLocal()


    try:

        yield db

    finally:
        db.rollback()
        db.close()





@pytest.fixture
def client(obtener_bd):

    laburar_api.dependency_overrides[obtener_sesion_bd] = lambda: obtener_bd

    with TestClient(laburar_api) as test_client:
        yield test_client

    laburar_api.dependency_overrides.clear()
