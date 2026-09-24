
def test_listar_mensajes_correctamente(client):

    response = client.get(
        "/mensajes/listar-mensajes/1"
    )

    print(response.json())

    assert response.status_code == 200

def test_actualizar_estado_mensajes_correctamente(client):

    datos = {
        "id_conversacion": 1,
        "usuario_id": 1
    }

    response = client.put(
        "/mensajes/actualizar-estado-mensajes",
        json=datos
    )

    print(response.json())

    assert response.status_code == 200

def test_verificar_mensajes_no_leidos_correctamente(client):

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
        "/mensajes/mensajes-no-leidos",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print(response.json())

    assert response.status_code == 200

def test_enviar_mensaje_a_empleador(client):

    datos_login_postulante = {
        "email": "test.postulante@example.com",
        "password": "password123"
    }

    login_postulante = client.post(
        "/autenticacion/login/",
        json=datos_login_postulante
    )

    assert login_postulante.status_code == 200

    token_postulante = login_postulante.json()["access_token"]

    datos_login_empleador = {
        "email": "test.empleador@example.com",
        "password": "password123"
    }

    login_empleador = client.post(
        "/autenticacion/login/",
        json=datos_login_empleador
    )

    assert login_empleador.status_code == 200

    token_empleador = login_empleador.json()["access_token"]

    with client.websocket_connect(f"/mensajes/1?token={token_postulante}") as websocket_postulante:

        with client.websocket_connect(f"/mensajes/1?token={token_empleador}") as websocket_empleador:

            datos = {
                "contenido": "Hola"
            }

            websocket_postulante.send_json(datos)

            mensaje = websocket_empleador.receive_json()

            print(mensaje)

            assert mensaje["contenido"] == "Hola"
            assert mensaje["leido"] is False

def test_enviar_mensaje_a_postulante(client):

    datos_login_postulante = {
        "email": "test.postulante@example.com",
        "password": "password123"
    }

    login_postulante = client.post(
        "/autenticacion/login/",
        json=datos_login_postulante
    )

    assert login_postulante.status_code == 200

    token_postulante = login_postulante.json()["access_token"]

    datos_login_empleador = {
        "email": "test.empleador@example.com",
        "password": "password123"
    }

    login_empleador = client.post(
        "/autenticacion/login/",
        json=datos_login_empleador
    )

    assert login_empleador.status_code == 200

    token_empleador = login_empleador.json()["access_token"]

    with client.websocket_connect(f"/mensajes/1?token={token_empleador}") as websocket_empleador:

        with client.websocket_connect(f"/mensajes/1?token={token_postulante}") as websocket_postulante:

            datos = {
                "contenido": "Hola postulante"
            }

            websocket_empleador.send_json(datos)

            mensaje = websocket_postulante.receive_json()

            assert mensaje["contenido"] == "Hola postulante"
            assert mensaje["leido"] is False

def test_verificar_mensajes_no_leidos_con_mensaje(client):

    datos_login_empleador = {
        "email": "test.empleador@example.com",
        "password": "password123"
    }

    login_empleador = client.post(
        "/autenticacion/login/",
        json=datos_login_empleador
    )

    assert login_empleador.status_code == 200

    token_empleador = login_empleador.json()["access_token"]

    datos_login_postulante = {
        "email": "test.postulante@example.com",
        "password": "password123"
    }

    login_postulante = client.post(
        "/autenticacion/login/",
        json=datos_login_postulante
    )

    assert login_postulante.status_code == 200

    token_postulante = login_postulante.json()["access_token"]

    with client.websocket_connect(f"/mensajes/1?token={token_empleador}") as websocket_empleador:

        with client.websocket_connect(f"/mensajes/1?token={token_postulante}") as websocket_postulante:

            datos = {
                "contenido": "Mensaje sin leer"
            }

            websocket_empleador.send_json(datos)

            mensaje = websocket_postulante.receive_json()

            print(mensaje)

    response = client.get(
        "/mensajes/mensajes-no-leidos",
        headers={
            "Authorization": f"Bearer {token_postulante}"
        }
    )

    print(response.json())

    assert response.status_code == 200
    assert response.json()["cantidad_mensajes_no_leidos"] > 0