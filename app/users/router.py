from exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from fastapi import APIRouter, Depends, HTTPException, Response

from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.models import User
from app.users.dao import UserDAO
from app.users.dto import SUserAuth
from app.users.dependencies import get_current_admin_user, get_current_user


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


##################################### AUTH ROUTER #####################################

@auth_router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.get_one_or_none(User.email==user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add_one(email=user_data.email, hashed_password=hashed_password)
    return {"message": "User created"}


@auth_router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return {"message": "User logged out"}



##################################### USER ROUTER #####################################

@user_router.get("/me")
async def read_current_user(user: User = Depends(get_current_user)):
    return user


@user_router.get("/all")
async def get_users(user: User = Depends(get_current_admin_user)):
    return await UserDAO.get_all()