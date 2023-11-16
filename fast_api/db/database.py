from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
from fastapi import FastAPI
from ..config.config import settings


def build_connection_string():
    return f"""
    dbname={settings.POSTGRES_DB}
    user={settings.POSTGRES_USER}
    password={settings.POSTGRES_PASSWORD}
    host={settings.POSTGRES_HOST}
    port={settings.POSTGRES_PORT}
    """

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.async_pool = AsyncConnectionPool(conninfo=build_connection_string())
    yield
    await app.async_pool.close()
