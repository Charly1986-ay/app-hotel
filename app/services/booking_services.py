from fastapi import BackgroundTasks
from sqlmodel import Session

from datetime import date

from app.models.user import User
from app.services.mail_services import generate_booking_invoice_html, send_email_base
from app.utils.utils_dates import compare_to_date

from app.models.booking import Booking, BookingCreate
from app.models.payment import Payment, PaymentStatus
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
            #payment: PaymentCreate, 
            type_card: str, 
            token_id: str,
            currency: str,
            user: User,                       
            background_tasks: BackgroundTasks
    ):
        # Validar las fechas
        if (compare_to_date(booking.check_in)) or (
            compare_to_date(booking.check_out)): raise PaymentException()

        # Validar que existan IDs de habitaciones
        if not booking.room_ids:
            raise RoomNotFound()
        
        total = 0
        rooms_to_assign = []

        # calculamos la reserva
        for room_id in booking.room_ids:
            room = self.room_repository.get(room_id=room_id)  
            if not room:
                raise RoomNotFound()         
            total += room.price
            rooms_to_assign.append(room)        

        # creamos el stripe services
        payment_intent = create_payment(
            amount = total,
            currency = currency,
            type_card = type_card,
            card = {'token': token_id}
        )

        if payment_intent is None:
            raise PaymentException()
        
        else: 
            # instanceamos la reserva
            booking_db = Booking(
                check_in = booking.check_in,
                check_out = booking.check_out,
                user_id = booking.user_id,
                rooms = rooms_to_assign
            )

            # instanceamos el pago
            payment_db = Payment(
                user_id = booking.user_id,
                booking_id = booking_db,
                amount = total,
                currency = currency,
                stripe_payment_intent_id = payment_intent.id,
                status = PaymentStatus.COMPLETED
            )

            # Guardamos todo en la base de datos de manera transaccional
            saved_booking = self.booking_repository.save_all(
                booking_obj=booking_db, 
                payment_obj=payment_db
            )

            # 🛠️ 3. PREPARACIÓN Y ENCOLA_DO DEL COMPROBANTE DE PAGO
            
            # Formateamos los nombres de las habitaciones asignadas (ej: "Suite 101, Doble 102")
            rooms_names = ", ".join([r.name for r in rooms_to_assign]) if hasattr(rooms_to_assign[0], 'name') else "Habitación de Hotel"

            # Generamos el molde de la factura usando los datos en memoria
            html_invoice = generate_booking_invoice_html(
                customer_name=user.full_name,
                room_name=rooms_names,
                check_in=str(booking_db.check_in),
                check_out=str(booking_db.check_out),
                total_price=total
            )

            # Mandamos a la cola de fondo el mail para que se despache sin trabar la respuesta de la API
            background_tasks.add_task(
                send_email_base,
                email_destination=user.email,
                subject=f"Confirmación de Reserva - Pago Exitoso 🏨",
                body_html=html_invoice
            )

            return saved_booking
        

    def get_all_available_rooms_services(self, start: date, end: date):
        return self.booking_repository.get_all_available_rooms(
            start=start,
            end=end
        )