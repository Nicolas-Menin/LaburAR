

def test_buscar_ofertas_laborales_correctamente(client):
    response = client.get(
        "/oferta-laboral/buscar-ofertas-laborales"
    )
    print(response.json())
    assert response.status_code == 200

def test_buscar_ofertas_laborales_por_busqueda(client):

    response = client.get(
        "/oferta-laboral/buscar-ofertas-laborales",
        params={
            "busqueda": "Python"
        }
    )

    print(response.json())

    assert response.status_code == 200

def test_buscar_ofertas_laborales_por_rubro(client):

    response = client.get(
        "/oferta-laboral/buscar-ofertas-laborales",
        params={
            "rubro": "Tecnología"
        }
    )

    print(response.json())

    assert response.status_code == 200

def test_buscar_ofertas_laborales_sin_resultados(client):

    response = client.get(
        "/oferta-laboral/buscar-ofertas-laborales",
        params={
            "busqueda": "OfertaQueNoExiste123456"
        }
    )

    print(response.json())

    assert response.status_code == 200
    assert response.json() == []


def test_buscar_ofertas_laborales_por_jornada(client):

    response = client.get(
        "/oferta-laboral/buscar-ofertas-laborales",
        params={
            "jornada": "COMPLETA"
        }
    )

    print(response.json())

    assert response.status_code == 200

def test_buscar_ofertas_laborales_por_turno(client):

    response = client.get(
        "/oferta-laboral/buscar-ofertas-laborales",
        params={
            "turno": "MAÑANA"
        }
    )

    print(response.json())

    assert response.status_code == 200

def test_buscar_ofertas_laborales_por_dias(client):

    response = client.get(
        "/oferta-laboral/buscar-ofertas-laborales",
        params={"dias_laborales":["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]}
    )
    print(response.request.url)
    print(response.json())

    assert response.status_code == 200

def test_buscar_ofertas_laborales_con_filtros_combinados(client):

    response = client.get(
        "/oferta-laboral/buscar-ofertas-laborales",
        params={
            "busqueda": "Python",
            "rubro": "Tecnología",
            "jornada": "COMPLETA",
            "turno": "MAÑANA"
        }
    )

    print(response.json())

    assert response.status_code == 200

def test_buscar_ofertas_laborales_por_jornada_invalida(client):

    response = client.get(
        "/oferta-laboral/buscar-ofertas-laborales",
        params={
            "jornada": "JORNADA_INEXISTENTE"
        }
    )

    print(response.json())

    assert response.status_code == 422

def test_buscar_ofertas_laborales_por_turno_invalido(client):

    response = client.get(
        "/oferta-laboral/buscar-ofertas-laborales",
        params={
            "turno": "TURNO_INEXISTENTE"
        }
    )

    print(response.json())

    assert response.status_code == 422
