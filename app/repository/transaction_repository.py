from sqlmodel import select, Session

from app.models.payment import Payment

from datetime import date

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db


    def get(self, payment_id: int) -> Payment | None:
        return self.db.get(Payment, payment_id)
    
    
    def get_check_in(self, check_in: date) -> Payment | None:
        return self.db.exec(
            select(Payment).where(Payment.check_in == check_in)).all()
    

    def get_check_out(self, check_out: date) -> Payment | None:
        return self.db.exec(
            select(Payment).where(Payment.check_out == check_out)).all()
    

    def create(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.flush()
        #self.db.commit()
        self.db.refresh(payment)
        return payment
    

    def update(self, payment: Payment, updates: dict) -> Payment:        
        for key, value in updates.items():
            setattr(payment, key, value)

        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment