from backend.app.db.session import SessionLocal



def obtener_sesion_bd():
    """Funcion para obtener una sesion para la base de datos"""

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()
