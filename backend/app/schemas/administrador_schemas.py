from typing import List
from pydantic import BaseModel
from backend.app.schemas.reporte_schemas import ReporteAdministrador
from backend.app.schemas.usuario_schemas import UsuarioAdministrador


class AdministradorUsuarios(BaseModel):
    """Contrato para que el administradorvisualice los usuarios"""

    usuarios: List[UsuarioAdministrador] | None = None


class AdministradorReportes(BaseModel):
    """Contrato para que el administrador visualice  los reportes"""

    reportes: List[ReporteAdministrador] | None = None