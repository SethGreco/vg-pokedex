from fastapi import FastAPI, Request, status
from fastapi.openapi.utils import get_openapi
from fast_api.routers import health, pokedex, title
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fast_api.db.database import lifespan
from fast_api.models.schema import ErrorResponse



app = FastAPI(lifespan=lifespan,
              title="Filler", 
              description="Filler",
              version="3.1.0",
              responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse}})

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(pokedex.router, prefix="/api/v1", tags=["Pokedex"])
app.include_router(title.router, prefix="/api/v1", tags=["Title"])



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req: Request, exec: RequestValidationError):
    """
    Override the default 422 with 400
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exec.errors()})
    )


def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
        return app.openapi_schema


app.openapi = custom_openapi