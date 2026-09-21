from unittest.mock import Mock

from backend.app.services.oferta_laboral_service import OfertaLaboralService


def test_buscar_ofertas_laborales_con_filtros():

    oferta_laboral_dao = Mock()

    service = OfertaLaboralService(
        oferta_laboral_dao=oferta_laboral_dao
    )

    filtros = Mock()
    filtros.rubro = "Tecnologia"
    filtros.jornada = "Jornada completa"
    filtros.turno = "Mañana"

    dias_laborales = ["Lunes", "Martes"]

    resultado_esperado = ["oferta1", "oferta2"]

    oferta_laboral_dao.filtrar_ofertas_laborales.return_value = resultado_esperado

    resultado = service.buscar_ofertas_laborales(
        filtros=filtros,
        busqueda="programador",
        dias_laborales=dias_laborales
    )

    assert resultado == resultado_esperado

    oferta_laboral_dao.filtrar_ofertas_laborales.assert_called_once_with(
        busqueda="programador",
        rubro="Tecnologia",
        jornada="Jornada completa",
        turno="Mañana",
        dias_laborales=["Lunes", "Martes"],
        offset=0
    )


def test_buscar_ofertas_laborales_sin_filtros():

    oferta_laboral_dao = Mock()

    service = OfertaLaboralService(
        oferta_laboral_dao=oferta_laboral_dao
    )

    filtros = Mock()
    filtros.rubro = None
    filtros.jornada = None
    filtros.turno = None

    resultado_esperado = []

    oferta_laboral_dao.filtrar_ofertas_laborales.return_value = resultado_esperado

    resultado = service.buscar_ofertas_laborales(
        filtros=filtros
    )

    assert resultado == resultado_esperado

    oferta_laboral_dao.filtrar_ofertas_laborales.assert_called_once_with(
        busqueda=None,
        rubro=None,
        jornada=None,
        turno=None,
        dias_laborales=None,
        offset=0
    )