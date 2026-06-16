import uuid
import stripe
from app.core.config import settings
from app.core.exceptions import PaymentException

# 1. En lugar de usar la clave global, instanciamos el cliente asíncrono oficial
stripe_client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)


# 2. Convertimos a 'async def'
async def create_payment_method(type_card: str, card: dict) -> str | None:
    try:
        # 3. Usamos 'await' y llamamos a través del cliente asíncrono
        payment_method = await stripe_client.payment_methods.create(
            type=type_card, 
            card=card
        )
        return payment_method.id
    except stripe.error.StripeError as e:
        print(f'Error de stripe al crear Payment Method: {e.user_message}')
        return None


async def create_payment(
        amount: int, 
        currency: str, 
        type_card: str, 
        card: dict  # Recibe {"token": "tok_XXXX"}
) -> stripe.PaymentIntent | None:
    
    # 4. CRÍTICO: Agregar 'await' al llamar a la función de arriba
    payment_method_id = await create_payment_method(type_card=type_card, card=card)
    
    if payment_method_id:
        try:
            # 5. Usamos 'await' y el cliente asíncrono para generar el cobro
            payment_intent = await stripe_client.payment_intents.create(
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
            
        except stripe.error.StripeError as e:
            print(f"Error general de Stripe: {e.user_message}")
            raise PaymentException(detail="Servicio de pagos no disponible temporalmente")
    else:
        print('No se pudo crear un método de pago')
        return None