from typing import List, Literal
from datetime import time

import flet as ft

from frontend.src.services.api_service import ApiService


class EmpleadorService:
    """Service de Empleador"""

    @staticmethod
    async def perfil(page: ft.Page):
        """Metodo para obtener perfil de empleador"""

        return await ApiService.get(
            page=page,
            endpoint="/empleador/perfil-empleador"
        )

    @staticmethod
    async def obtener_empleador(
        page: ft.Page,
        empleador_id: int
    ):
        """Metodo para obtener el perfil de un empleador por su id"""

        return await ApiService.get(
            page=page,
            endpoint=f"/empleador/{empleador_id}"
        )

    @staticmethod
    async def buscar_empleadores(
        page: ft.Page,
        busqueda: str | None = None,
        direccion: str | None = None,
        ubicacion: str | None = None,
        rubro: str | None = None,
        offset: int = 0,
    ):
        """Metodo para buscar empleadores"""

        params = {
            "busqueda": busqueda,
            "direccion": direccion,
            "ubicacion": ubicacion,
            "rubro": rubro,
            "offset": offset,
        }

        return await ApiService.get(
            page=page,
            endpoint="/empleador/buscar-empleadores",
            params=params
        )

    @staticmethod
    async def actualizar_empleador(
        page: ft.Page,
        nombre_negocio: str | None = None,
        direccion: str | None = None,
        ubicacion: str | None = None,
        descripcion: str | None = None,
        rubro: str | None = None,
        foto_perfil: str | None = None
    ):
        """Metodo para actualizar datos de empleador"""

        datos = {
            "nombre_negocio": nombre_negocio,
            "direccion": direccion,
            "ubicacion": ubicacion,
            "descripcion": descripcion,
            "rubro": rubro,
            "foto_perfil": foto_perfil
        }

        return await ApiService.put(
            page=page,
            endpoint="/empleador/actualizar-empleador",
            datos=datos
        )

    @staticmethod
    async def filtrar_postulaciones(
        page: ft.Page,
        oferta_id: int | None = None,
        busqueda: str | None = None,
        offset: int = 0
    ):
        """Metodo para filtrar postulaciones de oferta laboral de empleador"""

        params = {
            "oferta_id": oferta_id,
            "busqueda": busqueda,
            "offset": offset
        }

        return await ApiService.get(
            page=page,
            endpoint="/empleador/filtrar-postulaciones-oferta-laboral",
            params=params
        )

    @staticmethod
    async def actualizar_estado_postulacion(
        page: ft.Page,
        estado: Literal["ACEPTADA", "RECHAZADA"],
        oferta_id: int,
        postulacion_id:int
    ):
        """Metodo para actualizar el estado de una postulacion de oferta laboral de empleador"""

        datos = {
            "estado": estado,
        }

        return await ApiService.put(
            page=page,
            endpoint=f"/empleador/actualizar-estado-postulacion?oferta_id={oferta_id}&postulacion_id={postulacion_id}",
            datos=datos
            )

    @staticmethod
    async def verificar_conexiones_oferta_laboral(
        page: ft.Page,
        postulante_id: int
    ):
        """Metodo para verificar si ofertas laborales NO poseen conexion laboral"""

        params = {"postulante_id": postulante_id}

        return await ApiService.get(
            page=page,
            endpoint="/empleador/verificar-conexion-oferta-laboral",
            params=params
        )

    @staticmethod
    async def crear_oferta_laboral(
        page: ft.Page,
        titulo: str,
        descripcion: str,
        requisitos: List[str],
        ubicacion: str,
        direccion: str,
        rubro: str,
        estado: Literal[
            "ACTIVA",
            "PAUSADA"
        ],
        salario_tipo: Literal[
            "FIJO",
            "RANGO",
            "A_CONVENIR",
            "NO_INFORMAR"
        ],
        jornada: Literal[
            "COMPLETA",
            "MEDIA_JORNADA",
            "TEMPORAL",
            "A_CONVENIR"
        ],
        turno: Literal[
            "MAÑANA",
            "TARDE",
            "NOCHE"
        ],
        hora_inicio: time,
        hora_fin: time,
        salario_minimo: float | None = None,
        salario_maximo: float | None = None,
        dias_laborales: List[str] | None = None
    ):
        """Metodo para crear oferta laboral"""

        datos = {
            "titulo": titulo,
            "descripcion": descripcion,
            "requisitos": requisitos,
            "ubicacion": ubicacion,
            "direccion": direccion,
            "rubro": rubro,
            "estado": estado,
            "salario_tipo": salario_tipo,
            "salario_minimo": salario_minimo,
            "salario_maximo": salario_maximo,
            "jornada": jornada,
            "turno": turno,
            "dias_laborales": dias_laborales,
            "hora_inicio": str(hora_inicio),
            "hora_fin": str(hora_fin)
        }

        return await ApiService.post(
            page=page,
            endpoint="/empleador/crear-oferta-laboral",
            datos=datos
        )

    @staticmethod
    async def filtrar_ofertas_laborales(
        page: ft.Page,
        busqueda: str | None = None
    ):
        """Metodo para filtrar las ofertas laborales de empleador"""

        params = {"busqueda": busqueda}

        return await ApiService.get(
            page=page,
            endpoint="/empleador/filtrar-ofertas-laborales",
            params=params
        )

    @staticmethod
    async def actualizar_oferta_laboral(
        page: ft.Page,
        oferta_laboral_id: int,
        titulo: str | None = None,
        descripcion: str | None = None,
        requisitos: List[str] | None = None,
        ubicacion: str | None = None,
        direccion: str | None = None,
        rubro: str | None = None,
        estado: Literal[
            "ACTIVA",
            "PAUSADA",
            "CERRADA"
        ] | None = None,
        salario_tipo: Literal[
            "FIJO",
            "RANGO",
            "A_CONVENIR",
            "NO_INFORMAR"
        ] | None = None,
        jornada: Literal[
            "COMPLETA",
            "MEDIA_JORNADA",
            "TEMPORAL",
            "A_CONVENIR"
        ] | None = None,
        turno: Literal[
            "MAÑANA",
            "TARDE",
            "NOCHE"
        ] | None = None,
        hora_inicio: time | None = None,
        hora_fin: time | None = None,
        salario_minimo: float | None = None,
        salario_maximo: float | None = None,
        dias_laborales: List[str] | None = None,
    ):
        """Metodo para actualizar oferta laboral de postulante"""

        datos = {
            "titulo": titulo,
            "descripcion": descripcion,
            "requisitos": requisitos,
            "ubicacion": ubicacion,
            "direccion": direccion,
            "rubro": rubro,
            "estado": estado,
            "salario_tipo": salario_tipo,
            "salario_minimo": salario_minimo,
            "salario_maximo": salario_maximo,
            "jornada": jornada,
            "turno": turno,
            "dias_laborales": dias_laborales,
            "hora_inicio": hora_inicio.isoformat() if hora_inicio else None,
            "hora_fin": hora_fin.isoformat() if hora_fin else None
        }

        return await ApiService.put(
            page=page,
            endpoint=f"/empleador/actualizar-oferta-laboral?oferta_laboral_id={oferta_laboral_id}",
            datos=datos
        )

    @staticmethod
    async def crear_conexion_laboral(
        page: ft.Page,
        oferta_laboral_id: int,
        postulante_id: int,
    ):
        """Metodo para crear conexion laboral"""

        datos = {
            "oferta_laboral_id": oferta_laboral_id,
            "postulante_id": postulante_id
        }

        return await ApiService.post(
            page=page,
            endpoint="/empleador/crear-conexion-laboral",
            datos=datos
        )

    @staticmethod
    async def crear_conexion_laboral_postulacion(
        page: ft.Page,
        oferta_laboral_id: int,
        postulante_id: int,
        estado: Literal[
            "ACEPTADA",
            "RECHAZADA"
        ]
    ):
        """Metodo para crear conexion laboral mediante la aceptacion de una postulacion"""

        datos = {
            "oferta_laboral_id": oferta_laboral_id,
            "postulante_id": postulante_id,
            "estado": estado
        }

        return await ApiService.post(
            page=page,
            endpoint="/empleador/crear-conexion-laboral",
            datos=datos
        )

    @staticmethod
    async def buscar_conexiones_laborales(
        page: ft.Page,
        busqueda: str | None = None,
        oferta_id: int | None = None,
        offset: int = 0
    ):
        """Metodo para buscar conexiones laborales"""

        params = {
            "oferta_id": oferta_id,
            "busqueda": busqueda,
            "offset": offset
        }

        return await ApiService.get(
            page=page,
            endpoint="/empleador/buscar-conexiones-laborales",
            params=params
        )

    @staticmethod
    async def verificar_conexion_laboral(
        page: ft.Page,
        postulante_id: int,
        oferta_id: int | None = None
    ):
        """Metodo para verificar si existe conexion laboral con postulante"""

        params = {
            "postulante_id": postulante_id,
            "oferta_id": oferta_id
        }

        return await ApiService.get(
            page=page,
            endpoint="/empleador/verificar-conexion-laboral",
            params=params
        )