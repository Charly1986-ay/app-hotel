from contextlib import asynccontextmanager
from pwdlib import PasswordHash
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.db import engine, init_db
from app.models.booking import Booking, StatusBooking
from app.models.supply import Supply
from app.seeds.data.user import USERS
from app.seeds.data.room import ROOMS
from app.seeds.data.booking import BOOKINGS
from app.seeds.data.supply import SUPPLIES
from app.models.user import User
from app.models.room import Room, StatusRoom

@asynccontextmanager
async def atomic(db: AsyncSession):
    try:
        yield
        await db.commit()
    except Exception:
        await db.rollback()
        raise


def get_hex(name: str) -> str:
    return hex(id(name))


def hash_password(plain: str) -> str:
    return PasswordHash.recommended().hash(plain)


async def _user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.exec(select(User).where(User.email == email))
    return result.first()


async def seed_users(db: AsyncSession) -> None:
    async with atomic(db):
        for data in USERS:
            obj = await _user_by_email(db, data['email'])
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


async def seed_rooms(db: AsyncSession) -> None:
    async with atomic(db):
        for data in ROOMS:
            result = await db.exec(select(Room).where(Room.image == data['image']))
            obj = result.first()

            if not obj:
                room_data = data.copy()
                if 'status' not in room_data:
                    room_data['status'] = StatusRoom.AVAILABLE
                db.add(Room(**room_data))
            else:
                if data.get('status'):
                    obj.status = data.get('status')
                    db.add(obj)


async def seed_bookings(db: AsyncSession) -> None:
    async with atomic(db):
        for data in BOOKINGS:
            # 1. Extraemos los valores de forma segura
            user_id = data.get('user_id')
            room_id = data.get('room_id')
            check_in = data.get('check_in')
            check_out = data.get('check_out')

            # Si faltan datos vitales en este diccionario de BOOKINGS, lo saltamos silenciosamente
            if not user_id or not room_id or not check_in:
                continue

            # 2. Buscamos el usuario
            user_result = await db.exec(select(User).where(User.id == user_id))
            user = user_result.first()
            
            # 3. Buscamos la habitación
            room_result = await db.exec(select(Room).where(Room.id == room_id))
            room = room_result.first()

            # 4. Si ambos existen en la BD, procedemos
            if user and room:
                # Comprobamos idempotencia: que este usuario no tenga ya una reserva en esa fecha exacta
                exists_result = await db.exec(select(Booking).where(
                    Booking.user_id == user.id, 
                    Booking.check_in == check_in
                ))
                exists = exists_result.first()
                
                if not exists:
                    # Instanciamos el Booking. Como tu modelo soporta rooms=[room], 
                    # SQLModel se encargará de insertar automáticamente la fila en 'bookingroom'
                    db.add(Booking(
                        check_in=check_in,
                        check_out=check_out,
                        user_id=user.id,
                        status=data.get('status', StatusBooking.CONFIRMED.value),
                        rooms=[room] 
                    ))


async def seed_supplies(db: AsyncSession) -> None:
    async with atomic(db):
        for data in SUPPLIES:
            result = await db.exec(select(Supply).where(Supply.name == data['name']))
            obj = result.first()

            if not obj:
                supply_db = Supply(**data)
                db.add(supply_db)
            


async def run_all() -> None:
    await init_db()  
    async with AsyncSession(engine) as db:
        await seed_users(db)
        await seed_rooms(db)
        await seed_bookings(db)
        await seed_supplies(db)

async def run_users() -> None:
    async with AsyncSession(engine) as db:
        await seed_users(db)

async def run_rooms() -> None:
    async with AsyncSession(engine) as db:
        await seed_rooms(db)

async def run_booking() -> None:
    async with AsyncSession(engine) as db:
        await seed_bookings(db)

async def run_supplies() -> None:
    async with AsyncSession(engine) as db:
        await seed_supplies(db)