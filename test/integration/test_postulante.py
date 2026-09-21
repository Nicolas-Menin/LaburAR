
def test_obtener_perfil_postulante_correctamente(client):

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
        "/postulante/perfil",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    print(response.json())
    assert response.status_code == 200

def test_obtener_perfil_postulante_sin_token(client):

    response = client.get(
        "/postulante/perfil"
    )

    assert response.status_code == 401

def test_obtener_perfil_postulante_token_invalido(client):

    response = client.get(
        "/postulante/perfil",
        headers={
            "Authorization": "Bearer token_invalido"
        }
    )

    assert response.status_code == 401

def test_buscar_postulantes_sin_filtros(client):
    response = client.get(
        "/postulante/buscar-postulantes"
    )

    print(response.json())

    assert response.status_code == 200

def test_buscar_postulantes_por_ubicacion(client):
    response = client.get(
        "/postulante/buscar-postulantes",
        params={
            "ubicacion": "Punta Alta"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_buscar_postulantes_por_habilidades(client):
    response = client.get(
        "/postulante/buscar-postulantes",
        params={
            "habilidades": ["Python",]
        }
    )

    print(response.json())

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_buscar_postulantes_disponibilidad_invalida(client):
    response = client.get(
        "/postulante/buscar-postulantes",
        params={
            "disponibilidad": "DISPONIBILIDAD_INVALIDA"
        }
    )

    assert response.status_code == 422

def test_actualizar_postulante_correctamente(client):
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

    datos = {
        "nombre": "Nicolas",
        "apellido": "Menin",
        "ubicacion": "Punta Alta",
        "descripcion_personal": "Descripción actualizada",
        "disponibilidad": "JORNADA_COMPLETA"
    }

    response = client.put(
        "/postulante/actualizar-postulante",
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_actualizar_postulante_sin_token(client):
    datos = {
        "nombre": "Nicolas"
    }

    response = client.put(
        "/postulante/actualizar-postulante",
        json=datos
    )

    assert response.status_code == 401

def test_actualizar_postulante_disponibilidad_invalida(client):

    datos = {
        "disponibilidad": "DISPONIBILIDAD_INVALIDA"
    }

    response = client.put(
        "/postulante/actualizar-postulante",
        json=datos,
        headers={"Authorization": "Bearer token_invalido"}
    )

    assert response.status_code == 422

def test_crear_estudio_postulante_correctamente(client):

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

    datos = {
        "titulo": "Ingeniero de Software",
        "institucion": "Universwidad del Sur",
        "fecha_inicio": "2023-02-02",
        "estado": "EN_CURSO",
        "nivel": "UNIVERSITARIO"
    }

    response = client.post(
        "/postulante/crear-estudio",
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_crear_estudio_postulante_sin_token(client):

    datos = {
            "titulo": "Ingeniero de Software",
            "institucion": "Universwidad del Sur",
            "fecha_inicio": "2023-02-02",
            "estado": "EN_CURSO",
            "nivel": "UNIVERSITARIO"
        }

    response = client.post(
        "/postulante/crear-estudio",
        json=datos,
        headers={"Authorization": "Sin-token"}
    )

    assert response.status_code == 401

def test_crear_estudio_postulante_datos_incorrectos(client):

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

    datos = {
        "titulo": "Ingeniero Mecanico",
        "institucion": "Universwidad del Sur",
        "fecha_inicio": "2023-02-02",
        "estado": "EN_CURSO",
        "nivel": "JARDIN"
    }

    response = client.post(
        "/postulante/crear-estudio",
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

def test_actualizar_estudio_postulante_correctamente(client):


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

    datos = {
        "fecha_fin": "2026-04-22",
        "estado": "NO_TERMINADO"
    }


    response = client.put("/postulante/actualizar-estudio",
                params= {"estudio_id": 1},
                json= datos,
                headers= {"Authorization": f"Bearer {token}"}
    )


    assert response.status_code == 200

def test_actualizar_estudio_postulante_sin_token(client):

    datos = {
        "fecha_fin": "2026-06-22",
        "estado": "NO_TERMINADO"
    }

    response = client.put(
        "/postulante/actualizar-estudio",
        json= datos,
    )

    assert response.status_code == 401

def test_actualizar_estudio_postulante_datos_incorrectos(client):


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

    datos = {
        "fecha_fin": "2026-04-22",
        "estado": "NO_LO_TERMINO_MASSSS"
    }


    response = client.put("/postulante/actualizar-estudio",
                params= {"estudio_id": 1},
                json= datos,
                headers= {"Authorization": f"Bearer {token}"}
    )


    assert response.status_code == 422

def test_eliminar_estudio_postulante_correctamente(client):

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

    response = client.delete(
        "postulante/eliminar-estudio",
        params={"estudio_id": 1},
        headers= {"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_eliminar_estudio_postulante_no_encontrado(client):

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

    response = client.delete(
        "/postulante/eliminar-estudio",
        params={"estudio_id": 300},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_crear_experiencia_laboral_postulante_correctamente(client):

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

    datos = {
        "empresa": "Tech Solutions",
        "puesto": "Desarrollador Backend",
        "fecha_inicio": "2024-02-01",
        "area": "Sistemas"
    }

    response = client.post(
        "/postulante/crear-experiencia-laboral",
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_crear_experiencia_laboral_postulante_sin_token(client):

    datos = {
        "empresa": "Tech Solutions",
        "puesto": "Desarrollador Backend",
        "fecha_inicio": "2024-02-01",
        "area": "Sistemas"
    }

    response = client.post(
        "/postulante/crear-experiencia-laboral",
        json=datos
    )

    assert response.status_code == 401

def test_crear_experiencia_laboral_postulante_datos_incorrectos(client):

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

    datos = {
        "empresa": "Tech Solutions",
        "puesto": "Desarrollador Backend",
        "fecha_inicio": "2024-02-01",
        "area": "Sistemas",
        "fecha_fin": "FECHA_INVALIDA"
    }

    response = client.post(
        "/postulante/crear-experiencia-laboral",
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

def test_actualizar_experiencia_laboral_postulante_correctamente(client):

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

    datos = {
        "puesto": "Desarrollador Backend Senior",
        "area": "Sistemas"
    }

    response = client.put(
        "/postulante/actualizar-experiencia-laboral",
        params={"experiencia_laboral_id": 1},
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_actualizar_experiencia_laboral_postulante_sin_token(client):

    datos = {
        "puesto": "Desarrollador Backend Senior",
        "area": "Sistemas"
    }

    response = client.put(
        "/postulante/actualizar-experiencia-laboral",
        params={"experiencia_laboral_id": 1},
        json=datos
    )

    assert response.status_code == 401

def test_actualizar_experiencia_laboral_postulante_datos_incorrectos(client):

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

    datos = {
        "fecha_inicio": "FECHA_INVALIDA"
    }

    response = client.put(
        "/postulante/actualizar-experiencia-laboral",
        params={"experiencia_laboral_id": 1},
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

def test_eliminar_experiencia_laboral_postulante_correctamente(client):

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

    response = client.delete(
        "/postulante/eliminar-experiencia-laboral",
        params={"experiencia_laboral_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_eliminar_experiencia_laboral_postulante_no_encontrada(client):

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

    response = client.delete(
        "/postulante/eliminar-experiencia-laboral",
        params={"experiencia_laboral_id": 999999},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_crear_habilidad_postulante_correctamente(client):

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

    datos = {
        "nombre": "Python"
    }

    response = client.post(
        "/postulante/crear-habilidad",
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_crear_habilidad_postulante_sin_token(client):

    datos = {
        "nombre": "Python"
    }

    response = client.post(
        "/postulante/crear-habilidad",
        json=datos
    )

    assert response.status_code == 401

def test_crear_habilidad_postulante_datos_incorrectos(client):

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

    datos = {
        "nombre": "P"
    }

    response = client.post(
        "/postulante/crear-habilidad",
        json=datos,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

def test_eliminar_habilidad_postulante_correctamente(client):

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

    response = client.delete(
        "/postulante/eliminar-habilidad",
        params={"habilidad_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_eliminar_habilidad_postulante_no_encontrada(client):

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

    response = client.delete(
        "/postulante/eliminar-habilidad",
        params={"habilidad_id": 300},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_crear_postulacion_postulante_correctamente(client):

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

    response = client.post(
        "/postulante/crear-postulacion",
        params={"oferta_id": 3},
        headers={"Authorization": f"Bearer {token}"}
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200

def test_crear_postulacion_sin_token(client):

    response = client.post(
        "/postulante/crear-postulacion",
        params={"oferta_id": 3}
    )

    assert response.status_code == 401

def test_crear_postulacion_oferta_inexistente(client):

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

    response = client.post(
        "/postulante/crear-postulacion",
        params={"oferta_id": 999999},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_crear_postulacion_duplicada(client):

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

    response = client.post(
        "/postulante/crear-postulacion",
        params={"oferta_id": 3},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 409

def test_verificar_postulacion_correctamente(client):

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
        "/postulante/verificar-postulacion",
        params={"oferta_id": 3},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_verificar_postulacion_sin_token(client):

    response = client.get(
        "/postulante/verificar-postulacion",
        params={"oferta_id": 3}
    )

    assert response.status_code == 401


def test_verificar_postulacion_oferta_inexistente(client):

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
        "/postulante/verificar-postulacion",
        params={"oferta_id": 300},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_mis_postulaciones_correctamente(client):

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
        "/postulante/mis-postulaciones",
        params={"offset": 0},
        headers={"Authorization": f"Bearer {token}"}
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200

def test_mis_postulaciones_sin_token(client):

    response = client.get(
        "/postulante/mis-postulaciones",
        params={"offset": 0},
    )

    assert response.status_code == 401

def test_mis_postulaciones_por_busqueda(client):

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
        "/postulante/mis-postulaciones",
        params={
            "offset": 0,
            "busqueda": "Backend"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_actualizar_solicitud_laboral_correctamente(client):
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

    response = client.put(
        "/postulante/actualizar-solicitud-laboral",
        params={
            "conexion_laboral_id": 1,
            "estado": "ACEPTADA"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_actualizar_solicitud_laboral_sin_token(client):
    response = client.put(
        "/postulante/actualizar-solicitud-laboral",
        params={
            "conexion_laboral_id": 1,
            "estado": "RECHAZADA"
        }
    )

    assert response.status_code == 401

def test_actualizar_solicitud_laboral_inexistente(client):
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

    response = client.put(
        "/postulante/actualizar-solicitud-laboral",
        params={
            "conexion_laboral_id": 300,
            "estado": "ACEPTADA"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_verificar_conexion_laboral_correctamente(client):
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
        "/postulante/verificar-conexion-laboral",
        params={"oferta_id": 3},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_verificar_conexion_laboral_sin_token(client):
    response = client.get(
        "/postulante/verificar-conexion-laboral",
        params={"oferta_id": 3}
    )

    assert response.status_code == 401

def test_buscar_solicitudes_laborales_correctamente(client):
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
        "/postulante/buscar-solicitudes-laborales",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

def test_buscar_solicitudes_laborales_sin_token(client):
    response = client.get(
        "/postulante/buscar-solicitudes-laborales"
    )

    assert response.status_code == 401


def test_buscar_solicitudes_laborales_con_busqueda(client):
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
        "/postulante/buscar-solicitudes-laborales",
        params={"busqueda": "Backend"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200