from pwdlib import PasswordHash
from sqlmodel import select
from contextlib import asynccontextmanager
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.db import engine, init_db
from app.models.booking import Booking
from app.seeds.data.user import USERS
from app.seeds.data.room import ROOMS
from app.seeds.data.booking import BOOKINGS
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


# Agregamos async y cambiamos a db.exec para que sea asíncrono nativo
async def _user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.exec(select(User).where(User.email == email))
    return result.scalars().first()


# Cambiamos a async def y usamos "async with atomic(db):"
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
            obj = result.scalars().first()
            if not obj:
                db.add(Room(
                    bed_count=data['bed_count'],
                    max_capacity=data['max_capacity'],
                    price=data['price'],
                    image=data.get('image'),
                    type_room=data.get('type_room'),
                    status=data.get('status', StatusRoom.AVAILABLE)
                ))
            else:
                if data.get('status'):
                    obj.status = data.get('status')
                    db.add(obj)


async def seed_bookings(db: AsyncSession) -> None:
    async with atomic(db):
        for data in BOOKINGS:
            # Consultas adaptadas a exec() asíncrono
            user_result = await db.exec(select(User).where(User.id == data['user_id']))
            user = user_result.scalars().first()
            
            room_result = await db.exec(select(Room).where(Room.id == data['user_id']))
            room = room_result.scalars().first()

            if user and room:
                exists_result = await db.exec(select(Booking).where(
                    Booking.user_id == user.id, 
                    Booking.check_in == data['check_in']
                ))
                exists = exists_result.scalars().first()
                
                if not exists:
                    db.add(Booking(
                        check_in=data['check_in'],
                        check_out=data['check_out'],
                        user_id=user.id,
                        status=data['status'],
                        rooms=[room] 
                    ))


# Todos los ejecutores ahora usan "async def" y controlan la sesión asíncrona correctamente
async def run_all() -> None:
    await init_db()  # init_db ya tenía run_sync internamente
    async with AsyncSession(engine) as db:
        await seed_users(db)
        await seed_rooms(db)
        await seed_bookings(db)

async def run_users() -> None:
    async with AsyncSession(engine) as db:
        await seed_users(db)

async def run_rooms() -> None:
    async with AsyncSession(engine) as db:
        await seed_rooms(db)

async def run_booking() -> None:
    async with AsyncSession(engine) as db:
        await seed_bookings(db)