import pytest
from fastapi import HTTPException
from unittest.mock import Mock


from backend.app.services.usuario_service import UsuarioService

def test_iniciar_sesion_usuario_inexistente():

    usuario_dao = Mock()
    usuario_dao.buscar_por_email.return_value = None


    postulante_dao = Mock()
    empleador_dao = Mock()
    autenticacion_service = Mock()
    token_service = Mock()
    brevo_service = Mock()

    usuario_service = UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )

    with pytest.raises(HTTPException) as error:
        usuario_service.iniciar_sesion(
            email="usuario@correo.com",
            password="123456"
        )

    assert error.value.status_code == 401

def test_iniciar_sesion_password_incorrecta():

    usuario_dao = Mock()

    usuario = Mock()
    usuario.id = 1
    usuario.password_hash = "hash_de_prueba"
    usuario.rol = "POSTULANTE"

    usuario_dao.buscar_por_email.return_value = usuario

    postulante_dao = Mock()
    empleador_dao = Mock()

    autenticacion_service = Mock()
    autenticacion_service.verify_password.return_value = False

    token_service = Mock()
    brevo_service = Mock()

    usuario_service = UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )

    with pytest.raises(HTTPException) as error:
        usuario_service.iniciar_sesion(
            email="usuario@correo.com",
            password="123456"
        )

    assert error.value.status_code == 401

def test_iniciar_sesion_correctamente():

    usuario_dao = Mock()

    usuario = Mock()
    usuario.id = 1
    usuario.password_hash = "hash_de_prueba"
    usuario.rol = "POSTULANTE"

    usuario_dao.buscar_por_email.return_value = usuario

    postulante_dao = Mock()
    empleador_dao = Mock()

    autenticacion_service = Mock()
    autenticacion_service.verify_password.return_value = True

    token_service = Mock()
    token_service.crear_token.return_value = "token_de_prueba"

    brevo_service = Mock()

    usuario_service = UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )

    resultado = usuario_service.iniciar_sesion(
        email="usuario@correo.com",
        password="123456"
    )

    assert resultado["access_token"] == "token_de_prueba"
    assert resultado["token_type"] == "Bearer"
    assert resultado["rol"] == "POSTULANTE"

def test_registrar_postulante_email_existente():

    usuario_dao = Mock()

    usuario_existente = Mock()
    usuario_dao.buscar_por_email.return_value = usuario_existente

    postulante_dao = Mock()
    empleador_dao = Mock()
    autenticacion_service = Mock()
    token_service = Mock()
    brevo_service = Mock()

    usuario_service = UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )

    datos = Mock()
    datos.usuario.email = "usuario@correo.com"

    with pytest.raises(HTTPException) as error:
        usuario_service.registrar_postulante(datos)

    assert error.value.status_code == 409

def test_registrar_postulante_correctamente():

    usuario_dao = Mock()
    usuario_dao.buscar_por_email.return_value = None

    postulante_dao = Mock()

    autenticacion_service = Mock()
    autenticacion_service.password_hash.return_value = "hash_de_prueba"

    empleador_dao = Mock()
    token_service = Mock()
    brevo_service = Mock()

    usuario_service = UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )

    datos = Mock()

    datos.usuario.email = "usuario@correo.com"
    datos.usuario.password = "123456"

    datos.postulante.nombre = "Nicolas"
    datos.postulante.apellido = "Menin"
    datos.postulante.ubicacion = "Punta Alta"
    datos.postulante.descripcion_personal = None
    datos.postulante.foto_perfil = None
    datos.postulante.cv_url = None
    datos.postulante.disponibilidad = None

    usuario_dao.crear_usuario.side_effect = (
        lambda usuario: setattr(usuario, "id", 1)
    )

    resultado = usuario_service.registrar_postulante(datos)

    assert resultado.nombre == "Nicolas"
    assert resultado.apellido == "Menin"
    assert resultado.usuario_id == 1

    usuario_dao.crear_usuario.assert_called_once()
    postulante_dao.crear_postulante.assert_called_once()

