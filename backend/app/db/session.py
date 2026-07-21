from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import DB_URL



# CREACION DEL MOTOR DE LA BASE DE DATOS
engine = create_engine(DB_URL,echo=True,pool_pre_ping=True)

# FABRICA DE SESIONES PARA INTERACTUAR CON LA BASE DE DATIS
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=True
)