from typing import List, Literal
from datetime import time
from frontend.src.services.api_service import ApiService




class EmpleadorService:
    """Service de Empleador"""


    @staticmethod
    async def perfil():
        """Metodo para obtener perfil de empleador"""

        return await ApiService.get("/empleador/perfil-empleador")

    @staticmethod
    async def buscar_empleadores(
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

        return await ApiService.get(endpoint="/empleador/buscar-empleadores",params=params)

    @staticmethod
    async def actualizar_empleador(
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


        return await ApiService.put(endpoint="/empleador/actualizar-empleador",datos=datos)

    @staticmethod
    async def filtrar_postulaciones(
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


        return await ApiService.get(endpoint="/empleador/filtrar-postulaciones-oferta-laboral",params=params)

    @staticmethod
    async def crear_oferta_laboral(
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


        return await ApiService.post(endpoint="/empleador/crear-oferta-laboral",datos=datos)

    @staticmethod
    async def actualizar_oferta_laboral(
        titulo: str | None = None,
        descripcion: str | None = None,
        requisitos: List[str] | None = None,
        ubicacion: str | None = None,
        direccion: str | None = None,
        rubro: str | None = None,
        estado: Literal[
            "ACTIVA",
            "PAUSADA"
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
        dias_laborales: List[str] | None = None
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
            "hora_inicio": str(hora_inicio),
            "hora_fin": str(hora_fin)

        }

        return await ApiService.put(endpoint="/empleador/actualizar-oferta-laboral",datos=datos)

    @staticmethod
    async def crear_conexion_laboral(
        oferta_laboral_id: int,
        postulante_id: int,
    ):
        """Metodo para crear conexion laboral"""

        datos = {
            "oferta_laboral_id": oferta_laboral_id,
            "postulante_id": postulante_id
        }

        return await ApiService.put(endpoint="/empleador/crear-conexion-laboral",datos=datos)

    @staticmethod
    async def crear_conexion_laboral_postulacion(
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

        return await ApiService.post(endpoint="/empleador/crear-conexion-laboral",datos=datos)

    @staticmethod
    async def buscar_conexiones_laborales(
        busqueda: str | None = None,
        offset: int = 0
    ):
        """Metodo para buscar conexiones laborales"""

        params = {
            "busqueda": busqueda,
            "offset": offset
        }

        return await ApiService.get(endpoint="/empleador/buscar-conexiones-laborales",params=params)

    @staticmethod
    async def verificar_conexion_laboral(
        postulante_id: int,
        oferta_id: int = None
    ):
        """Metodo para verificar si existe conexion laboral con postulante"""

        params = {
            "postulante_id": postulante_id,
            "oferta_id": oferta_id
        }


        return await ApiService.get("/empleador/verificar-conexion-laboral",params=params)

