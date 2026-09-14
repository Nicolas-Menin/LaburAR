from pydantic import BaseModel


class ConversacionResponsePostulante(BaseModel):
    """Contrato para traer las conversaciones de un postulante"""

    conversacion_id: int
    nombre_empleador: str
    foto_perfil: str | None
    nombre_oferta: str
    cantidad_mensajes_no_leidos: int

class ConversacionResponseEmpleador(BaseModel):
    """Contrato para traer las conversaciones de un empleador"""

    conversacion_id: int
    nombre: str
    apellido: str
    foto_perfil: str | None
    nombre_oferta: str
    cantidad_mensajes_no_leidos: int
