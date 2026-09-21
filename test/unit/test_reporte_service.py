from unittest.mock import Mock, patch
from backend.app.services.reporte_service import ReporteService


def test_crear_reporte_correctamente():

    reporte_dao = Mock()

    reporte_service = ReporteService(
        reporte_dao=reporte_dao
    )

    datos = Mock()
    datos.motivo = "Contenido inapropiado"
    datos.descripcion = "Descripción del reporte"

    reporte_creado = Mock()

    reporte_dao.crear_reporte.return_value = reporte_creado

    with patch("backend.app.services.reporte_service.Reporte"):

        resultado = reporte_service.crear_reporte(
            datos=datos,
            usuario_id=1,
            usuario_reportado_id=2
        )

    assert resultado == reporte_creado
