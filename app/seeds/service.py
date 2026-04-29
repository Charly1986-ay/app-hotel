from contextlib import contextmanager

from pwdlib import PasswordHash
from sqlmodel import Session, select

from app.core.db import engine
from app.seeds.data.user import USERS
from app.seeds.data.room import ROOMS
from app.models.user import User
from app.models.room import Room


@contextmanager
def atomic(db: Session):
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise


def get_hex(name: str) -> str:
    return hex(id(name))


def hash_password(plain: str) -> str:
    return PasswordHash.recommended().hash(plain)

def _user_by_email(db: Session, email: str) -> User | None:
        return db.exec(
            select(User).where(User.email == email)).first()


def seed_users(db: Session) -> None:
    with atomic(db):
        for data in USERS:
            obj = _user_by_email(db, data['email'])
            if obj:
                changed = False
                if obj.full_name != data.get('full_name'):
                    obj.full_name = data.get('full_name')
                    changed = True
                if data.get('password'):
                    obj.hashed_password = hash_password(data['password'])
                    changed = True
                if data.get('role'):
                    obj.role = data.get('role')
                    changed = True
                if changed:
                    db.add(obj)
            else:
                db.add(User(
                    email=data['email'],
                    full_name=data.get('full_name'),
                    role=data.get('role'),
                    hashed_password=hash_password(data['password'])
                ))

def seed_rooms(db: Session) -> None:
    with atomic(db):
        for data in ROOMS:
            db.add(Room(
                bed_count = data['bed_count'],
                max_capacity=data['max_capacity'],
                price=data['price'],
                image=data.get('image'),
                type_room=data.get('type_room')
            ))


def run_all() -> None:
    with Session(engine) as db:
        seed_users(db)
        seed_rooms(db)

def run_users() -> None:
    with Session(engine) as db:
        seed_users(db)

def run_rooms() -> None:
    with Session(engine) as db:
        seed_rooms(db)