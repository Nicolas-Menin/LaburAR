
# EL OBJETO SESION SIRVE PARA VERIFICAR SI EL USUARIO POSEE TOKEN
class Sesion:
    """Clase que almacena el estado de la sesion del usuario"""

    token: str | None = None
    rol: str | None = None
