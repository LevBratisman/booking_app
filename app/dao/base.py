from sqlalchemy import select

from app.database import async_session_maker


class BaseDAO:
    
    model = None
    
    @classmethod
    async def get_by_id(cls, model_id: int) -> dict | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.id == model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()
    
    @classmethod
    async def get_one_or_none(cls, *filters) -> dict | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(*filters)
            result = await session.execute(query)
            return result.mappings().one_or_none()
    
    @classmethod
    async def get_all(cls, *filters) -> list[dict]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns, (cls.model.id*2).label("double_cost")).filter(*filters)
            result = await session.execute(query)
            return result.mappings().all()