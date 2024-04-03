from datetime import datetime, timezone
from app.users.dao import UserDAO
from app.users.models import User
from exceptions import IncorrectTokenFormatException, TokenAbsentException, TokenExpiredException, UserHasNotPermissionsException, UserIsNotPresentException
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError

from app.users.dto import SUser
from app.config import settings


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)) -> SUser:
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise IncorrectTokenFormatException
    
    user = await UserDAO.get_one_or_none(User.id == int(user_id))
    if not user:
        raise UserIsNotPresentException
    
    return user
    
    
async def get_current_admin_user(user: SUser = Depends(get_current_user)) -> SUser:
    if user.role != "admin":
        raise UserHasNotPermissionsException
    return user