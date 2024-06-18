from fastapi import APIRouter, status, Depends
from schames import ProductBase
from database import engine, session
from model import Product, Users
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from database import SessionLocal

session = session(bind=engine)
product_router = APIRouter(prefix="/product")


@product_router.get('/')
async def list(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    products = session.query(Product).all()
    context = [
        {
            "id": product.id,
            "product_name": product.product_name,
            "price": product.price,
            "description": product.description,
            "category_code": product.category_code,
            "category_name": product.category_name,
            "subcategory_code": product.subcategory_code,
            "subcategory_name": product.subcategory_name
        }
        for product in products
    ]
    return jsonable_encoder(context)


@product_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(product: ProductBase, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == current_user).first()

    if user and user.is_staff:
        check_product = session.query(Product).filter(Product.id == product.id).first()
        if check_product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with this ID already exists")

        new_product = Product(
            id=product.id,
            product_name=product.product_name,
            image=product.image,
            price=product.price,
            description=product.description,
            category_code=product.category_code,
            category_name=product.category_name,
            subcategory_code=product.subcategory_code,
            subcategory_name=product.subcategory_name,
        )

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        data = {
            "code": 201,
            "msg": "Success",
            "Product": jsonable_encoder(new_product)
        }
        return data

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only ADMIN can modify data")


@product_router.get('/{id}')
async def category_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == current_user).first()
    if user.is_staff:
        check_product = session.query(Product).filter(Product.id == id).first()
        if check_product:
            return jsonable_encoder(check_product)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday id ga ega product yo'q")
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumotlarni faqat Admin o'zgartirish mumkin")


@product_router.put('/{product_id}', status_code=status.HTTP_200_OK)
async def update(product_id: int, product: ProductBase, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == current_user).first()
    if user.is_staff:
        db_product = session.query(Product).filter(Product.id == product_id).first()
        if db_product:
            db_product.product_name = product.product_name
            db_product.image = product.image
            db_product.price = product.price
            db_product.description = product.description
            db_product.category_code = product.category_code
            db_product.category_name = product.category_name
            db_product.subcategory_code = product.subcategory_code
            db_product.subcategory_name = product.subcategory_name

            session.commit()
            session.refresh(db_product)

            return {
                "code": 200,
                "msg": "Product update successfully",
                "Product": db_product
            }
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday category_id mavjud emas")
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumotlarni faqat Admin o'zgartirish mumkin")


@product_router.delete('/{product_id}', status_code=status.HTTP_200_OK)
async def delete(product_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == current_user).first()
    if user.is_staff:
        db_product = session.query(Product).filter(Product.id == product_id).first()

        if not db_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        session.delete(db_product)
        session.commit()

        return {
            "msg": "Product deleted successfully"
        }
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumotlarni faqat Admin o'zgartirish mumkin")


