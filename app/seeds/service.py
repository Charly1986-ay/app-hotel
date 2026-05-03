from contextlib import contextmanager

from pwdlib import PasswordHash
from sqlmodel import Session, select

from app.core.db import engine, init_db
from app.models.booking import Booking
from app.seeds.data.user import USERS
from app.seeds.data.room import ROOMS
from app.seeds.data.booking import BOOKINGS
from app.models.user import User
from app.models.room import Room, StatusRoom


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
            # Evitamos duplicados buscando por el nombre de la imagen
            obj = db.exec(select(Room).where(Room.image == data['image'])).first()
            if not obj:
                db.add(Room(
                    bed_count=data['bed_count'],
                    max_capacity=data['max_capacity'],
                    price=data['price'],
                    image=data.get('image'),
                    type_room=data.get('type_room'),
                    # Si el seed dice que es 'occupied', lo respetamos, si no, 'available'
                    status=data.get('status', StatusRoom.AVAILABLE)
                ))
            else:
                # Opcional: Actualizar el estado si ya existe para resetear el test
                if data.get('status'):
                    obj.status = data.get('status')
                    db.add(obj)

def seed_bookings(db: Session) -> None:
    with atomic(db):
        for data in BOOKINGS:
            # 1. Buscamos al usuario (usando el offset o email)
            # Para este ejemplo de test, asumimos que los IDs coinciden con tu lista de seeds
            user = db.exec(select(User).where(User.id == data['user_id'])).first()
            
            # 2. Buscamos una habitación disponible para este booking
            # En un test real, podrías asignar la habitación 1 al booking 1, etc.
            room = db.exec(select(Room).where(Room.id == data['user_id'])).first()

            if user and room:
                # Comprobamos si la reserva ya existe para no duplicar
                exists = db.exec(select(Booking).where(
                    Booking.user_id == user.id, 
                    Booking.check_in == data['check_in']
                )).first()
                
                if not exists:
                    db.add(Booking(
                        check_in=data['check_in'],
                        check_out=data['check_out'],
                        user_id=user.id,
                        status=data['status'],
                        rooms=[room] # Relación N:M
                    ))


def run_all() -> None:
    init_db()
    with Session(engine) as db:
        seed_users(db)
        seed_rooms(db)
        seed_bookings(db)

def run_users() -> None:
    with Session(engine) as db:
        seed_users(db)

def run_rooms() -> None:
    with Session(engine) as db:
        seed_rooms(db)

def run_booking() -> None:
    with Session(engine) as db:
        seed_bookings(db)