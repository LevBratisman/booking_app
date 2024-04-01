from app.bookings.dao import BookingDAO
from app.bookings.dto import SBooking, BookingWithColumn
from fastapi import APIRouter

from app.bookings.models import Booking
from sqlalchemy import select


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.get("")
async def get_bookings() -> list[SBooking]:
    return await BookingDAO.get_all()

@router.get("/{booking_id}")
async def get_booking(booking_id: int) -> SBooking | None:
    return await BookingDAO.get_by_id(booking_id)
