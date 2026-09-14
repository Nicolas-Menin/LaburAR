import cloudinary.uploader





class CloudinaryService:
    """Service de Cloudinary"""

    def actualizar_foto_perfil(self, archivo,id_usuario: int):
        """Metodo para actualizar foto de perfil"""


        archivo_imagen = cloudinary.uploader.upload(
            archivo,
            folder="laburar/imagenes_perfiles/",
            public_id = f"usuario_{id_usuario}",
            overwrite = True
            )

        url = archivo_imagen["secure_url"]

        return url

    def actualizar_cv_postulante(self,archivo,id_postulante):
        """Metodo para actualizar el cv del postulante"""

        archivo_cv = cloudinary.uploader.upload(
            archivo,
            folder="laburar/archivos_cv_postulante/",
            public_id = f"cv_postulante_{id_postulante}"
        )


        url = archivo_cv["secure_url"]

        return url