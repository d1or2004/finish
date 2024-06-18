from fastapi import APIRouter, status, Depends
from schames import UserBase, LoginSchames
from database import engine, session
from model import Users
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
import datetime
from fastapi_jwt_auth import AuthJWT

session = session(bind=engine)
auth_router = APIRouter(prefix="/auth")


@auth_router.get('/')
async def list(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    users = session.query(Users).all()
    context = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "password": user.password,
            "is_staff": user.is_staff
        }
        for user in users
    ]
    return jsonable_encoder(context)


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: UserBase):
    db_email = session.query(Users).filter(Users.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu emaildan oldin ro'yxatdan o'tkazilgan")
    db_username = session.query(Users).filter(Users.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu username mavjud")

    new_user = Users(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        telegram_id=user.telegram_id

    )
    session.add(new_user)
    session.commit()
    return user


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginSchames, Authorize: AuthJWT = Depends()):
    db_user = session.query(Users).filter(Users.username == user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_lifetime = datetime.timedelta(minutes=60)
        refresh_lifetime = datetime.timedelta(days=1)
        access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        refresh_token = Authorize.create_access_token(subject=db_user.username, expires_time=refresh_lifetime)
        token = {
            "access token": access_token,
            "refresh token": refresh_token
        }
        response = {
            "code": 200,
            "success": True,
            "msg": "User successfully login",
            "id": db_user.id,
            "staf": db_user.is_staff,
            "token": token
        }
        return jsonable_encoder(response)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parol yoki username noto'g'ri ")
