from fastapi import FastAPI
from auth import auth_router
from product_router import product_router
from card import card_router
from schames import Settings
from fastapi_jwt_auth import AuthJWT

app = FastAPI()
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(card_router)


@AuthJWT.load_config
def get_cofig():
    return Settings()


@app.get("/")
def read_root():
    return {"Hello": "World"}
