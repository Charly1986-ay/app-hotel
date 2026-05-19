import uuid

import stripe

from app.core.config import settings
from app.core.exceptions import PaymentException

# 2. ASIGNA LA CLAVE GLOBALMENTE
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_method(type_card: str, card: dict) -> str | None:
    try:
        # 'card' ahora contiene {"token": "tok_XXXX"} gracias a BookingServices.
        # Stripe acepta este diccionario feliz de la vida.
        payment_method = stripe.PaymentMethod.create(
            type=type_card, 
            card=card
        )
        return payment_method.id
    except stripe.error.StripeError as e:  # <-- IMPORTANTE: Usa stripe.error.StripeError
        print(f'Error de stripe al crear Payment Method: {e.user_message}')
        return None


# currency = 'usd', 'eur' o 'ar'
# type_card = 'card'
""" 
    card_data = {
        "number": "4242424242424242",
        "exp_month": 12,
        "exp_year": 2027,
        "cvc": "123"
    }    
    card = card_data
"""
def create_payment(
        amount: int, 
        currency: str, 
        type_card: str, 
        card: dict  # Recibe {"token": "tok_XXXX"} desde BookingServices
) -> stripe.PaymentIntent | None:
    
    # Se lo reenvía a la función de arriba sin tocar nada
    payment_method_id = create_payment_method(type_card=type_card, card=card)
    
    if payment_method_id:
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency=currency,
                payment_method=payment_method_id,
                confirm=True,
                idempotency_key=f"booking_{uuid.uuid4()}", 
                automatic_payment_methods={
                    "enabled": True,
                    "allow_redirects": "never" 
                }
            )
            return payment_intent
            
        except stripe.error.CardError as e:
            print(f"Error de cliente: {e.user_message}")
            raise PaymentException(detail=e.user_message)
            
        except stripe.error.StripeError as e:  # <-- Agrega el "as e" por si quieres printearlo
            print(f"Error general de Stripe: {e.user_message}")
            raise PaymentException(detail="Servicio de pagos no disponible temporalmente")
    else:
        print('No se pudo crear un método de pago')
        return None  # <-- Agrega este return por buena práctica si falla