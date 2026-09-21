from typing import Literal
from fastapi import HTTPException
from backend.app.repositories.administtrador_dao import AdministradorDAO
from backend.app.repositories.usuario_dao import UsuarioDAO
from backend.app.repositories.reporte_dao import ReporteDAO


class AdministradorService:
    """Service de Administrador"""

    def __init__(self,
                 administrador_dao: AdministradorDAO,
                 reporte_dao: ReporteDAO,
                 usuario_dao: UsuarioDAO
                 ):
        self.administrador_dao = administrador_dao
        self.reporte_dao = reporte_dao
        self.usuario_dao = usuario_dao



    def filtrar_usuarios(self,usuario_id: int, filtros: Literal["POSTULANTE","EMPLEADOR"],offset: int = 0,busqueda: str | None = None):
        """Metodo para filtrar y buscar usuarios por rol"""

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise HTTPException(404, "Usuario no encontrado")

        if usuario.rol != "ADMINISTRADOR":
            raise HTTPException(401,"Unauthorized: No eres administrador")


        return self.administrador_dao.listar_usuarios(filtros,busqueda,offset)


    def moderar_reporte(self,
                        estado:  Literal["REVISADO","PENDIENTE","SANCIONADO"],
                        reporte_id: int,
                        usuario_id:int
                        ):
        """Metodo para moderar el reporte"""

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise HTTPException(404, "Usuario no encontrado")

        if usuario.rol != "ADMINISTRADOR":
            raise HTTPException(401,"Unauthorized: No eres administrador")

        reporte = self.reporte_dao.buscar_reporte_por_id(reporte_id)

        if not reporte:
            raise HTTPException(404, "Reporte no encontrado")
        reporte.estado = estado

        return self.reporte_dao.actualizar_reporte(reporte)

    def desactivar_usuario(self,usuario_id:int,desactivar_usuario_id:int):
        """Metodo para desactivar usuario"""

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise HTTPException(404, "Usuario no encontrado")

        if usuario.rol != "ADMINISTRADOR":
            raise HTTPException(401,"Unauthorized: No eres administrador")

        usuario_desactivado = self.usuario_dao.buscar_por_id(desactivar_usuario_id)

        if not usuario_desactivado:
            raise HTTPException(404, "Usuario para desactivar no encontrado")

        if usuario_desactivado.estado == "DESACTIVADO":
            raise HTTPException(422, "El usuario ya esta desactivado")

        usuario_desactivado.estado = "DESACTIVADO"

        return self.administrador_dao.actualizar_estado_usuario(usuario_desactivado)

    def banear_usuario(self,usuario_id:int,banear_usuario_id: int):
        """Metodo para banear usuario"""

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise HTTPException(404, "Usuario no encontrado")

        if usuario.rol != "ADMINISTRADOR":
            raise HTTPException(401,"Unauthorized: No eres administrador")

        usuario_baneado = self.usuario_dao.buscar_por_id(banear_usuario_id)

        if not usuario_baneado:
            raise HTTPException(404, "Usuario para banear no encontrado")

        if usuario_baneado.estado == "BANEADO":
            raise HTTPException(422, "El usuario ya esta baneado")

        usuario_baneado.estado = "BANEADO"

        return self.administrador_dao.actualizar_estado_usuario(usuario_baneado)


    def filtrar_reportes(
        self,
        usuario_id: int,
        filtros:  Literal["REVISADO","PENDIENTE","SANCIONADO"],
        busqueda: str | None = None,
        offset: int = 0,
        ):
        """Metodo para filtrar y buscar reportes"""

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise HTTPException(404, "Usuario no encontrado")

        if usuario.rol != "ADMINISTRADOR":
            raise HTTPException(401,"Unauthorized: No eres administrador")

        return self.reporte_dao.listar_reportes(filtros,busqueda,offset)