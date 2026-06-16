from fastapi import BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import date

from app.models.user import User
from app.services.mail_services import generate_booking_invoice_html, send_email_base
from app.utils.utils_dates import compare_to_date

from app.models.booking import Booking, BookingCreate
from app.models.payment import Payment, PaymentStatus
from app.repository.booking_repository import BookingRepository
from app.repository.room_repository import RoomRepository

# Importamos tu nuevo servicio de Stripe limpio
from app.services.stripe_services import create_payment
from app.core.exceptions import PaymentException, RoomNotFound


class BookingServices:
    def __init__(self, db: AsyncSession):
        self.booking_repository = BookingRepository(db=db)
        self.room_repository = RoomRepository(db=db)

    async def create_reservation(
            self, 
            booking: BookingCreate, 
            token_id: str,     # <-- Removimos type_card porque Stripe ya deduce el tipo mediante el token
            currency: str,
            user: User,                      
            background_tasks: BackgroundTasks
    ) -> Booking:
        # Validar las fechas (Local CPU)
        if compare_to_date(booking.check_in) or compare_to_date(booking.check_out): 
            raise PaymentException()

        # Validar que existan IDs de habitaciones
        if not booking.room_ids:
            raise RoomNotFound()
        
        total = 0
        rooms_to_assign = []

        # Buscamos las habitaciones en la DB asíncronamente
        for room_id in booking.room_ids:
            room = await self.room_repository.get(room_id=room_id)  
            if not room:
                raise RoomNotFound()         
            total += room.price
            rooms_to_assign.append(room)        

        # CORRECCIÓN CRÍTICA: Llamada alineada con tu nuevo stripe_services.py
        payment_intent = await create_payment(
            amount=total,
            currency=currency,
            stripe_token=token_id  # <-- Pasamos el token limpio (string 'tok_XXXX')
        )

        if payment_intent is None:
            raise PaymentException()
        
        else: 
            # Instanciamos los objetos en memoria
            booking_db = Booking(
                check_in=booking.check_in,
                check_out=booking.check_out,
                user_id=booking.user_id,
                rooms=rooms_to_assign
            )

            payment_db = Payment(
                user_id=booking.user_id,
                booking_id=booking_db,
                amount=total,
                currency=currency,
                stripe_payment_intent_id=payment_intent.id,
                status=PaymentStatus.COMPLETED
            )

            # Guardamos de manera transaccional con await
            saved_booking = await self.booking_repository.save_all(
                booking_obj=booking_db, 
                payment_obj=payment_db
            )

            # Preparación del comprobante
            rooms_names = ", ".join([r.name for r in rooms_to_assign]) if hasattr(rooms_to_assign[0], 'name') else "Habitación de Hotel"

            html_invoice = generate_booking_invoice_html(
                customer_name=user.full_name,
                room_name=rooms_names,
                check_in=str(booking_db.check_in),
                check_out=str(booking_db.check_out),
                total_price=total
            )

            # Task en segundo plano (FastAPI administra su asincronía automáticamente)
            background_tasks.add_task(
                send_email_base,
                email_destination=user.email,
                subject=f"Confirmación de Reserva - Pago Exitoso 🏨",
                body_html=html_invoice
            )

            return saved_booking
        

    async def get_all_available_rooms_services(self, start: date, end: date) -> list:
        return await self.booking_repository.get_all_available_rooms(
            start=start,
            end=end
        )