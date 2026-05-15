import uuid

import stripe

from app.core.exceptions import PaymentException

def create_payment_method(type_card: str, card: dict) -> str:
    try:
        payment_method = stripe.PaymentMethod.create(type=type_card, card=card)

        return payment_method.id
    except stripe.StripeError as e:
        print(f'Error de stripe: {e.user_message}')


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
        card: dict
) -> stripe.PaymentIntent | None:
    
    payment_method_id = create_payment_method(type_card=type_card, card=card)
    
    if payment_method_id:
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency=currency,
                payment_method=payment_method_id,
                confirm=True,
                # Esto evita cobros dobles si hay un reintento por error de red
                idempotency_key=f"booking_{uuid.uuid4()}", 
                automatic_payment_methods={
                    "enabled": True,
                    "allow_redirects": "never" # Importante para APIs puras
                }
            )
            return payment_intent
        except stripe.error.CardError as e:
            # Errores del cliente (ej: no hay plata)
            print(f"Error de cliente: {e.user_message}")
            raise PaymentException(detail=e.user_message)
        except stripe.error.StripeError:
            # Errores de conexión o del sistema de Stripe
            raise PaymentException(detail="Servicio de pagos no disponible temporalmente")
    else:
        print('No se pudo crear un método de pago')