from typing import Annotated
from fastapi import FastAPI, Request, status, Depends, HTTPException
from fastapi.openapi.utils import get_openapi
from fast_api.routers import health, pokedex, title
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fast_api.db.database import lifespan
from fast_api.models.schema import ErrorResponse, User

# example code for security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI(lifespan=lifespan,
              title="Filler",
              description="Filler",
              version="3.1.0",
              responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse}}
              )

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(pokedex.router, prefix="/api/v1", tags=["Pokedex"])
app.include_router(title.router, prefix="/api/v1", tags=["Title"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req: Request,
                                       exec: RequestValidationError):
    """
    Override the default 422 with 400
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exec.errors()})
    )


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


# example security code
def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserInDB(User):
    hashed_password: str


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe"
    )


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.get("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema
    app.openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    )
    for _, method_item in app.openapi_schema.get('paths').items():
        for _, param in method_item.items():
            responses = param.get('responses')
            # remove 422 response, also can remove other status code
            if '422' in responses:
                del responses['422']
    return app.openapi_schema


app.openapi = custom_openapi
