from sqlmodel import select, Session

from app.models.booking import Booking

from datetime import date

class BookingRepository:
    def __init__(self, db: Session):
        self.db = db


    def get(self, booking_id: int) -> Booking | None:
        return self.db.get(Booking, booking_id)
    
    
    def get_check_in(self, check_in: date) -> Booking | None:
        return self.db.exec(
            select(Booking).where(Booking.check_in == check_in)).all()
    

    def get_check_out(self, check_out: date) -> Booking | None:
        return self.db.exec(
            select(Booking).where(Booking.check_out == check_out)).all()
    

    def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        self.db.flush()
        #self.db.commit()
        self.db.refresh(booking)
        return booking
    

    def update(self, booking: Booking, updates: dict) -> Booking:        
        for key, value in updates.items():
            setattr(booking, key, value)

        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking