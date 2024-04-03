from jose import jwt

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from app.users.dao import UserDAO
from app.users.dto import SUserAuth
from app.users.models import User

from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(user_data: SUserAuth):
    user = await UserDAO.get_one_or_none(User.email==user_data.email)
    if user and verify_password(user_data.password, user.hashed_password):
        return user
    return None