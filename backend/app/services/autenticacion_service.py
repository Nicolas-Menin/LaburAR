import bcrypt



class AutenticacionService:
    """Service de Autenticacion"""

    def password_hash(self, password: str):
        """Metodo para hashear la contraseña del usuario"""

        password_bits = password.encode()

        salt = bcrypt.gensalt()

        hash_bites = bcrypt.hashpw(password_bits,salt)

        contrasena_hash = hash_bites.decode()

        return contrasena_hash


    def verify_password(self,password_user: str,password_db:str):
        """Metodo para verificar la contraseña de usuario es correcta."""

        return bcrypt.checkpw(password_user.encode(),password_db.encode())