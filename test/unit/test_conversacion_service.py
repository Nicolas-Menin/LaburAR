from unittest.mock import Mock

from backend.app.services.conversacion_service import ConversacionService


def test_traer_conversacion_postulante_correctamente():

    conversacion_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    mensaje_dao = Mock()

    conversacion_service = ConversacionService(
        conversacion_dao=conversacion_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        mensaje_dao=mensaje_dao
    )

    postulante = Mock()
    postulante.id = 1

    conversacion = Mock()
    conversacion.id = 10
    conversacion.nombre_negocio = "Negocio ABC"
    conversacion.foto_perfil = "foto.jpg"
    conversacion.titulo = "Vendedor"

    postulante_dao.buscar_por_id.return_value = postulante
    conversacion_dao.traer_conversaciones_postulante.return_value = [conversacion]
    mensaje_dao.contar_mensajes_no_leidos.return_value = 3

    resultado = conversacion_service.traer_conversacion_postulante(
        usuario_id=1
    )

    assert resultado == [
        {
            "conversacion_id": 10,
            "nombre_empleador": "Negocio ABC",
            "foto_perfil": "foto.jpg",
            "nombre_oferta": "Vendedor",
            "cantidad_mensajes_no_leidos": 3
        }
    ]

def test_traer_conversacion_empleador_correctamente():

    conversacion_dao = Mock()
    postulante_dao = Mock()
    empleador_dao = Mock()
    mensaje_dao = Mock()

    conversacion_service = ConversacionService(
        conversacion_dao=conversacion_dao,
        postulante_dao=postulante_dao,
        empleador_dao=empleador_dao,
        mensaje_dao=mensaje_dao
    )

    empleador = Mock()
    empleador.id = 1

    conversacion = Mock()
    conversacion.id = 20
    conversacion.nombre = "Juan"
    conversacion.apellido = "Pérez"
    conversacion.foto_perfil = "foto.jpg"
    conversacion.titulo = "Programador"

    empleador_dao.buscar_por_id.return_value = empleador
    conversacion_dao.traer_conversaciones_empleador.return_value = [conversacion]
    mensaje_dao.contar_mensajes_no_leidos.return_value = 2

    resultado = conversacion_service.traer_conversacion_empleador(
        usuario_id=1
    )

    assert resultado == [
        {
            "conversacion_id": 20,
            "nombre": "Juan",
            "apellido": "Pérez",
            "foto_perfil": "foto.jpg",
            "nombre_oferta": "Programador",
            "cantidad_mensajes_no_leidos": 2
        }
    ]