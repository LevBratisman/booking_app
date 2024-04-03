from datetime import date
from typing import Optional
from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel
import uvicorn

from app.bookings.router import router as booking_router
from app.users.router import auth_router 
from app.users.router import user_router
from app.hotels.router import hotel_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(hotel_router)
app.include_router(booking_router)


def run():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    
    
if __name__ == "__main__":
    run()