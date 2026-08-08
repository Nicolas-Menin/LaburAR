from sqlalchemy.orm import Session
from backend.app.models.usuario import Usuario


class UsuarioDAO:
    """"""

    def __init__(self,db: Session):
        self.db = db



    def crear_usuario(self, usuario: Usuario):
        """Metodo para crear usuario"""

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)

        return usuario


    def buscar_por_id(self,id_usuario:int):
        """Metodo para buscar usuario por id"""

        return self.db.query(Usuario).filter(
            Usuario.id == id_usuario
        ).first()

    def listar_usuarios(self,offset: int = 0, limit: int = 10):
        """Metodo para listar usuarios"""

        return self.db.query(Usuario).offset(offset).limit(limit).all()



    def buscar_por_email(self,email: str):
        """Método para buscar usuario por email"""

        return self.db.query(Usuario).filter(
            Usuario.email == email
        ).first()

    def actualizar_usuario(self,usuario:Usuario):
        """Metodo para actualizar los datos del usuario"""

        self.db.commit()
        self.db.refresh(usuario)

        return usuario

