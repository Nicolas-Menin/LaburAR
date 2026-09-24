import httpx
from frontend.src.core.config import API_URL
from frontend.src.session.sesion import Sesion

class ApiService:
    """Service de API"""

    @staticmethod
    async def post(endpoint: str,datos: dict):
        """Metodo para realizar solicitudes POST"""

        headers =ApiService._obtener_headers()

        async with httpx.AsyncClient() as cliente:

            response = await cliente.post(f"{API_URL}{endpoint}",json=datos,headers=headers)

        response.raise_for_status()



        return response.json()


    @staticmethod
    async def put(endpoint:str, datos:dict):
        """Metodo para realizar solicitudes PUT"""

        headers =ApiService._obtener_headers()

        async with httpx.AsyncClient() as cliente:

            response = await cliente.put(f"{API_URL}{endpoint}",json=datos,headers=headers)


        response.raise_for_status()


        return response.json()

    @staticmethod
    async def get(endpoint:str, params: dict | None = None):
        """Metodo para realizar solicitudes GET"""

        headers =ApiService._obtener_headers()

        async with httpx.AsyncClient() as cliente:

            response = await cliente.get(f"{API_URL}{endpoint}",params=params,headers=headers)


        response.raise_for_status()

        return response.json()

    @staticmethod
    async def delete(endpoint: str, params: dict | None = None):
        """Metodo para realizar solicitudes DELETE"""

        headers =ApiService._obtener_headers()

        async with httpx.AsyncClient() as cliente:

            response = await cliente.delete(f"{API_URL}{endpoint}",params=params,headers=headers)


        response.raise_for_status()


        return response.json()

    @staticmethod
    async def _obtener_headers():
        """Metodo para obtener los headers de autenticacion"""

        if Sesion.token:

            return {"Authorization": f"Bearer {Sesion.token}"}


        return {}
