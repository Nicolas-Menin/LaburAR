from backend.app.services.autenticacion_service import AutenticacionService


def test_password_hash_correctamente():
    service = AutenticacionService()

    password = "MiPassword123"

    password_hash = service.password_hash(password)

    assert password_hash != password
    assert isinstance(password_hash, str)
    assert service.verify_password(password, password_hash) is True


def test_verify_password_incorrecta():
    service = AutenticacionService()

    password = "MiPassword123"
    password_hash = service.password_hash(password)

    assert service.verify_password("PasswordIncorrecta", password_hash) is False