from datetime import date
from app.bookings.dao import BookingDAO
from app.bookings.dto import SBooking
from app.users.dependencies import get_current_user
from app.users.models import User
from exceptions import RoomCannotBeBookedException, BookingIsNotExistException
from fastapi import APIRouter, Depends

from app.bookings.models import Booking


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.get("")
async def get_bookings(user: User = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.get_all(Booking.user_id == user.id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date, 
    date_to: date,
    user: User = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException
    
    
@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: User = Depends(get_current_user)):
    result = await BookingDAO.delete_booking(booking_id, user.id)
    if not result:
        raise BookingIsNotExistException
    else:
        return result

