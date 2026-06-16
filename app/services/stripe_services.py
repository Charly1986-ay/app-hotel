import stripe
from fastapi.concurrency import run_in_threadpool
from app.core.config import settings

# Configuramos la clave secreta de Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def _execute_stripe_charge(amount: int, currency: str, stripe_token: str):
    """
    Función sincrónica que interactúa con Stripe cumpliendo con todas las reglas de su API.
    """
    return stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        # 1. Pasamos el token como método de pago directo
        payment_method_data={
            "type": "card",
            "card": {"token": stripe_token},
        },
        confirm=True,  # Confirmamos el pago de inmediato
        
        # 2. SOLUCIÓN COMPLETA AL TRACEBACK:
        # Le decimos que use los métodos automáticos del dashboard pero PROHIBIMOS redirecciones
        automatic_payment_methods={
            "enabled": True,
            "allow_redirects": "never"  # ◄ ¡Esto es lo que soluciona el InvalidRequestError!
        },
        off_session=False,
    )

async def create_payment(amount: float, stripe_token: str, currency: str = "usd"):
    """
    Tu función asíncrona original que llama tu 'booking_services.py'.
    """
    # Convertimos el float (66) a centavos enteros (6600)
    amount_in_cents = int(amount * 100)
    
    # Ejecutamos en el pool de hilos
    payment_intent = await run_in_threadpool(
        _execute_stripe_charge,
        amount=amount_in_cents,
        currency=currency,
        stripe_token=stripe_token
    )
    
    return payment_intent