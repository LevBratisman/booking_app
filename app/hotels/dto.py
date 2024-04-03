from pydantic import BaseModel

class SHotel(BaseModel):
    name: str
    location: str
    services: list
    room_quantity: int
    
class SHotelFullInfo(SHotel):
    id: int
    image_id: int