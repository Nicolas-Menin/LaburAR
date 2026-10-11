from typing import Literal, List
from datetime import date
import flet as ft

from frontend.src.services.api_service import ApiService


class PostulanteService:
    """Service de Postulante"""

    @staticmethod
    async def perfil(page: ft.Page):
        """Metodo para obtener perfil de postulante"""

        return await ApiService.get(
            page,
            endpoint="/postulante/perfil"
        )

    @staticmethod
    async def obtener_postulante(
        page: ft.Page,
        postulante_id: int
    ):
        """Metodo para obtener el perfil de un postulante por su id"""

        return await ApiService.get(
            page,
            f"/postulante/{postulante_id}"
        )

    @staticmethod
    async def buscar_postulantes(
        page: ft.Page,
        busqueda: str | None = None,
        ubicacion: str | None = None,
        estudios: str | None = None,
        experiencias_laborales: str | None = None,
        disponibilidad: Literal[
            "JORNADA_COMPLETA",
            "MEDIA_JORNADA",
            "FINES_SEMANA",
            "A_CONVENIR"
        ] | None = None,
        habilidades: List[str] | None = None,
        offset: int = 0
    ):
        """Metodo para buscar postulantes"""

        params = {
            "busqueda": busqueda,
            "ubicacion": ubicacion,
            "estudios": estudios,
            "experiencias_laborales": experiencias_laborales,
            "disponibilidad": disponibilidad,
            "habilidades": habilidades,
            "offset": offset
        }

        return await ApiService.get(
            page,
            endpoint="/postulante/buscar-postulantes",
            params=params
        )

    @staticmethod
    async def actualizar_postulante(
        page: ft.Page,
        nombre: str | None = None,
        apellido: str | None = None,
        ubicacion: str | None = None,
        descripcion_personal: str | None = None,
        disponibilidad: Literal[
            "JORNADA_COMPLETA",
            "MEDIA_JORNADA",
            "FINES_SEMANA",
            "A_CONVENIR"
        ] | None = None,
        foto_perfil: str | None = None,
        cv: str | None = None
    ):
        """Metodo para actualizar postulante"""

        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "ubicacion": ubicacion,
            "descripcion_personal": descripcion_personal,
            "disponibilidad": disponibilidad,
            "foto_perfil": foto_perfil,
            "cv": cv

        }


        return await ApiService.put(
            page,
            endpoint="/postulante/actualizar-postulante",
            datos=datos
        )

    @staticmethod
    async def crear_estudio(
        page: ft.Page,
        titulo: str,
        institucion: str,
        fecha_inicio: date,
        estado: Literal[
            "EN_CURSO",
            "NO_TERMINADO",
            "FINALIZADO"
        ],
        nivel: Literal[
            "PRIMARIO",
            "SECUNDARIO",
            "UNIVERSITARIO",
            "TERCIARIO",
            "CURSO"
        ],
        fecha_fin: date | None = None,
    ):
        """Metodo para crear estudio de postulante"""

        datos = {
            "titulo": titulo,
            "institucion": institucion,
            "fecha_inicio": fecha_inicio.isoformat() ,
            "fecha_fin": fecha_fin.isoformat() if fecha_fin else None,
            "estado": estado,
            "nivel": nivel
        }

        return await ApiService.post(
            page,
            endpoint="/postulante/crear-estudio",
            datos=datos
        )

    @staticmethod
    async def actualizar_estudio(
        page: ft.Page,
        estudio_id: int,
        titulo: str | None = None,
        institucion: str | None = None,
        fecha_inicio: date | None = None,
        estado: Literal[
            "EN_CURSO",
            "NO_TERMINADO",
            "FINALIZADO"
        ] | None = None,
        nivel: Literal[
            "PRIMARIO",
            "SECUNDARIO",
            "UNIVERSITARIO",
            "TERCIARIO",
            "CURSO"
        ] | None = None,
        fecha_fin: date | None = None,
    ):
        """Metodo para actualizar datos de estudio de postulante"""

        datos = {
            "titulo": titulo,
            "institucion": institucion,
            "fecha_inicio": fecha_inicio.isoformat() if fecha_inicio else None,
            "fecha_fin": fecha_fin.isoformat() if fecha_fin else None,
            "estado": estado,
            "nivel": nivel
        }

        return await ApiService.put(
            page,
            endpoint=f"/postulante/actualizar-estudio?estudio_id={estudio_id}",
            datos=datos
        )

    @staticmethod
    async def eliminar_estudio(
        page: ft.Page,
        estudio_id: int
    ):
        """Metodo para eliminar estudio de postulante"""

        params = {"estudio_id": estudio_id}

        return await ApiService.delete(
            page,
            "/postulante/eliminar-estudio",
            params=params
        )

    @staticmethod
    async def crear_experiencia_laboral(
        page: ft.Page,
        empresa: str,
        puesto: str,
        fecha_inicio: date,
        fecha_fin: date,
        descripcion: str,
        area: str
    ):
        """Metodo para crear experiencia laboral de postulante"""

        datos = {
            "empresa": empresa,
            "puesto": puesto,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat() if fecha_fin else None,
            "descripcion": descripcion,
            "area": area
        }

        return await ApiService.post(
            page,
            endpoint="/postulante/crear-experiencia-laboral",
            datos=datos
        )

    @staticmethod
    async def actualizar_experiencia_laboral(
        page: ft.Page,
        experiencia_laboral_id: int,
        empresa: str | None = None,
        puesto: str | None = None,
        fecha_inicio: date | None = None,
        fecha_fin: date | None = None,
        descripcion: str | None = None,
        area: str | None = None,
    ):
        """Metodo para actualizar datos de la experiencia laboral de postulante"""

        datos = {
            "empresa": empresa,
            "puesto": puesto,
            "fecha_inicio": fecha_inicio.isoformat() if fecha_inicio else None,
            "fecha_fin": fecha_fin.isoformat() if fecha_fin else None,
            "descripcion": descripcion,
            "area": area,
        }

        return await ApiService.put(
            page,
            endpoint=f"/postulante/actualizar-experiencia-laboral?experiencia_laboral_id={experiencia_laboral_id}",
            datos=datos
        )

    @staticmethod
    async def eliminar_experiencia_laboral(
        page: ft.Page,
        experiencia_laboral_id: int
    ):
        """Metodo para eliminar experiencia laboral de postulante"""

        params = {
            "experiencia_laboral_id": experiencia_laboral_id
        }

        return await ApiService.delete(
            page,
            endpoint="/postulante/eliminar-experiencia-laboral",
            params=params
        )

    @staticmethod
    async def crear_habilidad(
        page: ft.Page,
        nombre: str
    ):
        """Metodo para crear habilidad de postulante"""

        datos = {"nombre": nombre}

        return await ApiService.post(
            page,
            endpoint="/postulante/crear-habilidad",
            datos=datos
        )

    @staticmethod
    async def eliminar_habilidad(
        page: ft.Page,
        habilidad_id: int
    ):
        """Metodo para eliminar habilidad de postulante"""

        params = {"habilidad_id": habilidad_id}

        return await ApiService.delete(
            page,
            "/postulante/eliminar-habilidad",
            params=params
        )

    @staticmethod
    async def filtrar_postulaciones(
        page: ft.Page,
        busqueda: str | None = None,
        offset: int = 0
    ):
        """Metodo para filtrar las postulaciones de postulante"""

        params = {
            "busqueda": busqueda,
            "offset": offset
        }

        return await ApiService.get(
            page,
            endpoint="/postulante/mis-postulaciones",
            params=params
        )

    @staticmethod
    async def crear_postulacion(
        page: ft.Page,
        oferta_id: int
    ):
        """Metodo para crear/postularse a una oferta laboral"""

        datos = {"oferta_id": oferta_id}

        return await ApiService.post(
            page,
            "/postulante/crear-postulacion",
            datos=datos
        )

    @staticmethod
    async def verificar_postulacion(
        page: ft.Page,
        oferta_id: int
    ):
        """Metodo para verificar si un postulante esta postulado a una oferta laboral"""

        params = {"oferta_id": oferta_id}

        return await ApiService.get(
            page,
            "/postulante/verificar-postulacion",
            params=params
        )

    @staticmethod
    async def actualizar_conexion_laboral(
        page: ft.Page,
        conexion_laboral_id: int,
        estado: Literal[
            "ACEPTADA",
            "RECHAZADA"
        ]
    ):
        """Metodo para actualizar conexion laboral"""

        datos = {
            "conexion_laboral_id": conexion_laboral_id,
            "estado": estado
        }

        return await ApiService.put(
            page,
            "/postulante/actualizar-solicitud-laboral",
            datos=datos
        )

    @staticmethod
    async def verificar_conexion_laboral(
        page: ft.Page,
        oferta_id: int
    ):
        """Metodo para verificar si existe una conexion laboral con una oferta laboral"""

        params = {"oferta_id": oferta_id}

        return await ApiService.get(
            page,
            endpoint="/postulante/verificar-conexion-laboral",
            params=params
        )

    @staticmethod
    async def buscar_conexiones_laborales(
        page: ft.Page,
        busqueda: str | None = None,
        offset: int = 0
    ):
        """Metodo para buscar conexiones laborales de postulante"""

        params = {
            "busqueda": busqueda,
            "offset": offset
        }

        return await ApiService.get(
            page,
            "/postulante/buscar-solicitudes-laborales",
            params=params
        )