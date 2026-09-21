from unittest.mock import Mock
import pytest
from fastapi import HTTPException

from backend.app.services.empleador_service import EmpleadorService

def test_actualizar_empleador_inexistente():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador_dao.buscar_por_id.return_value = None

    datos = Mock()
    datos.nombre_negocio = "Nuevo negocio"
    datos.direccion = None
    datos.ubicacion = None
    datos.descripcion = None
    datos.rubro = None

    with pytest.raises(HTTPException) as exc_info:
        empleador_service.actualizar_empleador(
            datos=datos,
            usuario_id=1
        )

    assert exc_info.value.status_code == 404


def test_actualizar_empleador_correctamente():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador = Mock()
    empleador.nombre_negocio = "Negocio anterior"
    empleador.direccion = "Direccion anterior"
    empleador.ubicacion = "Ubicacion anterior"
    empleador.descripcion = "Descripcion anterior"
    empleador.rubro = "Rubro anterior"

    empleador_dao.buscar_por_id.return_value = empleador
    empleador_dao.actualizar_empleador.return_value = empleador

    datos = Mock()
    datos.nombre_negocio = "Nuevo negocio"
    datos.direccion = "Nueva direccion"
    datos.ubicacion = "Nueva ubicacion"
    datos.descripcion = "Nueva descripcion"
    datos.rubro = "Nuevo rubro"

    resultado = empleador_service.actualizar_empleador(
        datos=datos,
        usuario_id=1
    )

    assert resultado == empleador
    assert empleador.nombre_negocio == "Nuevo negocio"
    assert empleador.direccion == "Nueva direccion"
    assert empleador.ubicacion == "Nueva ubicacion"
    assert empleador.descripcion == "Nueva descripcion"
    assert empleador.rubro == "Nuevo rubro"


def test_actualizar_empleador_con_foto():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador = Mock()
    empleador.nombre_negocio = "Mi negocio"

    empleador_dao.buscar_por_id.return_value = empleador
    cloudinary_service.actualizar_foto_perfil.return_value = (
        "https://cloudinary.com/foto.jpg"
    )
    empleador_dao.actualizar_empleador.return_value = empleador

    datos = Mock()
    datos.nombre_negocio = None
    datos.direccion = None
    datos.ubicacion = None
    datos.descripcion = None
    datos.rubro = None

    resultado = empleador_service.actualizar_empleador(
        datos=datos,
        usuario_id=1,
        foto_perfil="foto.jpg"
    )

    assert resultado == empleador
    assert empleador.foto_perfil == "https://cloudinary.com/foto.jpg"

def test_perfil_empleador_correctamente():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador = Mock()
    empleador.id = 1

    perfil = Mock()

    empleador_dao.buscar_por_id.return_value = empleador
    empleador_dao.perfil_empleador.return_value = perfil

    resultado = empleador_service.perfil_empleador(1)

    assert resultado == perfil

    empleador_dao.perfil_empleador.assert_called_once_with(1)

def test_perfil_empleador_inexistente():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        empleador_service.perfil_empleador(1)

    assert exc_info.value.status_code == 404

def test_buscar_empleadores_con_filtros():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    filtros = Mock()
    filtros.busqueda = "Juan"
    filtros.direccion = "Calle 123"
    filtros.ubicacion = "Punta Alta"
    filtros.rubro = "Construccion"

    empleadores = ["empleador1", "empleador2"]

    empleador_dao.filtrar_empleadores.return_value = empleadores

    resultado = empleador_service.buscar_empleadores(filtros)

    assert resultado == empleadores


def test_buscar_empleadores_sin_filtros():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    filtros = Mock()
    filtros.busqueda = None
    filtros.direccion = None
    filtros.ubicacion = None
    filtros.rubro = None

    empleadores = []

    empleador_dao.filtrar_empleadores.return_value = empleadores

    resultado = empleador_service.buscar_empleadores(filtros)

    assert resultado == empleadores

def test_filtrar_postulaciones_empleador_inexistente():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        empleador_service.filtrar_postulaciones_oferta_laboral(
            usuario_id=1,
            offset=10,
            busqueda="Juan",
            oferta_id=5
        )

    assert exc_info.value.status_code == 404
def test_filtrar_postulaciones_oferta_laboral_correctamente():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador = Mock()
    empleador.id = 1

    postulaciones = ["postulacion1", "postulacion2"]

    empleador_dao.buscar_por_id.return_value = empleador
    postulacion_service.listar_postulaciones_empleador.return_value = postulaciones

    resultado = empleador_service.filtrar_postulaciones_oferta_laboral(
        usuario_id=1,
        offset=10,
        busqueda="Juan",
        oferta_id=5
    )

    assert resultado == postulaciones

