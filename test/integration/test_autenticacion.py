from unittest.mock import patch




def test_registrar_postulante_correctamente(client):

    datos = {
        "usuario": {
            "email": "manuel.prueba@example.com",
            "password": "manuel123"
        },
        "postulante": {
            "nombre": "Manuel",
            "apellido": "Ferran",
            "ubicacion": "Monte hermoso",
            "descripcion_personal": "Tecnico electrisista con experencia en todo",
            "disponibilidad": "JORNADA_COMPLETA"
        }
    }

    response = client.post(
        "/autenticacion/registrar-postulante",
        json=datos
    )
    print(response.json())

    assert response.status_code == 200

def test_registrar_postulante_email_existente(client):

    datos = {
        "usuario": {
            "email": "test.postulante@example.com",
            "password": "password123"
        },
        "postulante": {
            "nombre": "Otro",
            "apellido": "Usuario",
            "ubicacion": "Punta Alta",
            "disponibilidad": "JORNADA_COMPLETA"
        }
    }

    response = client.post(
        "/autenticacion/registrar-postulante",
        json=datos
    )

    assert response.status_code == 409

def test_registrar_postulante_password_invalida(client):

    datos = {
        "usuario": {
            "email": "otro.postulante@example.com",
            "password": "123"
        },
        "postulante": {
            "nombre": "Nicolas",
            "apellido": "Menin",
            "ubicacion": "Punta Alta",
            "disponibilidad": "JORNADA_COMPLETA"
        }
    }

    response = client.post(
        "/autenticacion/registrar-postulante",
        json=datos
    )

    assert response.status_code == 422

def test_iniciar_sesion_correctamente(client):

    datos = {
        "email": "test.postulante@example.com",
        "password": "password123"
    }

    response = client.post(
        "/autenticacion/login/",
        json=datos
    )

    assert response.status_code == 200

    datos_respuesta = response.json()

    assert "access_token" in datos_respuesta
    assert "token_type" in datos_respuesta
    assert "rol" in datos_respuesta

def test_iniciar_sesion_password_incorrecta(client):

    datos = {
        "email": "test.postulante@example.com",
        "password": "password_incorrecta"
    }

    response = client.post(
        "/autenticacion/login/",
        json=datos
    )

    assert response.status_code == 401

def test_iniciar_sesion_email_inexistente(client):

    datos = {
        "email": "usuario_que_no_existe@example.com",
        "password": "password123"
    }

    response = client.post(
        "/autenticacion/login/",
        json=datos
    )

    assert response.status_code == 401

def test_iniciar_sesion_usuario_baneado(client):


    datos_login = {
            "email": "test.postulante@example.com",
            "password": "password123"
        }

    response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    print(response.json())

    assert response.status_code == 403


def test_registrar_empleador_correctamente(client):

    datos = {
        "usuario": {
            "email": "test.empleador@example.com",
            "password": "password123"
        },
        "empleador": {
            "nombre_negocio": "Comercio Test",
            "direccion": "Calle Falsa 123",
            "ubicacion": "Punta Alta",
            "descripcion": "Negocio utilizado para pruebas",
            "rubro": "Comercio"
        }
    }

    response = client.post(
        "/autenticacion/registrar-empleador",
        json=datos
    )

    assert response.status_code == 200

def test_registrar_empleador_email_existente(client):

    datos = {
        "usuario": {
            "email": "test.empleador@example.com",
            "password": "password123"
        },
        "empleador": {
            "nombre_negocio": "Otro Comercio",
            "direccion": "Otra Calle 456",
            "ubicacion": "Punta Alta"
        }
    }

    response = client.post(
        "/autenticacion/registrar-empleador",
        json=datos
    )

    assert response.status_code == 409

def test_recuperar_contrasena_email_existente(client):

    datos = {
        "email": "test.postulante@example.com"
    }

    with patch(
        "backend.app.services.brevo_service.BrevoService.enviar_email_recuperacion_contrasena"
    ) as brevo_mock:

        brevo_mock.return_value = {
            "message": "Email enviado correctamente"
        }

        response = client.post(
            "/autenticacion/resetear-contraseña",
            json=datos
        )

    assert response.status_code == 200

    brevo_mock.assert_called_once()

def test_recuperar_contrasena_email_inexistente(client):

    datos = {
        "email": "usuario_inexistente@example.com"
    }

    response = client.post(
        "/autenticacion/resetear-contraseña",
        json=datos
    )

    assert response.status_code == 404

def test_recuperar_contrasena_email_invalido(client):

    datos = {
        "email": "email_invalido"
    }

    response = client.post(
        "/autenticacion/resetear-contraseña",
        json=datos
    )

    assert response.status_code == 422