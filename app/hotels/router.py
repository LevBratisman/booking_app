from app.hotels.dao import HotelDAO
from app.hotels.dto import SHotel, SHotelFullInfo
from app.hotels.models import Hotel, Room
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.dto import SRoom, SRoomFullInfo
from fastapi import APIRouter



hotel_router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@hotel_router.get("/all")
async def get_hotels() -> list[SHotel]:
    return await HotelDAO.get_all()


@hotel_router.get("/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotelFullInfo:
    return await HotelDAO.get_by_id(hotel_id)


@hotel_router.get("/{location}")
async def get_hotels(location: str) -> list[SHotel]:
    return await HotelDAO.get_hotels_by_location(location)


@hotel_router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel(hotel_id: int) -> list[SRoomFullInfo]:
    return await RoomDAO.get_all(Room.hotel_id == hotel_id)