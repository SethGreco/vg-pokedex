from fastapi import FastAPI, Request, status
from fastapi.openapi.utils import get_openapi
from fast_api.routers import health
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

app = FastAPI()

app.include_router(health.router, prefix="/api/v1", tags=["Health"])


@app.get("/")
async def hello():
    """
    Default endpoint for now
    TO BE DELETED
    """
    return "hello world"



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req: Request, exec: RequestValidationError):
    """
    Override the default 422 with 400
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exec.errors()})
    )

