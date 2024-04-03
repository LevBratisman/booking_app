from sqlalchemy import delete, insert, select

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
            query = select(cls.model.__table__.columns).filter(*filters)
            result = await session.execute(query)
            return result.mappings().all()
        
    @classmethod
    async def add_one(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            
    @classmethod
    async def delete(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(cls.model.id == model_id)
            result = await session.execute(query)
            if not result:
                return None
            else:
                delete(cls.model).where(cls.model.id == model_id)
                await session.commit()
                return {"message": "deleted"}