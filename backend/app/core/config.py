import os
import cloudinary
from brevo import Brevo


cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
)

CONFIG_DB = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_DATABASE")
}
DB_URL = os.getenv("DB_URL")
JWT_KEY = os.getenv("JWT_KEY")


client_brevo = Brevo(api_key=os.getenv("BREVO_API_KEY"))
sender = os.getenv("SENDER")
