def test_crear_reporte_correctamente(client):
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

    datos_reporte = {
        "motivo": "Prueba",
        "descripcion": "Reporte creado para realizar pruebas"
    }

    response = client.post(
        "/reporte/crear-reporte",
        params={
            "usuario_reportado_id": 1
        },
        json=datos_reporte,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
