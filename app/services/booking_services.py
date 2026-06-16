from fastapi import BackgroundTasks
# 1. Importamos la extensión asíncrona de SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import date

from app.models.user import User
from app.services.mail_services import generate_booking_invoice_html, send_email_base
from app.utils.utils_dates import compare_to_date

from app.models.booking import Booking, BookingCreate
from app.models.payment import Payment, PaymentStatus
from app.repository.booking_repository import BookingRepository
from app.repository.room_repository import RoomRepository

# Asumimos que vas a implementar/usar la versión async de tu cliente de Stripe
from app.services.stripe_services import create_payment
from app.core.exceptions import PaymentException, RoomNotFound


class BookingServices:
    # 2. Tipamos el constructor para recibir AsyncSession
    def __init__(self, db: AsyncSession):
        self.booking_repository = BookingRepository(db=db)
        self.room_repository = RoomRepository(db=db)

    # 3. Convertimos el método principal en 'async def'
    async def create_reservation(
            self, 
            booking: BookingCreate, 
            type_card: str, 
            token_id: str,
            currency: str,
            user: User,                       
            background_tasks: BackgroundTasks
    ) -> Booking:
        # Validar las fechas (operación local de CPU, se queda igual)
        if (compare_to_date(booking.check_in)) or (
            compare_to_date(booking.check_out)): raise PaymentException()

        # Validar que existan IDs de habitaciones
        if not booking.room_ids:
            raise RoomNotFound()
        
        total = 0
        rooms_to_assign = []

        # 4. Buscamos las habitaciones en la DB de manera asíncrona
        for room_id in booking.room_ids:
            # Agregamos 'await' porque el repositorio ahora es asíncrono
            room = await self.room_repository.get(room_id=room_id)  
            if not room:
                raise RoomNotFound()         
            total += room.price
            rooms_to_assign.append(room)        

        # 5. Pasarela de pagos (CRÍTICO: Agregar 'await' para no congelar el servidor mientras responde Stripe)
        payment_intent = await create_payment(
            amount = total,
            currency = currency,
            type_card = type_card,
            card = {'token': token_id}
        )

        if payment_intent is None:
            raise PaymentException()
        
        else: 
            # Instanciamos los objetos (operación local en memoria)
            booking_db = Booking(
                check_in = booking.check_in,
                check_out = booking.check_out,
                user_id = booking.user_id,
                rooms = rooms_to_assign
            )

            payment_db = Payment(
                user_id = booking.user_id,
                booking_id = booking_db,
                amount = total,
                currency = currency,
                stripe_payment_intent_id = payment_intent.id,
                status = PaymentStatus.COMPLETED
            )

            # 6. Guardamos de manera transaccional usando 'await'
            saved_booking = await self.booking_repository.save_all(
                booking_obj=booking_db, 
                payment_obj=payment_db
            )

            # 7. Preparación del comprobante (operaciones en memoria, se quedan igual)
            rooms_names = ", ".join([r.name for r in rooms_to_assign]) if hasattr(rooms_to_assign[0], 'name') else "Habitación de Hotel"

            html_invoice = generate_booking_invoice_html(
                customer_name=user.full_name,
                room_name=rooms_names,
                check_in=str(booking_db.check_in),
                check_out=str(booking_db.check_out),
                total_price=total
            )

            # El Background Task de FastAPI funciona perfecto tanto con funciones sync como async
            background_tasks.add_task(
                send_email_base,
                email_destination=user.email,
                subject=f"Confirmación de Reserva - Pago Exitoso 🏨",
                body_html=html_invoice
            )

            return saved_booking
        

    # 8. También convertimos a asíncrono el método de consulta de disponibilidad
    async def get_all_available_rooms_services(self, start: date, end: date) -> list:
        return await self.booking_repository.get_all_available_rooms(
            start=start,
            end=end
        )