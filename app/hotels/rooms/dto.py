from pydantic import BaseModel

class SRoom(BaseModel):
    name: str
    description: str
    price: int
    services: list
    quantity: int
    
class SRoomFullInfo(SRoom):
    id: int
    hotel_id: int
    image_id: int