def test_crear_oferta_laboral_correctamente():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador = Mock()
    empleador.id = 1

    empleador_dao.buscar_por_id.return_value = empleador

    datos = Mock()
    datos.titulo = "Atención al cliente"
    datos.descripcion = "Atención al cliente"
    datos.requisitos = "Experiencia previa"
    datos.ubicacion = "Punta Alta"
    datos.direccion = "Calle 123"
    datos.rubro = "Comercio"
    datos.estado = "ACTIVA"
    datos.salario_tipo = "MENSUAL"
    datos.salario_minimo = 500000
    datos.salario_maximo = 700000
    datos.jornada = "MEDIA_JORNADA"
    datos.turno = "MAÑANA"
    datos.dias_laborales = ["LUNES", "MARTES"]
    datos.hora_inicio = "08:00"
    datos.hora_fin = "13:00"

    oferta_creada = Mock()

    oferta_laboral_dao.crear_oferta_laboral.return_value = oferta_creada

    resultado = empleador_service.crear_oferta_laboral(
        datos=datos,
        usuario_id=1
    )

    assert resultado == oferta_creada

def test_crear_oferta_laboral_sin_datos_opcionales():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador = Mock()
    empleador.id = 1

    empleador_dao.buscar_por_id.return_value = empleador

    datos = Mock()
    datos.titulo = "Atención al cliente"
    datos.descripcion = "Atención al cliente"
    datos.requisitos = "Experiencia previa"
    datos.ubicacion = "Punta Alta"
    datos.direccion = "Calle 123"
    datos.rubro = "Comercio"
    datos.estado = "ACTIVA"
    datos.salario_tipo = "MENSUAL"
    datos.salario_minimo = None
    datos.salario_maximo = None
    datos.jornada = "MEDIA_JORNADA"
    datos.turno = "MAÑANA"
    datos.dias_laborales = None
    datos.hora_inicio = "08:00"
    datos.hora_fin = "13:00"

    oferta_creada = Mock()

    oferta_laboral_dao.crear_oferta_laboral.return_value = oferta_creada

    resultado = empleador_service.crear_oferta_laboral(
        datos=datos,
        usuario_id=1
    )

    assert resultado == oferta_creada

def test_actualizar_oferta_laboral_empleador_inexistente():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador_dao.buscar_por_id.return_value = None

    datos = Mock()

    with pytest.raises(HTTPException) as exc_info:
        empleador_service.actualizar_oferta_laboral(
            datos=datos,
            oferta_laboral_id=1,
            usuario_id=1
        )

    assert exc_info.value.status_code == 404

def test_actualizar_oferta_laboral_inexistente():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador = Mock()
    empleador.id = 1

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_empleador.return_value = None

    datos = Mock()

    with pytest.raises(HTTPException) as exc_info:
        empleador_service.actualizar_oferta_laboral(
            datos=datos,
            oferta_laboral_id=5,
            usuario_id=1
        )

    assert exc_info.value.status_code == 404

def test_actualizar_oferta_laboral_correctamente():

    empleador_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()
    oferta_laboral_dao = Mock()

    empleador_service = EmpleadorService(
        empleador_dao=empleador_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service,
        oferta_laboral_dao=oferta_laboral_dao
    )

    empleador = Mock()
    empleador.id = 1

    oferta = Mock()

    oferta.titulo = "Título anterior"
    oferta.descripcion = "Descripción anterior"
    oferta.requisitos = "Requisitos anteriores"
    oferta.ubicacion = "Ubicación anterior"
    oferta.direccion = "Dirección anterior"
    oferta.rubro = "Rubro anterior"
    oferta.estado = "ACTIVA"
    oferta.salario_tipo = "RANGO"
    oferta.salario_minimo = 400000
    oferta.salario_maximo = 600000
    oferta.dias_laborales = ["LUNES"]
    oferta.hora_inicio = "08:00"
    oferta.hora_fin = "12:00"

    empleador_dao.buscar_por_id.return_value = empleador
    oferta_laboral_dao.buscar_por_empleador.return_value = oferta
    oferta_laboral_dao.actualizar_oferta.return_value = oferta

    datos = Mock()

    datos.titulo = "Nuevo título"
    datos.descripcion = "Nueva descripción"
    datos.requisitos = "Nuevos requisitos"
    datos.ubicacion = "Nueva ubicación"
    datos.direccion = "Nueva dirección"
    datos.rubro = "Nuevo rubro"
    datos.estado = "PAUSADA"
    datos.salario_tipo = "RANGO"
    datos.salario_minimo = 500000
    datos.salario_maximo = 700000
    datos.dias_laborales = ["LUNES", "MARTES"]
    datos.hora_inicio = "09:00"
    datos.hora_fin = "13:00"

    resultado = empleador_service.actualizar_oferta_laboral(
        datos=datos,
        oferta_laboral_id=5,
        usuario_id=1
    )

    assert resultado == oferta
    assert oferta.titulo == "Nuevo título"
    assert oferta.descripcion == "Nueva descripción"
    assert oferta.requisitos == "Nuevos requisitos"
    assert oferta.ubicacion == "Nueva ubicación"
    assert oferta.direccion == "Nueva dirección"
    assert oferta.rubro == "Nuevo rubro"
    assert oferta.estado == "PAUSADA"
    assert oferta.salario_tipo == "RANGO"
    assert oferta.salario_minimo == 500000
    assert oferta.salario_maximo == 700000
    assert oferta.dias_laborales == ["LUNES", "MARTES"]
    assert oferta.hora_inicio == "09:00"
    assert oferta.hora_fin == "13:00"