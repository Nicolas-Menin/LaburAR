from unittest.mock import Mock
import pytest
from fastapi import HTTPException

from backend.app.services.postulacion_service import PostulacionService


def test_crear_postulacion_ya_existente():

    postulacion_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()

    service = PostulacionService(
        postulacion_dao=postulacion_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao
    )

    postulante = Mock()
    postulante.id = 1

    oferta = Mock()
    oferta.id = 10
    oferta.empleador_id = 5

    postulacion = Mock()
    postulacion.estado = "PENDIENTE"

    postulante_dao.buscar_por_id.return_value = postulante
    oferta_laboral_dao.buscar_por_id.return_value = oferta

    postulacion_dao.buscar_postulacion.return_value = postulacion

    with pytest.raises(HTTPException) as error:
        service.crear_postulacion(
            usuario_id=1,
            oferta_id=10
        )

    assert error.value.status_code == 409

    postulacion_dao.crear_postulacion.assert_not_called()
    postulacion_dao.actualizar_postulacion.assert_not_called()

def test_crear_postulacion_rechazada_vuelve_a_pendiente():

    postulacion_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()

    service = PostulacionService(
        postulacion_dao=postulacion_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao
    )

    postulante = Mock()
    postulante.id = 1

    oferta = Mock()
    oferta.id = 10
    oferta.empleador_id = 5

    postulacion = Mock()
    postulacion.estado = "RECHAZADA"

    postulante_dao.buscar_por_id.return_value = postulante
    oferta_laboral_dao.buscar_por_id.return_value = oferta
    postulacion_dao.obtener_postulacion.return_value = postulacion

    postulacion_dao.actualizar_postulacion.return_value = postulacion

    resultado = service.crear_postulacion(
        usuario_id=1,
        oferta_id=10
    )

    assert postulacion.estado == "PENDIENTE"
    assert resultado == postulacion

    postulacion_dao.actualizar_postulacion.assert_called_once_with(
        postulacion
    )

    postulacion_dao.crear_postulacion.assert_not_called()

def test_crear_postulacion_correctamente():

    postulacion_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()

    service = PostulacionService(
        postulacion_dao=postulacion_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao
    )

    postulante = Mock()
    postulante.id = 1

    oferta = Mock()
    oferta.id = 10
    oferta.empleador_id = 5

    postulante_dao.buscar_por_id.return_value = postulante
    oferta_laboral_dao.buscar_por_id.return_value = oferta
    postulacion_dao.obtener_postulacion.return_value = None

    postulacion_creada = Mock()
    postulacion_dao.crear_postulacion.return_value = postulacion_creada

    resultado = service.crear_postulacion(
        usuario_id=1,
        oferta_id=10
    )

    assert resultado == postulacion_creada

    postulacion_dao.crear_postulacion.assert_called_once()

    nueva_postulacion = (
        postulacion_dao.crear_postulacion.call_args.args[0]
    )

    assert nueva_postulacion.postulante_id == 1
    assert nueva_postulacion.oferta_id == 10
    assert nueva_postulacion.empleador_id == 5
    assert nueva_postulacion.estado == "PENDIENTE"

    postulacion_dao.actualizar_postulacion.assert_not_called()

def test_verificar_postulacion_existente():

    postulacion_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()

    service = PostulacionService(
        postulacion_dao=postulacion_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao
    )

    postulante = Mock()
    postulante.id = 1

    postulacion = Mock()
    postulacion.id = 20

    postulante_dao.buscar_por_id.return_value = postulante
    postulacion_dao.obtener_postulacion.return_value = postulacion

    resultado = service.verificar_postulacion(
        usuario_id=1,
        oferta_id=10
    )

    assert resultado == postulacion

def test_verificar_postulacion_inexistente():

    postulacion_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()

    service = PostulacionService(
        postulacion_dao=postulacion_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante
    postulacion_dao.obtener_postulacion.return_value = None

    resultado = service.verificar_postulacion(
        usuario_id=1,
        oferta_id=10
    )

    assert resultado is None

def test_listar_postulaciones_postulante():

    postulacion_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()

    service = PostulacionService(
        postulacion_dao=postulacion_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao
    )

    postulaciones = [Mock(), Mock()]

    postulacion_dao.filtrar_postulaciones_postulante.return_value = (
        postulaciones
    )

    resultado = service.listar_postulaciones_postulante(
        postulante_id=1,
        busqueda="programador",
        offset=0
    )

    assert resultado == postulaciones

    postulacion_dao.filtrar_postulaciones_postulante.assert_called_once_with(
        1,
        "programador",
        0
    )

def test_listar_postulaciones_empleador():

    postulacion_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()

    service = PostulacionService(
        postulacion_dao=postulacion_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao
    )

    postulaciones = [Mock(), Mock()]

    postulacion_dao.filtrar_postulaciones_oferta_laboral.return_value = (
        postulaciones
    )

    resultado = service.listar_postulaciones_empleador(
        empleador_id=5,
        busqueda="programador",
        offset=0,
        oferta_id=10
    )

    assert resultado == postulaciones

    postulacion_dao.filtrar_postulaciones_oferta_laboral.assert_called_once_with(
        5,
        10,
        "programador",
        0
    )

def test_listar_postulaciones_empleador_sin_oferta():

    postulacion_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()

    service = PostulacionService(
        postulacion_dao=postulacion_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao
    )

    postulaciones = [Mock(), Mock()]

    postulacion_dao.filtrar_postulaciones_oferta_laboral.return_value = (
        postulaciones
    )

    resultado = service.listar_postulaciones_empleador(
        empleador_id=5,
        busqueda=None,
        offset=0,
        oferta_id=None
    )

    assert resultado == postulaciones

    postulacion_dao.filtrar_postulaciones_oferta_laboral.assert_called_once_with(
        5,
        None,
        None,
        0
    )