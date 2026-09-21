from unittest.mock import Mock
import pytest
from fastapi import HTTPException

from backend.app.services.postulante_service import PostulanteService



def test_actualizar_postulante_inexistente():

    postulante_dao = Mock()
    estudio_dao = Mock()
    experiencia_laboral_dao = Mock()
    habilidad_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=habilidad_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service
    )

    datos = Mock()
    datos.nombre = "Nicolas"

    postulante_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.actualizar_postulante(
            datos=datos,
            usuario_id=1
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Postulante no encontrado"

    postulante_dao.actualizar_postulante.assert_not_called()

def test_actualizar_postulante_correctamente():

    postulante_dao = Mock()
    estudio_dao = Mock()
    experiencia_laboral_dao = Mock()
    habilidad_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=habilidad_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service
    )

    postulante = Mock()
    postulante.id = 1
    postulante.nombre = "Nicolas"
    postulante.apellido = "Menin"
    postulante.ubicacion = "Tucuman"
    postulante.descripcion_personal = "Gordo compu"
    postulante.disponibilidad = "Media jornada"

    postulante_dao.buscar_por_id.return_value = postulante

    datos = Mock()
    datos.nombre = "Nicolas"
    datos.apellido = "Menin"
    datos.ubicacion = "Punta Alta"
    datos.descripcion_personal = "Desarrollador backend"
    datos.disponibilidad = "Jornada completa"

    datos_mock = postulante_dao.actualizar_postulante.return_value

    resultado = service.actualizar_postulante(
        datos=datos,
        usuario_id=1
    )

    assert postulante.nombre == "Nicolas"
    assert postulante.apellido == "Menin"
    assert postulante.ubicacion == "Punta Alta"
    assert postulante.descripcion_personal == "Desarrollador backend"
    assert postulante.disponibilidad == "Jornada completa"

    postulante_dao.buscar_por_id.assert_called_once_with(1)
    postulante_dao.actualizar_postulante.assert_called_once_with(postulante)

    assert resultado == datos_mock

def test_actualizar_postulante_con_foto_y_cv():

    postulante_dao = Mock()
    estudio_dao = Mock()
    experiencia_laboral_dao = Mock()
    habilidad_dao = Mock()
    cloudinary_service = Mock()
    postulacion_service = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=habilidad_dao,
        cloudinary_service=cloudinary_service,
        postulacion_service=postulacion_service
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante

    cloudinary_service.actualizar_foto_perfil.return_value = "https://foto-nueva.jpg"
    cloudinary_service.actualizar_cv_postulante.return_value = "https://cv-nuevo.pdf"

    datos = Mock()

    datos.nombre = None
    datos.apellido = None
    datos.ubicacion = None
    datos.descripcion_personal = None
    datos.disponibilidad = None

    resultado = service.actualizar_postulante(
        datos=datos,
        usuario_id=1,
        foto_perfil="foto.jpg",
        cv="cv.pdf"
    )

    assert postulante.foto_perfil == "https://foto-nueva.jpg"
    assert postulante.cv_url == "https://cv-nuevo.pdf"

    cloudinary_service.actualizar_foto_perfil.assert_called_once_with(
        "foto.jpg",
        1
    )

    cloudinary_service.actualizar_cv_postulante.assert_called_once_with(
        "cv.pdf",
        1
    )

    postulante_dao.actualizar_postulante.assert_called_once_with(postulante)

    assert resultado == postulante_dao.actualizar_postulante.return_value

def test_perfil_postulante():

    postulante_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante

    resultado = service.perfil_postulante(usuario_id=1)

    assert resultado == postulante

    postulante_dao.buscar_por_id.assert_called_once_with(1)


def test_buscar_postulantes_con_filtros():

    postulante_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    filtro = Mock()
    filtro.busqueda = "Python"
    filtro.ubicacion = "Punta Alta"
    filtro.estudios = ["Ingeniero de Software"]
    filtro.experiencias_laborales = ["Desarrollador"]
    filtro.disponibilidad = "Jornada completa"

    habilidades = ["Python", "FastAPI"]

    resultado_esperado = ["postulante1", "postulante2"]

    postulante_dao.filtrar_postulantes.return_value = resultado_esperado

    resultado = service.buscar_postulantes(
        filtro=filtro,
        habilidades=habilidades,
        offset=10
    )

    assert resultado == resultado_esperado

    postulante_dao.filtrar_postulantes.assert_called_once_with(
        busqueda="Python",
        ubicacion="Punta Alta",
        estudios=["Ingeniero de Software"],
        habilidades=["Python", "FastAPI"],
        experiencias_laborales=["Desarrollador"],
        disponibilidad="Jornada completa",
        offset=10
    )


