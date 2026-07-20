from sqlalchemy import create_engine
from backend.app.core.config import DB_URL



# CREACION DEL MOTOR DE LA BASE DE DATOS
engine = create_engine(DB_URL,echo=True,pool_pre_ping=True)

