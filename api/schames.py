from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional, Any


class UserBase(BaseModel):
    id: Optional[int] = None
    first_name: Optional[constr(max_length=100)] = None
    last_name: Optional[constr(max_length=100)] = None
    email: Optional[EmailStr] = None
    username: constr(max_length=100)
    password: str
    is_staff: Optional[bool] = Field(False)
    telegram_id: Optional[int]

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    id: Optional[int] = None
    product_name: str = Field(..., max_length=100)
    image: Optional[str] = None
    price: float = Field(..., gt=0)
    description: str = Field(..., max_length=300)
    category_code: str = Field(..., max_length=100)
    category_name: str = Field(..., max_length=100)
    subcategory_code: str = Field(..., max_length=100)
    subcategory_name: str = Field(..., max_length=100)


class CartBase(BaseModel):
    id: Optional[int]
    title_id: int
    user_id: int


class LoginSchames(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = "fcdaea536afe16410c7f2dccf14214306fede5ea3aa8b9456366d84147efd34d"
