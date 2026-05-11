from sqlmodel import select, Session

from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db=db

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
    
    def get_by_email(self, email: str) -> User | None:
        # 1. Ejecutamos la consulta con await (esto devuelve un ScalarResult)
        result = self.db.exec(select(User).where(User.email == email))
        
        # 2. Obtenemos el primer resultado
        return result.one_or_none()
    
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
