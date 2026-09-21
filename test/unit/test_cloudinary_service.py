from unittest.mock import patch

from backend.app.services.cloudinary_service import CloudinaryService


def test_actualizar_foto_perfil_correctamente():
    service = CloudinaryService()

    resultado_cloudinary = {
        "secure_url": "https://cloudinary.com/foto-perfil.jpg"
    }

    with patch(
        "backend.app.services.cloudinary_service.cloudinary.uploader.upload",
        return_value=resultado_cloudinary
    ):
        resultado = service.actualizar_foto_perfil(
            "foto.jpg",
            1
        )

    assert resultado == "https://cloudinary.com/foto-perfil.jpg"


def test_actualizar_cv_postulante_correctamente():
    service = CloudinaryService()

    resultado_cloudinary = {
        "secure_url": "https://cloudinary.com/cv.pdf"
    }

    with patch(
        "backend.app.services.cloudinary_service.cloudinary.uploader.upload",
        return_value=resultado_cloudinary
    ):
        resultado = service.actualizar_cv_postulante(
            "cv.pdf",
            1
        )

    assert resultado == "https://cloudinary.com/cv.pdf"