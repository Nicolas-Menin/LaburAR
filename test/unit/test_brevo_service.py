from unittest.mock import Mock

from backend.app.services.brevo_service import BrevoService


def test_enviar_email_recuperacion_contrasena_correctamente():
    client = Mock()
    client.transactional_emails.send_transac_email.return_value = {
        "message_id": "12345"
    }

    service = BrevoService(
        client=client,
        sender="no-reply@laburar.com"
    )

    resultado = service.enviar_email_recuperacion_contrasena(
        "usuario@gmail.com",
        "token123"
    )

    assert resultado == {"message_id": "12345"}