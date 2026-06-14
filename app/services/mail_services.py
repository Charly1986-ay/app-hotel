from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings

# Configuración usando tu archivo centralizado de config
mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False
)

async def send_email_base(email_destination: str, subject: str, body_html: str):
    """
    Función utilitaria para enviar correos asincrónicos.
    La puedes importar en cualquier parte del sistema.
    """
    message = MessageSchema(
        subject=subject,
        recipients=[email_destination],
        body=body_html,
        subtype=MessageType.html
    )
    
    fm = FastMail(mail_conf)
    await fm.send_message(message)

def generate_welcome_html(user_name: str) -> str:
    """Genera el diseño HTML para el correo de bienvenida del hotel."""
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; background-color: #4f46e5; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0;">🏨 ¡Bienvenido a Hotel Management!</h1>
            </div>
            <div style="padding: 20px; border: 1px solid #e5e7eb; border-top: none; border-radius: 0 0 8px 8px;">
                <p>Hola <strong>{user_name}</strong>,</p>
                <p>Gracias por registrarte en nuestra plataforma. Tu cuenta ha sido creada con éxito.</p>
                <p>A partir de ahora podrás gestionar tus reservas, ver tus habitaciones favoritas y acceder a beneficios exclusivos.</p>
                <br>
                <a href="#" style="background-color: #4f46e5; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Explorar Habitaciones</a>
            </div>
        </body>
    </html>
    """

def generate_booking_invoice_html(customer_name: str, room_name: str, check_in: str, check_out: str, total_price: float) -> str:
    """Genera la plantilla HTML estructurada para el comprobante de pago de la reserva."""
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <div style="text-align: center; border-bottom: 2px solid #4f46e5; padding-bottom: 20px;">
                <h1 style="color: #4f46e5; margin: 0;">🏨 Confirmación de Reserva</h1>
                <p style="margin: 5px 0 0 0; color: #666;">¡Pago Recibido con Éxito!</p>
            </div>
            
            <div style="padding: 20px 0;">
                <p>Hola <strong>{customer_name}</strong>,</p>
                <p>Tu pago ha sido procesado correctamente. Tu estancia en nuestro hotel está completamente garantizada. Aquí tienes los detalles de tu reserva:</p>
                
                <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                    <tr style="background-color: #f9fafb;">
                        <td style="padding: 10px; border: 1px solid #e5e7eb; font-weight: bold;">Habitación / Servicio</td>
                        <td style="padding: 10px; border: 1px solid #e5e7eb; text-align: right;">{room_name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #e5e7eb; font-weight: bold;">Fecha de Check-In</td>
                        <td style="padding: 10px; border: 1px solid #e5e7eb; text-align: right;">{check_in}</td>
                    </tr>
                    <tr style="background-color: #f9fafb;">
                        <td style="padding: 10px; border: 1px solid #e5e7eb; font-weight: bold;">Fecha de Check-Out</td>
                        <td style="padding: 10px; border: 1px solid #e5e7eb; text-align: right;">{check_out}</td>
                    </tr>
                    <tr style="font-size: 18px; font-weight: bold; color: #4f46e5;">
                        <td style="padding: 15px; border-top: 2px solid #4f46e5;">Total Pagado</td>
                        <td style="padding: 15px; border-top: 2px solid #4f46e5; text-align: right;">${total_price:.2f} USD</td>
                    </tr>
                </table>
            </div>
            
            <div style="text-align: center; font-size: 12px; color: #9ca3af; border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 20px;">
                <p>Ante cualquier duda o modificación en tu viaje, por favor ponte en contacto con nosotros respondiendo a este mail.</p>
                <p><strong>Hotel Management System</strong></p>
            </div>
        </body>
    </html>
    """