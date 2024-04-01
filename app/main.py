from datetime import date
from typing import Optional
from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel
import uvicorn

from app.bookings.router import router as booking_router

app = FastAPI()

app.include_router(booking_router)


class HotelSearchArgs():
    def __init__(
        self, 
        location: str, 
        date_to: date, 
        date_from: date, 
        has_spa: Optional[bool] = None, 
        stars: Optional[int] = Query(None, ge=1, le=5)
    ):
        self.location = location
        self.date_to = date_to
        self.date_from = date_from
        self.has_spa = has_spa
        self.stars = stars


class SHotel(BaseModel):
    name: str
    stars: int
    has_spa: bool
    location: str

@app.get("/hotels")
def get_hotels(args: HotelSearchArgs = Depends()):
    return args
    
    
class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    
    
@app.post("/bookings")
def add_booking(booking: SBooking):
    pass
    


def run():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    
    
if __name__ == "__main__":
    run()