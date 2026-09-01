from brevo import Brevo
from brevo import SendTransacEmailRequestToItem, SendTransacEmailRequestSender


class BrevoService:


    def __init__(self,client: Brevo,sender: str):
        self.client = client
        self.sender = sender



    def enviar_email_recuperacion_contrasena(
        self,
        destinatario: str,
        token: str
        ):
        """Metodo para enviar email de recuperacion de contraseña"""

        url =f"http://localhost:8550/restablecer-contrasena?token={token}"

        return self.client.transactional_emails.send_transac_email(
                subject="Restablecimiento de contraseña",
                html_content= f"""
                    <html>
                        <body>
                            <h2>Restablecer contraseña</h2>

                            <p>Recibimos una solicitud para restablecer tu contraseña.</p>

                            <p>
                                Hacé clic en el siguiente enlace para establecer una nueva contraseña:
                            </p>

                            <a href="{url}">
                                Restablecer contraseña
                            </a>

                            <p>
                                Este enlace expirará en 10 minutos.
                            </p>

                            <p>
                                Si no solicitaste este cambio, podés ignorar este correo.
                            </p>
                        </body>
                    </html>
                    """,
                sender=  SendTransacEmailRequestSender(
                    name="LaburAR",
                    email=self.sender
                ),
                to= [
                    SendTransacEmailRequestToItem(
                        email=destinatario
                    )
                ]
            )

