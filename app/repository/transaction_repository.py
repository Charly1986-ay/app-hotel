from sqlmodel import select, Session

from app.models.transaction import Transaction

from datetime import date

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db


    def get(self, transaction_id: int) -> Transaction | None:
        return self.db.get(Transaction, transaction_id)
    
    
    def get_check_in(self, check_in: date) -> Transaction | None:
        return self.db.exec(
            select(Transaction).where(Transaction.check_in == check_in)).all()
    

    def get_check_out(self, check_out: date) -> Transaction | None:
        return self.db.exec(
            select(Transaction).where(Transaction.check_out == check_out)).all()
    

    def create(self, transaction: Transaction) -> Transaction:
        self.db.add(transaction)
        self.db.flush()
        #self.db.commit()
        self.db.refresh(transaction)
        return transaction
    

    def update(self, transaction: Transaction, updates: dict) -> Transaction:        
        for key, value in updates.items():
            setattr(transaction, key, value)

        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction