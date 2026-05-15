from sqlmodel import Session

from app.models.booking import Booking, BookingCreate
from app.models.payment import Payment, PaymentCreate, PaymentStatus
from app.repository.booking_repository import BookingRepository
from app.repository.room_repository import RoomRepository

from app.services.stripe_services import create_payment

from app.core.exceptions import PaymentException, RoomNotFound

class BookingServices:
    def __init__(self, db: Session):
        self.booking_repository = BookingRepository(db=db)
        self.room_repository = RoomRepository(db=db)

    def create_reservation(
            self, 
            booking: BookingCreate, 
            payment: PaymentCreate, 
            type_card: str, 
            card: str
    ):
        # 1. Validar que existan IDs de habitaciones
        if not booking.room_ids:
            raise RoomNotFound()
        
        total = 0

        # calculamos la reserva
        for room_id in booking.room_ids:
            room = self.room_repository.get(room_id=room_id)  
            if not room:
                raise RoomNotFound()         
            total += room.price        

        # creamos el stripe services
        payment_intent = create_payment(
            amount=total,
            currency=payment.currency,
            type_card=type_card,
            card = card
        )

        if payment_intent is None:
            raise PaymentException()
        
        else: 
            # instanceamos la reserva
            booking_db = Booking(
                check_in = booking.check_in,
                check_out = booking.check_out,
                user_id = booking.user_id
            )

            # instanceamos el pago
            payment_db = Payment(
                user_id = booking.user_id,
                booking_id = booking_db,
                amount = total,
                currency = payment.currency,
                stripe_payment_intent_id = payment_intent.id,
                status = PaymentStatus.COMPLETED
            )

            return self.booking_repository.save_all(
                booking_obj=booking_db, 
                payment_obj=payment_db
            )