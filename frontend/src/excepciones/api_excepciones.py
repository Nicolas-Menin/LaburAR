class ApiException(Exception):
    """Excepcion general de la API."""
    pass


class ErrorAutenticacion(ApiException):
    """Error de autenticacion."""
    pass


class ErrorValidacion(ApiException):
    """Error de validacion."""
    pass


class ErrorNoEncontrado(ApiException):
    """Recurso no encontrado."""
    pass


class ErrorServidor(ApiException):
    """Error interno del servidor."""
    pass

