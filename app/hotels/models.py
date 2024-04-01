from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotel(Base):
    __tablename__ = "hotel"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name = Mapped[str] = mapped_column(String(150), nullable=False)
    location = Mapped[str] = mapped_column(String(150), nullable=False)
    services = Mapped[dict] = mapped_column(JSON)
    room_quantity = Mapped[int] = mapped_column(Integer, nullable=False)
    image_id = Mapped[int] = mapped_column(Integer)