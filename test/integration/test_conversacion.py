def test_traer_conversaciones_postulante_correctamente(client):

    datos_login = {
        "email": "test.postulante@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/conversacion/traer-conversaciones-postulante",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print(response.json())

    assert response.status_code == 200

def test_traer_conversaciones_empleador_correctamente(client):

    datos_login = {
        "email": "test.empleador@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/conversacion/traer-conversaciones-empleador",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print(response.json())

    assert response.status_code == 200