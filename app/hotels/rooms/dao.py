from app.dao.base import BaseDAO
from app.hotels.models import Room


class RoomDAO(BaseDAO):
    model = Room