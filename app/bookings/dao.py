from datetime import date
from app.dao.base import BaseDAO
from app.hotels.models import Room
from sqlalchemy import and_, delete, func, insert, or_, select
from exceptions import UserHasNotPermissionsException

from app.bookings.models import Booking
from app.database import async_session_maker, engine


class BookingDAO(BaseDAO):
    
    model = Booking
    
    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            """
                with booked_rooms as (
                    select * from booking
                    where room_id = 1 AND
                    (
                        (date_from >= '2024-06-15' and date_from <= '2024-06-20')
                        OR
                        (date_from <= '2024-06-15' and date_to >= '2024-06-20')
                        OR
                        (date_to >= '2024-06-15' and date_to <= '2024-06-20')
                    )
                )
                SELECT (room.quantity - COUNT(br.room_id))
                FROM room JOIN booked_rooms as br
                ON room.id = br.room_id
                GROUP BY room.quantity, br.room_id;
            """
            
            booked_rooms = select(Booking).where(
                and_(
                    Booking.room_id == room_id,
                    or_(
                        and_(
                            Booking.date_from >= date_from,
                            Booking.date_from <= date_to
                        ),
                        and_(
                            Booking.date_from <= date_from,
                            Booking.date_to >= date_to
                        ),
                        and_(
                            Booking.date_to >= date_from,
                            Booking.date_to <= date_to
                        )
                    )
                )
            ).cte("booked_rooms")
            
            get_available_rooms_quantity = select(
                    (Room.quantity - func.count(booked_rooms.c.id))
                ).select_from(Room).outerjoin(
                    booked_rooms, booked_rooms.c.room_id == Room.id
                ).where(Room.id == room_id).group_by(
                    Room.quantity, booked_rooms.c.room_id
                )
                
            print(get_available_rooms_quantity.compile(engine, compile_kwargs={"literal_binds": True}))
            
            available_rooms_quantity = await session.execute(get_available_rooms_quantity)
            
            available_rooms_quantity: int = available_rooms_quantity.scalar()
            
            if available_rooms_quantity > 0:
                get_price = select(Room.price).filter(Room.id == room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                
                add_booking = insert(cls.model).values(
                    user_id=user_id,
                    room_id=room_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(cls.model)
                
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
                
            else:
                return None
            
            
    @classmethod
    async def delete_booking(cls, booking_id: int, user_id: int):
        async with async_session_maker() as session:
            
            query = select(cls.model.__table__.columns).filter(cls.model.id == booking_id)
            result = await session.execute(query)
            result = result.mappings().one_or_none()
            if not result:
                return None
            else:
                if user_id != result.user_id:
                    raise UserHasNotPermissionsException
                else:
                    query = delete(cls.model).where(cls.model.id == booking_id)
                    await session.execute(query)
                    await session.commit()
                    return {"message": "deleted"}
            
            
        
            
            
    