def test_registrar_empleador_email_existente():

    usuario_dao = Mock()

    usuario_existente = Mock()
    usuario_dao.buscar_por_email.return_value = usuario_existente

    postulante_dao = Mock()
    empleador_dao = Mock()
    autenticacion_service = Mock()
    token_service = Mock()
    brevo_service = Mock()

    usuario_service = UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )

    datos = Mock()
    datos.usuario.email = "empleador@correo.com"

    with pytest.raises(HTTPException) as error:
        usuario_service.registrar_empleador(datos)

    assert error.value.status_code == 409

def test_registrar_empleador_correctamente():

    usuario_dao = Mock()
    usuario_dao.buscar_por_email.return_value = None

    postulante_dao = Mock()
    empleador_dao = Mock()

    autenticacion_service = Mock()
    autenticacion_service.password_hash.return_value = "hash_de_prueba"

    token_service = Mock()
    brevo_service = Mock()

    usuario_service = UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )

    datos = Mock()

    datos.usuario.email = "empleador@correo.com"
    datos.usuario.password = "123456"

    datos.empleador.nombre_negocio = "Mi Negocio"
    datos.empleador.direccion = "Calle 123"
    datos.empleador.ubicacion = "Punta Alta"
    datos.empleador.descripcion = None
    datos.empleador.rubro = None
    datos.empleador.foto_perfil = None

    usuario_dao.crear_usuario.side_effect = (
        lambda usuario: setattr(usuario, "id", 1)
    )

    resultado = usuario_service.registrar_empleador(datos)

    assert resultado.nombre_negocio == "Mi Negocio"
    assert resultado.direccion == "Calle 123"
    assert resultado.usuario_id == 1

    usuario_dao.crear_usuario.assert_called_once()
    empleador_dao.crear_empleador.assert_called_once()


def test_recuperacion_contrasena_usuario_inexistente():

    usuario_dao = Mock()
    usuario_dao.buscar_por_email.return_value = None

    postulante_dao = Mock()
    empleador_dao = Mock()
    autenticacion_service = Mock()
    token_service = Mock()
    brevo_service = Mock()

    usuario_service = UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )

    with pytest.raises(HTTPException) as error:
        usuario_service.recuperacion_contrasena(
            email="usuario@correo.com"
        )

    assert error.value.status_code == 404

def test_recuperacion_contrasena_correctamente():

    usuario_dao = Mock()

    usuario = Mock()
    usuario.id = 1
    usuario_dao.buscar_por_email.return_value = usuario

    postulante_dao = Mock()
    empleador_dao = Mock()
    autenticacion_service = Mock()

    token_service = Mock()
    token_service.crear_token.return_value = "token_recuperacion"

    brevo_service = Mock()
    brevo_service.enviar_email_recuperacion_contrasena.return_value = (
        "Correo enviado correctamente"
    )

    usuario_service = UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )

    resultado = usuario_service.recuperacion_contrasena(
        email="usuario@correo.com"
    )

    assert resultado == "Correo enviado correctamente"

    token_service.crear_token.assert_called_once()

    brevo_service.enviar_email_recuperacion_contrasena.assert_called_once_with(
        "usuario@correo.com",
        "token_recuperacion"
    )

def test_obtener_usuario_id_correctamente():

    usuario_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    autenticacion_service = Mock()

    token_service = Mock()
    token_service.decodificar_token.return_value = 1

    brevo_service = Mock()

    usuario_service = UsuarioService(
        usuario_dao=usuario_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        autenticacion_service=autenticacion_service,
        token_service=token_service,
        brevo_service=brevo_service
    )

    resultado = usuario_service.obtener_usuario_id(
        "token_de_prueba"
    )

    assert resultado == 1

    token_service.decodificar_token.assert_called_once_with(
        "token_de_prueba"
    )