def test_buscar_postulantes_sin_filtros():

    postulante_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    filtro = Mock()
    filtro.busqueda = None
    filtro.ubicacion = None
    filtro.estudios = None
    filtro.experiencias_laborales = None
    filtro.disponibilidad = None

    resultado_esperado = []

    postulante_dao.filtrar_postulantes.return_value = resultado_esperado

    resultado = service.buscar_postulantes(
        filtro=filtro,
        habilidades=[],
        offset=0
    )

    assert resultado == resultado_esperado

    postulante_dao.filtrar_postulantes.assert_called_once_with(
        busqueda=None,
        ubicacion=None,
        estudios=None,
        habilidades=None,
        experiencias_laborales=None,
        disponibilidad=None,
        offset=0
    )

def test_crear_estudio_correctamente():

    postulante_dao = Mock()
    estudio_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante

    datos = Mock()
    datos.titulo = "Analista en Sistemas"
    datos.institucion = "Instituto 190"
    datos.fecha_inicio = "2023-03-01"
    datos.fecha_fin = None
    datos.estado = "EN_CURSO"
    datos.nivel = "TERCIARIO"

    resultado_esperado = Mock()

    estudio_dao.crear_estudio.return_value = resultado_esperado

    resultado = service.crear_estudio(
        datos=datos,
        usuario_id=1
    )

    estudio = estudio_dao.crear_estudio.call_args.args[0]

    assert estudio.postulante_id == 1
    assert estudio.titulo == "Analista en Sistemas"
    assert estudio.institucion == "Instituto 190"
    assert estudio.fecha_inicio == "2023-03-01"
    assert estudio.fecha_fin is None
    assert estudio.estado == "EN_CURSO"
    assert estudio.nivel == "TERCIARIO"

    assert resultado == resultado_esperado

    postulante_dao.buscar_por_id.assert_called_once_with(1)
    estudio_dao.crear_estudio.assert_called_once()

