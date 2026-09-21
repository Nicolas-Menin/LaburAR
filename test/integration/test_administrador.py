def test_buscar_usuarios_postulantes_correctamente(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/administrador/buscar-usuarios",
        params={
            "filtro": "POSTULANTE"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_buscar_usuarios_empleadores_correctamente(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/administrador/buscar-usuarios",
        params={
            "filtro": "EMPLEADOR"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_buscar_usuarios_sin_token(client):

    response = client.get(
        "/administrador/buscar-usuarios",
        params={
            "filtro": "POSTULANTE"
        }
    )

    assert response.status_code == 401

def test_buscar_usuarios_usuario_no_administrador(client):
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
        "/administrador/buscar-usuarios",
        params={
            "filtro": "POSTULANTE"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401

def test_buscar_usuarios_filtro_invalido(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/administrador/buscar-usuarios",
        params={
            "filtro": "ADMINISTRADOR"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

def test_actualizar_reporte_correctamente(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/administrador/actualizar-reporte",
        params={
            "estado": "REVISADO",
            "reporte_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_actualizar_reporte_sin_token(client):

    response = client.put(
        "/administrador/actualizar-reporte",
        params={
            "estado": "REVISADO",
            "reporte_id": 1
        }
    )

    assert response.status_code == 401

def test_actualizar_reporte_usuario_no_administrador(client):
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

    response = client.put(
        "/administrador/actualizar-reporte",
        params={
            "estado": "REVISADO",
            "reporte_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401

def test_actualizar_reporte_no_encontrado(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/administrador/actualizar-reporte",
        params={
            "estado": "REVISADO",
            "reporte_id": 300
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_actualizar_reporte_estado_invalido(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/administrador/actualizar-reporte",
        params={
            "estado": "INVALIDO",
            "reporte_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422


def test_buscar_reportes_correctamente(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/administrador/buscar-reportes",
        params={
            "filtro": "REVISADO"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print(response.json())

    assert response.status_code == 200

def test_buscar_reportes_sin_token(client):
    response = client.get(
        "/administrador/buscar-reportes",
        params={
            "filtro": "REVISADO"
        }
    )

    assert response.status_code == 401

def test_buscar_reportes_usuario_no_administrador(client):
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
        "/administrador/buscar-reportes",
        params={
            "filtro": "REVISADO"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401

def test_buscar_reportes_filtro_invalido(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/administrador/buscar-reportes",
        params={
            "filtro": "INVALIDO"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

def test_buscar_reportes_con_busqueda(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/administrador/buscar-reportes",
        params={
            "filtro": "REVISADO",
            "busqueda": "Prue"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_desactivar_usuario_correctamente(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/administrador/desactivar-usuario",
        params={
            "desactivar_usuario_id": 8
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_desactivar_usuario_sin_token(client):
    response = client.put(
        "/administrador/desactivar-usuario",
        params={
            "desactivar_usuario_id": 8
        }
    )

    assert response.status_code == 401

def test_desactivar_usuario_usuario_no_administrador(client):
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

    response = client.put(
        "/administrador/desactivar-usuario",
        params={
            "desactivar_usuario_id": 8
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401

def test_desactivar_usuario_no_encontrado(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/administrador/desactivar-usuario",
        params={
            "desactivar_usuario_id": 300
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_desactivar_usuario_ya_desactivado(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/administrador/desactivar-usuario",
        params={
            "desactivar_usuario_id": 8
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

def test_banear_usuario_correctamente(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/administrador/banear-usuario",
        params={
            "banear_usuario_id": 7
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_banear_usuario_sin_token(client):
    response = client.put(
        "/administrador/banear-usuario",
        params={
            "banear_usuario_id": 7
        }
    )

    assert response.status_code == 401

def test_banear_usuario_usuario_no_administrador(client):
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

    response = client.put(
        "/administrador/banear-usuario",
        params={
            "banear_usuario_id": 7
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401

def test_banear_usuario_no_encontrado(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/administrador/banear-usuario",
        params={
            "banear_usuario_id": 999999
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_banear_usuario_ya_baneado(client):
    datos_login = {
        "email": "test.admin@example.com",
        "password": "password123"
    }

    login_response = client.post(
        "/autenticacion/login/",
        json=datos_login
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.put(
        "/administrador/banear-usuario",
        params={
            "banear_usuario_id": 7
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

