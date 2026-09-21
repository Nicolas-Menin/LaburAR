
def test_obtener_perfil_empleador_correctamente(client):
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
        "/empleador/perfil-empleador",
        headers={"Authorization": f"Bearer {token}"}
    )

    print(response.json())

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_obtener_perfil_empleador_sin_token(client):
    response = client.get(
        "/empleador/perfil-empleador"
    )

    assert response.status_code == 401

def test_buscar_empleadores_sin_filtros(client):
    response = client.get(
        "/empleador/buscar-empleadores"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_buscar_empleadores_por_ubicacion(client):
    response = client.get(
        "/empleador/buscar-empleadores",
        params={"ubicacion": "Bahia Blanca"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_actualizar_empleador_correctamente(client):
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

    datos = {
        "nombre_negocio": "ABSA",
        "descripcion": "Aguaa"
    }

    response = client.put(
        "/empleador/actualizar-empleador",
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_actualizar_empleador_sin_token(client):
    datos = {
        "nombre_negocio": "Empresa de Prueba",
        "descripcion": "Descripción de prueba"
    }

    response = client.put(
        "/empleador/actualizar-empleador",
        json=datos
    )

    assert response.status_code == 401


def test_actualizar_empleador_datos_incorrectos(client):
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

    datos = {
        "nombre_negocio": 12345
    }

    response = client.put(
        "/empleador/actualizar-empleador",
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422


def test_filtrar_postulaciones_oferta_laboral_sin_filtros(client):
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
        "/empleador/filtrar-postulaciones-oferta-laboral",
        params={"offset": 0},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filtrar_postulaciones_oferta_laboral_por_oferta(client):
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
        "/empleador/filtrar-postulaciones-oferta-laboral",
        params={
            "oferta_id": 3,
            "offset": 0
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filtrar_postulaciones_oferta_laboral_por_busqueda(client):
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
        "/empleador/filtrar-postulaciones-oferta-laboral",
        params={
            "busqueda": "Backend",
            "offset": 0
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filtrar_postulaciones_oferta_laboral_sin_token(client):
    response = client.get(
        "/empleador/filtrar-postulaciones-oferta-laboral",
        params={"offset": 0}
    )

    assert response.status_code == 401

def test_actualizar_oferta_laboral_correctamente(client):
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

    datos = {
        "titulo": "Desarrollador Backend Actualizado"
    }

    response = client.put(
        "/empleador/actualizar-oferta-laboral",
        params={"oferta_laboral_id": 3},
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_actualizar_oferta_laboral_sin_token(client):
    datos = {
        "titulo": "Oferta actualizada"
    }

    response = client.put(
        "/empleador/actualizar-oferta-laboral",
        params={"oferta_laboral_id": 3},
        json=datos
    )

    assert response.status_code == 401


def test_actualizar_oferta_laboral_datos_incorrectos(client):
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

    datos = {
        "titulo": 12345
    }

    response = client.put(
        "/empleador/actualizar-oferta-laboral",
        params={"oferta_laboral_id": 3},
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422


def test_actualizar_oferta_laboral_no_encontrada(client):
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

    datos = {
        "titulo": "Oferta inexistente"
    }

    response = client.put(
        "/empleador/actualizar-oferta-laboral",
        params={"oferta_laboral_id": 999999},
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_crear_oferta_laboral_correctamente(client):

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

    datos = {
        "titulo": "Desarrollador Backend Python",
        "descripcion": "Buscamos desarrollador backend para trabajar en el desarrollo y mantenimiento de APIs.",
        "requisitos": [
            "Python",
            "FastAPI",
            "SQLAlchemy",
            "PostgreSQL"
        ],
        "ubicacion": "Bahía Blanca",
        "direccion": "Av. Colón 1200",
        "rubro": "Tecnología",
        "estado": "ACTIVA",
        "salario_tipo": "RANGO",
        "salario_minimo": 800000,
        "salario_maximo": 1200000,
        "jornada": "COMPLETA",
        "turno": "MAÑANA",
        "dias_laborales": [
            "LUNES",
            "MARTES",
            "MIERCOLES",
            "JUEVES",
            "VIERNES"
        ],
        "hora_inicio": "08:00:00",
        "hora_fin": "17:00:00"
    }

    response = client.post(
        "/empleador/crear-oferta-laboral",
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_crear_conexion_laboral_oferta_inexistente(client):
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

    response = client.post(
        "/empleador/crear-conexion-laboral",
        params={
            "oferta_laboral_id": 999999,
            "postulante_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_crear_conexion_laboral_empleador_correctamente(client):
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

    response = client.post(
        "/empleador/crear-conexion-laboral",
        params={
            "oferta_laboral_id": 3,
            "postulante_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_crear_conexion_laboral_sin_token(client):
    response = client.post(
        "/empleador/crear-conexion-laboral",
        params={
            "oferta_laboral_id": 3,
            "postulante_id": 1
        }
    )

    assert response.status_code == 401

def test_crear_conexion_laboral_postulacion_sin_token(client):
    response = client.post(
        "/empleador/crear-conexion-laboral-postulacion",
        params={
            "oferta_laboral_id": 3,
            "postulante_id": 1,
            "estado": "ACEPTADA"
        }
    )

    assert response.status_code == 401

def test_crear_conexion_laboral_postulacion_oferta_inexistente(client):
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

    response = client.post(
        "/empleador/crear-conexion-laboral-postulacion",
        params={
            "oferta_laboral_id": 999999,
            "postulante_id": 1,
            "estado": "ACEPTADA"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_crear_conexion_laboral_postulacion_estado_invalido(client):
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

    response = client.post(
        "/empleador/crear-conexion-laboral-postulacion",
        params={
            "oferta_laboral_id": 3,
            "postulante_id": 1,
            "estado": "PENDIENTE"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

def test_buscar_conexiones_laborales_sin_filtros(client):
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
        "/empleador/buscar-conexiones-laboorales",
        params={"offset": 0},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_buscar_conexiones_laborales_con_busqueda(client):
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
        "/empleador/buscar-conexiones-laboorales",
        params={
            "busqueda": "Nicolas",
            "offset": 0
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_buscar_conexiones_laborales_sin_token(client):
    response = client.get(
        "/empleador/buscar-conexiones-laboorales",
        params={"offset": 0}
    )

    assert response.status_code == 401

def test_verificar_conexion_laboral_correctamente(client):
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
        "/empleador/verificar-conexion-laboral",
        params={
            "postulante_id": 1,
            "oferta_id": 3
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_verificar_conexion_laboral_no_existente(client):
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
        "/empleador/verificar-conexion-laboral",
        params={
            "postulante_id": 300,
            "oferta_id": 300
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() is None


def test_verificar_conexion_laboral_sin_token(client):
    response = client.get(
        "/empleador/verificar-conexion-laboral",
        params={
            "postulante_id": 1,
            "oferta_id": 3
        }
    )

    assert response.status_code == 401

def test_crear_conexion_laboral_postulacion_correctamente(client):
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

    response = client.post(
        "/empleador/crear-conexion-laboral-postulacion",
        params={
            "oferta_laboral_id": 3,
            "postulante_id": 1,
            "estado": "ACEPTADA"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200