def test_actualizar_estudio_postulante_inexistente():

    postulante_dao = Mock()
    estudio_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante_dao.buscar_por_id.return_value = None

    datos = Mock()

    with pytest.raises(HTTPException) as error:
        service.actualizar_estudio(
            datos=datos,
            usuario_id=1,
            estudio_id=10
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Postulante no encontrado"

    estudio_dao.actualizar_estudio.assert_not_called()

def test_actualizar_estudio_inexistente():

    postulante_dao = Mock()
    estudio_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante
    estudio_dao.buscar_estudio_id.return_value = None

    datos = Mock()

    with pytest.raises(HTTPException) as error:
        service.actualizar_estudio(
            datos=datos,
            usuario_id=1,
            estudio_id=10
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Estudio no encontrado"

    estudio_dao.actualizar_estudio.assert_not_called()

def test_actualizar_estudio_correctamente():

    postulante_dao = Mock()
    estudio_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    estudio = Mock()
    estudio.id = 10
    estudio.postulante_id = 1
    estudio.titulo = "Titulo anterior"
    estudio.institucion = "Institucion anterior"
    estudio.fecha_inicio = "2023-01-01"
    estudio.fecha_fin = None
    estudio.nivel = "Nivel anterior"
    estudio.estado = "EN_CURSO"

    postulante_dao.buscar_por_id.return_value = postulante
    estudio_dao.buscar_estudio_id.return_value = estudio
    estudio_dao.actualizar_estudio.return_value = estudio

    datos = Mock()
    datos.titulo = "Analista en Sistemas"
    datos.institucion = "Instituto 190"
    datos.fecha_inicio = None
    datos.fecha_fin = "2026-12-01"
    datos.nivel = "Terciario"
    datos.estado = "FINALIZADO"

    resultado = service.actualizar_estudio(
        datos=datos,
        usuario_id=1,
        estudio_id=10
    )

    assert estudio.titulo == "Analista en Sistemas"
    assert estudio.institucion == "Instituto 190"

    # Este campo venia en None, asique tiene el mismo valor anterior
    assert estudio.fecha_inicio == "2023-01-01"

    assert estudio.fecha_fin == "2026-12-01"
    assert estudio.nivel == "Terciario"
    assert estudio.estado == "FINALIZADO"

    postulante_dao.buscar_por_id.assert_called_once_with(1)
    estudio_dao.buscar_estudio_id.assert_called_once_with(10, 1)
    estudio_dao.actualizar_estudio.assert_called_once_with(estudio)

    assert resultado == estudio

def test_eliminar_estudio_postulante_inexistente():

    postulante_dao = Mock()
    estudio_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.eliminar_estudio(
            estudio_id=10,
            usuario_id=1
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Postulante no encontrado"

    estudio_dao.buscar_estudio_id.assert_not_called()
    estudio_dao.eliminar_estudio.assert_not_called()

def test_eliminar_estudio_inexistente():

    postulante_dao = Mock()
    estudio_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante
    estudio_dao.buscar_estudio_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.eliminar_estudio(
            estudio_id=10,
            usuario_id=1
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Estudio no encontrado"

    estudio_dao.eliminar_estudio.assert_not_called()

def test_eliminar_estudio_correctamente():

    postulante_dao = Mock()
    estudio_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=estudio_dao,
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    estudio = Mock()
    estudio.id = 10
    estudio.postulante_id = 1

    postulante_dao.buscar_por_id.return_value = postulante
    estudio_dao.buscar_estudio_id.return_value = estudio

    resultado = service.eliminar_estudio(
        estudio_id=10,
        usuario_id=1
    )

    estudio_dao.eliminar_estudio.assert_called_once_with(estudio)

    assert resultado == estudio_dao.eliminar_estudio.return_value


def test_crear_experiencia_laboral_postulante_inexistente():

    postulante_dao = Mock()
    experiencia_laboral_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante_dao.buscar_por_id.return_value = None

    datos = Mock()

    with pytest.raises(HTTPException) as error:
        service.crear_experiencia_laboral(
            datos=datos,
            usuario_id=1
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Postulante no encontrado"

    experiencia_laboral_dao.crear_experiencia_laboral.assert_not_called()

def test_crear_experiencia_laboral_correctamente():

    postulante_dao = Mock()
    experiencia_laboral_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante

    datos = Mock()
    datos.empresa = "Empresa Test"
    datos.puesto = "Desarrollador"
    datos.fecha_inicio = "2025-01-01"
    datos.descripcion = "Desarrollo de aplicaciones"
    datos.area = "Sistemas"

    experiencia_creada = Mock()
    experiencia_laboral_dao.crear_experiencia_laboral.return_value = experiencia_creada

    resultado = service.crear_experiencia_laboral(
        datos=datos,
        usuario_id=1
    )

    experiencia_laboral_dao.crear_experiencia_laboral.assert_called_once()

    experiencia = experiencia_laboral_dao.crear_experiencia_laboral.call_args[0][0]

    assert experiencia.postulante_id == 1
    assert experiencia.empresa == "Empresa Test"
    assert experiencia.puesto == "Desarrollador"
    assert experiencia.fecha_inicio == "2025-01-01"
    assert experiencia.descripcion == "Desarrollo de aplicaciones"
    assert experiencia.area == "Sistemas"

    assert resultado == experiencia_creada

def test_actualizar_experiencia_laboral_inexistente():

    postulante_dao = Mock()
    experiencia_laboral_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante
    experiencia_laboral_dao.buscar_por_id.return_value = None

    datos = Mock()

    with pytest.raises(HTTPException) as error:
        service.actualizar_experiencia_laboral(
            datos=datos,
            usuario_id=1,
            experiencia_laboral_id=10
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Experiencia laboral no encontrado"

    experiencia_laboral_dao.actualizar_experiencia_laboral.assert_not_called()


def test_actualizar_experiencia_laboral_sin_permiso():

    postulante_dao = Mock()
    experiencia_laboral_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    experiencia = Mock()
    experiencia.postulante_id = 2

    postulante_dao.buscar_por_id.return_value = postulante
    experiencia_laboral_dao.buscar_por_id.return_value = experiencia

    datos = Mock()

    with pytest.raises(HTTPException) as error:
        service.actualizar_experiencia_laboral(
            datos=datos,
            usuario_id=1,
            experiencia_laboral_id=10
        )

    assert error.value.status_code == 403
    assert error.value.detail == (
        "Permiso denegado: No coinciden los id del postulante"
    )

    experiencia_laboral_dao.actualizar_experiencia_laboral.assert_not_called()

def test_actualizar_experiencia_laboral_correctamente():

    postulante_dao = Mock()
    experiencia_laboral_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    experiencia = Mock()
    experiencia.postulante_id = 1
    experiencia.empresa = "Empresa anterior"
    experiencia.puesto = "Puesto anterior"
    experiencia.fecha_inicio = "2024-01-01"
    experiencia.fecha_fin = "2024-12-01"
    experiencia.descripcion = "Descripción anterior"
    experiencia.area = "Área anterior"

    postulante_dao.buscar_por_id.return_value = postulante
    experiencia_laboral_dao.buscar_por_id.return_value = experiencia

    datos = Mock()
    datos.empresa = "Nueva Empresa"
    datos.puesto = "Desarrollador Backend"
    datos.fecha_inicio = "2025-01-01"
    datos.fecha_fin = None
    datos.descripcion = "Desarrollo de APIs"
    datos.area = None

    experiencia_actualizada = Mock()
    experiencia_laboral_dao.actualizar_experiencia_laboral.return_value = (
        experiencia_actualizada
    )

    resultado = service.actualizar_experiencia_laboral(
        datos=datos,
        usuario_id=1,
        experiencia_laboral_id=10
    )

    assert experiencia.empresa == "Nueva Empresa"
    assert experiencia.puesto == "Desarrollador Backend"
    assert experiencia.fecha_inicio == "2025-01-01"
    assert experiencia.fecha_fin == "2024-12-01"
    assert experiencia.descripcion == "Desarrollo de APIs"
    assert experiencia.area == "Área anterior"

    experiencia_laboral_dao.actualizar_experiencia_laboral.assert_called_once_with(
        experiencia
    )

    assert resultado == experiencia_actualizada

def test_eliminar_experiencia_laboral_postulante_inexistente():

    postulante_dao = Mock()
    experiencia_laboral_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.eliminar_experiencia_laboral(
            experiencia_laboral_id=10,
            usuario_id=1
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Postulante no encontrado"

    experiencia_laboral_dao.buscar_por_id.assert_not_called()
    experiencia_laboral_dao.eliminar_experiencia_laboral.assert_not_called()

def test_eliminar_experiencia_laboral_inexistente():

    postulante_dao = Mock()
    experiencia_laboral_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante
    experiencia_laboral_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.eliminar_experiencia_laboral(
            experiencia_laboral_id=10,
            usuario_id=1
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Experiencia laboral no encontrada"

    experiencia_laboral_dao.eliminar_experiencia_laboral.assert_not_called()

def test_eliminar_experiencia_laboral_correctamente():

    postulante_dao = Mock()
    experiencia_laboral_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=experiencia_laboral_dao,
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    experiencia = Mock()
    experiencia.id = 10
    experiencia.postulante_id = 1

    postulante_dao.buscar_por_id.return_value = postulante
    experiencia_laboral_dao.buscar_por_id.return_value = experiencia

    resultado_eliminacion = Mock()
    experiencia_laboral_dao.eliminar_experiencia_laboral.return_value = (
        resultado_eliminacion
    )

    resultado = service.eliminar_experiencia_laboral(
        experiencia_laboral_id=10,
        usuario_id=1
    )

    experiencia_laboral_dao.buscar_por_id.assert_called_once_with(
        10,
        1
    )

    experiencia_laboral_dao.eliminar_experiencia_laboral.assert_called_once_with(
        experiencia
    )

    assert resultado == resultado_eliminacion

def test_crear_habilidad_postulante_inexistente():

    postulante_dao = Mock()
    habilidad_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=Mock(),
        habilidad_dao=habilidad_dao,
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante_dao.buscar_por_id.return_value = None

    datos = Mock()
    datos.nombre = "Python"

    with pytest.raises(HTTPException) as error:
        service.crear_habilidad(
            datos=datos,
            usuario_id=1
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Postulante no encontrado"

    habilidad_dao.crear_habilidad.assert_not_called()

def test_crear_habilidad_correctamente():

    postulante_dao = Mock()
    habilidad_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=Mock(),
        habilidad_dao=habilidad_dao,
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante

    datos = Mock()
    datos.nombre = "Python"

    habilidad_creada = Mock()
    habilidad_dao.crear_habilidad.return_value = habilidad_creada

    resultado = service.crear_habilidad(
        datos=datos,
        usuario_id=1
    )

    habilidad_dao.crear_habilidad.assert_called_once()

    habilidad = habilidad_dao.crear_habilidad.call_args[0][0]

    assert habilidad.postulante_id == 1
    assert habilidad.nombre == "Python"

    assert resultado == habilidad_creada

def test_eliminar_habilidad_postulante_inexistente():

    postulante_dao = Mock()
    habilidad_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=Mock(),
        habilidad_dao=habilidad_dao,
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.eliminar_habilidad(
            habilidad_id=10,
            usuario_id=1
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Postulante no encontrado"

    habilidad_dao.buscar_por_id.assert_not_called()
    habilidad_dao.eliminar_habilidad.assert_not_called()

def test_eliminar_habilidad_inexistente():

    postulante_dao = Mock()
    habilidad_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=Mock(),
        habilidad_dao=habilidad_dao,
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante
    habilidad_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.eliminar_habilidad(
            habilidad_id=10,
            usuario_id=1
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Habilidad no encontrada"

    habilidad_dao.eliminar_habilidad.assert_not_called()

def test_eliminar_habilidad_correctamente():

    postulante_dao = Mock()
    habilidad_dao = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=Mock(),
        habilidad_dao=habilidad_dao,
        cloudinary_service=Mock(),
        postulacion_service=Mock()
    )

    postulante = Mock()
    postulante.id = 1

    habilidad = Mock()
    habilidad.id = 10
    habilidad.postulante_id = 1

    postulante_dao.buscar_por_id.return_value = postulante
    habilidad_dao.buscar_por_id.return_value = habilidad

    resultado_eliminacion = Mock()
    habilidad_dao.eliminar_habilidad.return_value = resultado_eliminacion

    resultado = service.eliminar_habilidad(
        habilidad_id=10,
        usuario_id=1
    )

    habilidad_dao.buscar_por_id.assert_called_once_with(
        10,
        1
    )

    habilidad_dao.eliminar_habilidad.assert_called_once_with(
        habilidad
    )

    assert resultado == resultado_eliminacion


def test_filtrar_postulaciones_postulante_inexistente():

    postulante_dao = Mock()
    postulacion_service = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=postulacion_service
    )

    postulante_dao.buscar_por_id.return_value = None

    with pytest.raises(HTTPException) as error:
        service.filtrar_postulaciones(
            usuario_id=1,
            offset=0,
            busqueda="Python"
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Postulante no encontrado"

    postulacion_service.listar_postulaciones_postulante.assert_not_called()


def test_filtrar_postulaciones_correctamente():

    postulante_dao = Mock()
    postulacion_service = Mock()

    service = PostulanteService(
        postulante_dao=postulante_dao,
        estudio_dao=Mock(),
        experiencia_laboral_dao=Mock(),
        habilidad_dao=Mock(),
        cloudinary_service=Mock(),
        postulacion_service=postulacion_service
    )

    postulante = Mock()
    postulante.id = 1

    postulante_dao.buscar_por_id.return_value = postulante

    resultado_esperado = [Mock(), Mock()]

    postulacion_service.listar_postulaciones_postulante.return_value = (
        resultado_esperado
    )

    resultado = service.filtrar_postulaciones(
        usuario_id=1,
        offset=10,
        busqueda="Desarrollador"
    )

    postulacion_service.listar_postulaciones_postulante.assert_called_once_with(
        1,
        "Desarrollador",
        10
    )

    assert resultado == resultado_esperado