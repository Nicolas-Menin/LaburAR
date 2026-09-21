from unittest.mock import Mock

from backend.app.services.administrador_service import AdministradorService


def test_filtrar_usuarios_correctamente():

    administrador_dao = Mock()
    reporte_dao = Mock()
    usuario_dao = Mock()

    administrador_service = AdministradorService(
        administrador_dao=administrador_dao,
        reporte_dao=reporte_dao,
        usuario_dao=usuario_dao
    )

    usuario = Mock()
    usuario.rol = "ADMINISTRADOR"

    usuario_dao.buscar_por_id.return_value = usuario

    usuarios = ["usuario1", "usuario2"]

    administrador_dao.listar_usuarios.return_value = usuarios

    resultado = administrador_service.filtrar_usuarios(
        usuario_id=1,
        filtros="POSTULANTE",
        offset=10,
        busqueda="Juan"
    )

    assert resultado == usuarios

def test_moderar_reporte_correctamente():

    administrador_dao = Mock()
    reporte_dao = Mock()
    usuario_dao = Mock()

    administrador_service = AdministradorService(
        administrador_dao=administrador_dao,
        reporte_dao=reporte_dao,
        usuario_dao=usuario_dao
    )

    usuario = Mock()
    usuario.rol = "ADMINISTRADOR"

    usuario_dao.buscar_por_id.return_value = usuario

    reporte = Mock()
    reporte_dao.buscar_reporte_por_id.return_value = reporte

    reporte_dao.actualizar_reporte.return_value = reporte

    resultado = administrador_service.moderar_reporte(
        estado="REVISADO",
        reporte_id=5,
        usuario_id=1
    )

    assert resultado == reporte

def test_filtrar_reportes_correctamente():

    administrador_dao = Mock()
    reporte_dao = Mock()
    usuario_dao = Mock()

    administrador_service = AdministradorService(
        administrador_dao=administrador_dao,
        reporte_dao=reporte_dao,
        usuario_dao=usuario_dao
    )

    usuario = Mock()
    usuario.rol = "ADMINISTRADOR"

    usuario_dao.buscar_por_id.return_value = usuario

    reportes = ["reporte1", "reporte2"]

    reporte_dao.listar_reportes.return_value = reportes

    resultado = administrador_service.filtrar_reportes(
        usuario_id=1,
        filtros="PENDIENTE",
        busqueda="spam",
        offset=10
    )

    assert resultado == reportes

def test_desactivar_usuario_correctamente():

    administrador_dao = Mock()
    reporte_dao = Mock()
    usuario_dao = Mock()

    administrador_service = AdministradorService(
        administrador_dao=administrador_dao,
        reporte_dao=reporte_dao,
        usuario_dao=usuario_dao
    )

    administrador = Mock()
    administrador.rol = "ADMINISTRADOR"

    usuario = Mock()
    usuario.estado = "ACTIVO"

    usuario_dao.buscar_por_id.side_effect = [
        administrador,
        usuario
    ]

    administrador_dao.actualizar_estado_usuario.return_value = usuario

    resultado = administrador_service.desactivar_usuario(
        usuario_id=1,
        desactivar_usuario_id=2
    )

    assert resultado == usuario

def test_banear_usuario_correctamente():

    administrador_dao = Mock()
    reporte_dao = Mock()
    usuario_dao = Mock()

    administrador_service = AdministradorService(
        administrador_dao=administrador_dao,
        reporte_dao=reporte_dao,
        usuario_dao=usuario_dao
    )

    administrador = Mock()
    administrador.rol = "ADMINISTRADOR"

    usuario = Mock()
    usuario.estado = "ACTIVO"

    usuario_dao.buscar_por_id.side_effect = [
        administrador,
        usuario
    ]

    administrador_dao.actualizar_estado_usuario.return_value = usuario

    resultado = administrador_service.banear_usuario(
        usuario_id=1,
        banear_usuario_id=2
    )

    assert resultado == usuario