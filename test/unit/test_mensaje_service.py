from unittest.mock import Mock, patch

from backend.app.services.mensaje_service import MensajeService


def test_crear_mensaje_correctamente():

    mensaje_dao = Mock()

    mensaje_service = MensajeService(
        mensaje_dao=mensaje_dao
    )

    datos = Mock()
    datos.conversacion_id = 1
    datos.remitente_id = 2
    datos.contenido = "Hola, ¿cómo estás?"

    mensaje_creado = Mock()

    mensaje_dao.crear_mensaje.return_value = mensaje_creado

    with patch("backend.app.services.mensaje_service.Mensaje"):

        resultado = mensaje_service.crear_mensaje(datos)

    assert resultado == mensaje_creado


def test_listar_mensajes_correctamente():

    mensaje_dao = Mock()

    mensaje_service = MensajeService(
        mensaje_dao=mensaje_dao
    )

    mensajes = [
        Mock(),
        Mock()
    ]

    mensaje_dao.listar_mensajes.return_value = mensajes

    resultado = mensaje_service.listar_mensajes(
        conversacion_id=1
    )

    assert resultado == {
        "mensajes": mensajes
    }


def test_actualizar_estados_mensajes_correctamente():

    mensaje_dao = Mock()

    mensaje_service = MensajeService(
        mensaje_dao=mensaje_dao
    )

    mensaje_no_leido = Mock()
    mensaje_no_leido.remitente_id = 2
    mensaje_no_leido.leido = False

    mensaje_propio = Mock()
    mensaje_propio.remitente_id = 1
    mensaje_propio.leido = False

    mensaje_dao.listar_mensajes.return_value = [
        mensaje_no_leido,
        mensaje_propio
    ]

    mensajes_actualizados = Mock()

    mensaje_dao.actualizar_estados_mensajes.return_value = mensajes_actualizados

    datos = Mock()
    datos.id_conversacion = 10
    datos.usuario_id = 1

    resultado = mensaje_service.actualizar_estados_mensajes(datos)

    assert mensaje_no_leido.leido is True
    assert mensaje_propio.leido is False
    assert resultado == mensajes_actualizados


def test_existe_mensajes_no_leidos_correctamente():

    mensaje_dao = Mock()

    mensaje_service = MensajeService(
        mensaje_dao=mensaje_dao
    )

    mensajes = [
        Mock(),
        Mock(),
        Mock()
    ]

    mensaje_dao.existe_mensajes_no_leidos.return_value = mensajes

    resultado = mensaje_service.existe_mensajes_no_leidos(
        usuario_id=1
    )

    assert resultado == {
        "cantidad_mensajes_no_leidos": 3
    }