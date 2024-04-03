from fastapi import HTTPException, status


class BookingException(HTTPException):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 500  # <-- значения по умолчанию
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"
    
class IncorrectEmailOrPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"
        
class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Срок действия токена истек"
        
class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"
        
class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"
        
class UserIsNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    
class UserHasNotPermissionsException(BookingException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="У вас недостаточно прав"
    
class RoomCannotBeBookedException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Не осталось свободных номеров"
    
class BookingIsNotExistException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Такой брони не существует"