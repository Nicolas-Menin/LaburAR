import os
from dotenv import load_dotenv
import cloudinary
from brevo import Brevo
from sqlalchemy import URL

# CARGAMOS LAS VARIABLES DE ENTORNO
load_dotenv()

# CONFIGURACION DE CLOUDINARY (SERVICIO DE ALMACENAMIENTO DE ARCHIVOS)
cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
)

# CONFIGURACION DE LA BASE DE DATOS
CONFIG_DB = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_DATABASE")
}

# CREACION DE LA URL DE LA BASE DE DATOS PARA EL MOTOR DE BASE DE DATOS
DB_URL = URL.create(
    drivername="postgresql+psycopg",
    username=CONFIG_DB["user"],
    password=CONFIG_DB["password"],
    host=CONFIG_DB["host"],
    port=CONFIG_DB["port"],
    database=CONFIG_DB["database"]
)

# CLAVE UTILIZADA PARA LA GENERACION Y VALIDACION DE TOKENS JWT
JWT_KEY = os.getenv("JWT_KEY")

# CREACION DE CLIENTE PARA EL SERVICIO DE ENVIO DE CORREOS ELECTRONICOS
client_brevo = Brevo(api_key=os.getenv("BREVO_API_KEY"))

# DIRECCION DE CORREO UTILIZADA COMO REMITENTE
sender = os.getenv("SENDER")

# URL DEL SERVIDOR DE LA API
API_URL = os.getenv("API_URL")
