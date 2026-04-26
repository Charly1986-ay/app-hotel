from sqlmodel import select

from app.models.user import User

class UserRepository:
    def __init__(self, db):
        self.db=db

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
    
    def get_by_email(self, email: str) -> User | None:
        return self.db.exec(
            select(User).where(User.email == email)).first()
    
    def create(self, user: User) -> User:
        self.db.add(user)
        # self.db.flush()
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user: User, updates: dict) -> User:        
        for key, value in updates.items():
            setattr(user, key, value)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
