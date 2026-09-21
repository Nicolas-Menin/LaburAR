from unittest.mock import Mock
import pytest
from fastapi import HTTPException

from backend.app.services.conexion_laboral_service import ConexionLaboralService


def test_crear_conexion_laboral_empleador_inexistente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.crear_conexion_laboral(
            usuario_id=1,
            oferta_id=10,
            postulante_id=5
        )

    assert error.value.status_code == 404

    oferta_laboral_dao.buscar_por_empleador.assert_not_called()
    postulante_dao.buscar_por_id.assert_not_called()
    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()


def test_crear_conexion_laboral_oferta_inexistente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_empleador.return_value = None

    with pytest.raises(HTTPException) as error:
        service.crear_conexion_laboral(
            usuario_id=1,
            oferta_id=10,
            postulante_id=5
        )

    assert error.value.status_code == 404

    oferta_laboral_dao.buscar_por_empleador.assert_called_once_with(
        1,
        10
    )

    postulante_dao.buscar_por_id.assert_not_called()
    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()


def test_crear_conexion_laboral_postulante_inexistente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()
    oferta.id = 10

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_empleador.return_value = oferta
    postulante_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.crear_conexion_laboral(
            usuario_id=1,
            oferta_id=10,
            postulante_id=5
        )

    assert error.value.status_code == 404

    postulante_dao.buscar_por_id.assert_called_once_with(5)

    conexion_laboral_dao.buscar_conexion_laboral.assert_not_called()
    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()

def test_crear_conexion_laboral_ya_existente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()
    oferta.id = 10

    postulante = Mock()
    postulante.id = 5

    conexion = Mock()
    conexion.estado = "PENDIENTE"

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_empleador.return_value = oferta
    postulante_dao.buscar_por_id.return_value = postulante
    conexion_laboral_dao.buscar_conexion_laboral.return_value = conexion

    with pytest.raises(HTTPException) as error:
        service.crear_conexion_laboral(
            usuario_id=1,
            oferta_id=10,
            postulante_id=5
        )

    assert error.value.status_code == 409

    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()
    conexion_laboral_dao.actualizar_conexion_laboral.assert_not_called()

def test_crear_conexion_laboral_rechazada_vuelve_a_pendiente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()
    oferta.id = 10

    postulante = Mock()
    postulante.id = 5

    conexion = Mock()
    conexion.estado = "RECHAZADA"

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_empleador.return_value = oferta
    postulante_dao.buscar_por_id.return_value = postulante
    conexion_laboral_dao.buscar_conexion_laboral.return_value = conexion

    conexion_laboral_dao.actualizar_conexion_laboral.return_value = conexion

    resultado = service.crear_conexion_laboral(
        usuario_id=1,
        oferta_id=10,
        postulante_id=5
    )

    assert conexion.estado == "PENDIENTE"
    assert resultado == conexion

    conexion_laboral_dao.actualizar_conexion_laboral.assert_called_once_with(
        conexion
    )

    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()

def test_crear_conexion_laboral_correctamente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()
    oferta.id = 10

    postulante = Mock()
    postulante.id = 5

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_empleador.return_value = oferta
    postulante_dao.buscar_por_id.return_value = postulante

    # No existe una conexion previa
    conexion_laboral_dao.buscar_conexion_laboral.return_value = None

    conexion_creada = Mock()
    conexion_laboral_dao.crear_conexion_laboral.return_value = conexion_creada

    resultado = service.crear_conexion_laboral(
        usuario_id=1,
        oferta_id=10,
        postulante_id=5
    )

    assert resultado == conexion_creada

    conexion_laboral_dao.crear_conexion_laboral.assert_called_once()

    conexion = conexion_laboral_dao.crear_conexion_laboral.call_args.args[0]

    assert conexion.postulante_id == 5
    assert conexion.empleador_id == 1
    assert conexion.oferta_id == 10
    assert conexion.estado == "PENDIENTE"

    conexion_laboral_dao.actualizar_conexion_laboral.assert_not_called()

def test_crear_conexion_laboral_postulacion_empleador_inexistente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.crear_conexion_laboral_postulacion(
            usuario_id=1,
            oferta_id=10,
            postulante_id=5,
            estado="ACEPTADA"
        )

    assert error.value.status_code == 404

    oferta_laboral_dao.buscar_por_id.assert_not_called()
    postulacion_dao.buscar_postulacion.assert_not_called()
    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()


def test_crear_conexion_laboral_postulacion_oferta_inexistente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.crear_conexion_laboral_postulacion(
            usuario_id=1,
            oferta_id=10,
            postulante_id=5,
            estado="ACEPTADA"
        )

    assert error.value.status_code == 404

    postulacion_dao.buscar_postulacion.assert_not_called()
    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()

def test_crear_conexion_laboral_postulacion_oferta_otro_empleador():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()
    oferta.id = 10
    oferta.empleador_id = 2

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_id.return_value = oferta

    with pytest.raises(HTTPException) as error:
        service.crear_conexion_laboral_postulacion(
            usuario_id=1,
            oferta_id=10,
            postulante_id=5,
            estado="ACEPTADA"
        )

    assert error.value.status_code == 403

    postulacion_dao.buscar_postulacion.assert_not_called()
    conexion_laboral_dao.buscar_conexion_laboral.assert_not_called()
    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()

def test_crear_conexion_laboral_postulacion_inexistente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()
    oferta.id = 10
    oferta.empleador_id = 1

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_id.return_value = oferta
    postulacion_dao.buscar_postulacion.return_value = None

    with pytest.raises(HTTPException) as error:
        service.crear_conexion_laboral_postulacion(
            usuario_id=1,
            oferta_id=10,
            postulante_id=5,
            estado="ACEPTADA"
        )

    assert error.value.status_code == 404

    conexion_laboral_dao.buscar_conexion_laboral.assert_not_called()
    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()

def test_crear_conexion_laboral_postulacion_no_pendiente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()
    oferta.id = 10
    oferta.empleador_id = 1

    postulacion = Mock()
    postulacion.estado = "RECHAZADA"

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_id.return_value = oferta
    postulacion_dao.buscar_postulacion.return_value = postulacion

    with pytest.raises(HTTPException) as error:
        service.crear_conexion_laboral_postulacion(
            usuario_id=1,
            oferta_id=10,
            postulante_id=5,
            estado="ACEPTADA"
        )

    assert error.value.status_code == 409

    conexion_laboral_dao.buscar_conexion_laboral.assert_not_called()
    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()

def test_crear_conexion_laboral_postulacion_conexion_existente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()
    oferta.id = 10
    oferta.empleador_id = 1

    postulacion = Mock()
    postulacion.estado = "PENDIENTE"

    conexion = Mock()
    conexion.estado = "PENDIENTE"

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_id.return_value = oferta
    postulacion_dao.buscar_postulacion.return_value = postulacion
    conexion_laboral_dao.buscar_conexion_laboral.return_value = conexion
    conexion_laboral_dao.actualizar_conexion_laboral.return_value = conexion

    resultado = service.crear_conexion_laboral_postulacion(
        usuario_id=1,
        oferta_id=10,
        postulante_id=5,
        estado="ACEPTADA"
    )

    assert conexion.estado == "ACEPTADA"
    assert resultado == conexion

    conexion_laboral_dao.actualizar_conexion_laboral.assert_called_once_with(
        conexion
    )

    conexion_laboral_dao.crear_conexion_laboral.assert_not_called()

def test_crear_conexion_laboral_postulacion_sin_conexion():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()
    oferta.id = 10
    oferta.empleador_id = 1

    postulacion = Mock()
    postulacion.estado = "PENDIENTE"

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_id.return_value = oferta
    postulacion_dao.buscar_postulacion.return_value = postulacion

    # No existe una conexión previa
    conexion_laboral_dao.buscar_conexion_laboral.return_value = None

    conexion_creada = Mock()
    conexion_laboral_dao.crear_conexion_laboral.return_value = conexion_creada

    resultado = service.crear_conexion_laboral_postulacion(
        usuario_id=1,
        oferta_id=10,
        postulante_id=5,
        estado="PENDIENTE"
    )

    assert resultado == conexion_creada

    conexion_laboral_dao.crear_conexion_laboral.assert_called_once()

    conexion = conexion_laboral_dao.crear_conexion_laboral.call_args.args[0]

    assert conexion.postulante_id == 5
    assert conexion.empleador_id == 1
    assert conexion.oferta_id == 10
    assert conexion.estado == "PENDIENTE"

    conexion_laboral_dao.actualizar_conexion_laboral.assert_not_called()
    conversacion_dao.crear_conversacion.assert_not_called()

def test_crear_conexion_laboral_postulacion_aceptada_crea_conversacion():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()
    oferta.id = 10
    oferta.empleador_id = 1

    postulacion = Mock()
    postulacion.estado = "PENDIENTE"

    conexion = Mock()
    conexion.id = 20
    conexion.estado = "PENDIENTE"
    conexion.conversacion = None

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_id.return_value = oferta
    postulacion_dao.buscar_postulacion.return_value = postulacion
    conexion_laboral_dao.buscar_conexion_laboral.return_value = conexion
    conexion_laboral_dao.actualizar_conexion_laboral.return_value = conexion

    resultado = service.crear_conexion_laboral_postulacion(
        usuario_id=1,
        oferta_id=10,
        postulante_id=5,
        estado="ACEPTADA"
    )

    assert resultado == conexion
    assert conexion.estado == "ACEPTADA"

    conversacion_dao.crear_conversacion.assert_called_once()

    conversacion = conversacion_dao.crear_conversacion.call_args.args[0]

    assert conversacion.conexion_laboral_id == 20

def test_actualizar_conexion_laboral_estado_conexion_inexistente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    conexion_laboral_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.actualizar_conexion_laboral_estado(
            usuario_id=1,
            conexion_laboral_id=20,
            estado="ACEPTADA"
        )

    assert error.value.status_code == 404

    postulante_dao.buscar_por_id.assert_not_called()
    conexion_laboral_dao.actualizar_conexion_laboral.assert_not_called()
    conversacion_dao.crear_conversacion.assert_not_called()

def test_actualizar_conexion_laboral_estado_postulante_inexistente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    conexion = Mock()
    conexion.postulante_id = 5

    conexion_laboral_dao.buscar_por_id.return_value = conexion
    postulante_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.actualizar_conexion_laboral_estado(
            usuario_id=1,
            conexion_laboral_id=20,
            estado="ACEPTADA"
        )

    assert error.value.status_code == 404

    conexion_laboral_dao.actualizar_conexion_laboral.assert_not_called()
    conversacion_dao.crear_conversacion.assert_not_called()

def test_actualizar_conexion_laboral_estado_conexion_no_pertenece():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    conexion = Mock()
    conexion.postulante_id = 5

    postulante = Mock()
    postulante.id = 10

    conexion_laboral_dao.buscar_por_id.return_value = conexion
    postulante_dao.buscar_por_id.return_value = postulante

    with pytest.raises(HTTPException) as error:
        service.actualizar_conexion_laboral_estado(
            usuario_id=10,
            conexion_laboral_id=20,
            estado="ACEPTADA"
        )

    assert error.value.status_code == 403

    conexion_laboral_dao.actualizar_conexion_laboral.assert_not_called()
    conversacion_dao.crear_conversacion.assert_not_called()

def test_actualizar_conexion_laboral_estado_correctamente():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    conexion = Mock()
    conexion.id = 20
    conexion.postulante_id = 5
    conexion.estado = "PENDIENTE"
    conexion.conversacion = None

    postulante = Mock()
    postulante.id = 5

    conexion_laboral_dao.buscar_por_id.return_value = conexion
    postulante_dao.buscar_por_id.return_value = postulante
    conexion_laboral_dao.actualizar_conexion_laboral.return_value = conexion

    resultado = service.actualizar_conexion_laboral_estado(
        usuario_id=5,
        conexion_laboral_id=20,
        estado="RECHAZADA"
    )

    assert conexion.estado == "RECHAZADA"
    assert resultado == conexion

    conexion_laboral_dao.actualizar_conexion_laboral.assert_called_once_with(
        conexion
    )

    conversacion_dao.crear_conversacion.assert_not_called()

def test_actualizar_conexion_laboral_estado_aceptada_crea_conversacion():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    conexion = Mock()
    conexion.id = 20
    conexion.postulante_id = 5
    conexion.estado = "PENDIENTE"
    conexion.conversacion = None

    postulante = Mock()
    postulante.id = 5

    conexion_laboral_dao.buscar_por_id.return_value = conexion
    postulante_dao.buscar_por_id.return_value = postulante
    conexion_laboral_dao.actualizar_conexion_laboral.return_value = conexion

    resultado = service.actualizar_conexion_laboral_estado(
        usuario_id=5,
        conexion_laboral_id=20,
        estado="ACEPTADA"
    )

    assert conexion.estado == "ACEPTADA"
    assert resultado == conexion

    conversacion_dao.crear_conversacion.assert_called_once()

    conversacion = conversacion_dao.crear_conversacion.call_args.args[0]

    assert conversacion.conexion_laboral_id == 20

    conexion_laboral_dao.actualizar_conexion_laboral.assert_called_once_with(
        conexion
    )

def test_traer_conexiones_laborales_postulante():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    postulante = Mock()
    postulante.id = 5

    resultado_esperado = ["conexion1", "conexion2"]

    postulante_dao.buscar_por_id.return_value = postulante
    conexion_laboral_dao.listar_conexiones_laborales_postulante.return_value = (
        resultado_esperado
    )

    resultado = service.traer_conexiones_laborales_postulante(
        usuario_id=1,
        offset=10,
        busqueda="programador"
    )

    assert resultado == resultado_esperado

    conexion_laboral_dao.listar_conexiones_laborales_postulante.assert_called_once_with(
        5,
        "programador",
        10
    )

def test_traer_conexiones_laborales_empleador():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 8

    resultado_esperado = ["conexion1", "conexion2"]

    empleador_dao.buscar_por_id.return_value = empleador
    conexion_laboral_dao.listar_conexiones_laborales_empleador.return_value = (
        resultado_esperado
    )

    resultado = service.traer_conexiones_laborales_empleador(
        usuario_id=2,
        offset=20,
        busqueda="electricista"
    )

    assert resultado == resultado_esperado

    conexion_laboral_dao.listar_conexiones_laborales_empleador.assert_called_once_with(
        8,
        "electricista",
        20
    )

def verificar_conexion_laboral_postulante(self, usuario_id: int, oferta_id: int):
    postulante = self.postulante_dao.buscar_por_id(usuario_id)
    return self.conexion_laboral_dao.buscar_conexion_laboral_postulante(
        postulante.id,
        oferta_id
    )

def test_verificar_conexion_laboral_postulante():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    postulante = Mock()
    postulante.id = 5

    conexion_esperada = Mock()

    postulante_dao.buscar_por_id.return_value = postulante

    conexion_laboral_dao.obtener_conexion_laboral_postulante.return_value = (
        conexion_esperada
    )

    resultado = service.verificar_conexion_laboral_postulante(
        usuario_id=1,
        oferta_id=10
    )

    assert resultado == conexion_esperada
def test_verificar_conexion_laboral_empleador():

    conexion_laboral_dao = Mock()
    oferta_laboral_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    postulacion_dao = Mock()
    conversacion_dao = Mock()

    service = ConexionLaboralService(
        conexion_laboral_dao=conexion_laboral_dao,
        oferta_laboral_dao=oferta_laboral_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        postulacion_dao=postulacion_dao,
        conversacion_dao=conversacion_dao
    )

    empleador = Mock()
    empleador.id = 8

    conexion_esperada = Mock()

    empleador_dao.buscar_por_id.return_value = empleador

    conexion_laboral_dao.obtener_conexion_laboral_empleador.return_value = (
        conexion_esperada
    )

    resultado = service.verificar_conexion_laboral_empleador(
        usuario_id=2,
        postulante_id=5,
        oferta_id=10
    )

    assert resultado == conexion_esperada