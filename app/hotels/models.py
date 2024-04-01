from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotel(Base):
    __tablename__ = "hotel"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    location: Mapped[str] = mapped_column(String(150))
    services: Mapped[dict | None] = mapped_column(JSON)
    room_quantity: Mapped[int]
    image_id: Mapped[int]
    
    
class Room(Base):
    __tablename__ = "room"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id : Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
    services: Mapped[dict | None] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]