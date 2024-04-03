from app.dao.base import BaseDAO
from app.hotels.dto import SHotel
from app.hotels.models import Hotel
from sqlalchemy import or_, select
from app.database import async_session_maker


class HotelDAO(BaseDAO):
    model = Hotel
    
    @classmethod
    async def get_hotels_by_location(cls, location: str) -> list[SHotel]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(
                or_(
                    cls.model.location.like(f'%{location}%'),
                    cls.model.location.like(f'%{location.capitalize()}%'),
                    cls.model.location.like(f'%{location.lower()}%'),
                    cls.model.location.like(f'%{location.upper()}%'),
                    )
                )
            result = await session.execute(query)
            return result.mappings().all()