from fastapi import APIRouter, status, Depends
from schames import CartBase, UserBase
from database import engine, session
from model import Product, Users, Cart
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

session = session(bind=engine)

card_router = APIRouter(prefix="/orders")


@card_router.get('/')
async def select(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    cards = session.query(Cart).all()
    # context = [
    #     {
    #         "id": card.id,
    #         "Product": {
    #             "id": card.web_cart.id,
    #             "username": card.title_id.product_name,
    #             "email": card.title_id.description,
    #             "count": card.title_id.count
    #         },
    #
    #         "User": {
    #             "id": card.user_id.id,
    #             "name": card.user_id.first_name,
    #             "price": card.user_id.last_name
    #         },
    #     }
    #     for card in cards
    # ]
    data = {
        "code": 200,
        "msg": "Succesfully",
        "Cards": jsonable_encoder(cards)
    }
    return data


@card_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(card: CartBase, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    check_card = session.query(Cart).filter(Cart.id == card.id).first()
    check_user_id = session.query(Users).filter(Users.id == card.user_id).first()
    check_title_id = session.query(Product).filter(Product.id == card.title_id).first()

    if check_card:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Card with this ID already exists")

    if not check_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id does not exist")

    if not check_title_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="title_id does not exist")
    new_card = Cart(
        id=card.id,
        title_id=card.title_id,
        user_id=card.user_id
    )
    session.add(new_card)
    session.commit()
    session.refresh(new_card)

    # data = {
    #     "code": 201,
    #     "msg": "Successfully",
    #     "Product": {
    #         "id": new_card.id,
    #         "product_name": new_card.product_name,
    #         "price": new_card.price,
    #         "description": new_card.description,
    #         "category_code": new_card.category_code,
    #         "category_name": new_card.category_name,
    #         "subcategory_code": new_card.description,
    #         "subcategory_name": new_card.subcategory_name,
    #     },
    #     "User": {
    #         "id": new_card.id,
    #         "first_name": new_card.first_name,
    #         "last_name": new_card.last_name,
    #     }
    # }
    data = {
        "code": 200,
        "msg": "Succesfully",
        "Cards": jsonable_encoder(new_card)
    }
    return data


@card_router.post('/user/order')
async def user_order(user_order: UserBase, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    check_user = session.query(Users).filter(Users.username == user_order.username).first()
    if check_user.is_staff:
        check_order = session.query(Cart).filter(Cart.user_id == check_user.id)
        if check_order:
            context = [
                {
                    "id": order.id,
                    "user": {
                        "id": order.users.id,
                        "username": order.users.username,
                        "email": order.users.email
                    },
                    "count": order.count,
                    "product": {
                        "id": order.products.id,
                        "name": order.products.name,
                        "price": order.products.price
                    },
                    "Jami summa": order.count * order.product.price
                }
                for order in check_order
            ]
            return jsonable_encoder(context)
        else:
            return HTTPException(status_code=status.HTTP_200_OK, detail="Savat bosh")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ma'lumotlarni faqat admin ko'rish mumkin")
