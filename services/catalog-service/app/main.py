"""Catalog Service — управление товарным каталогом маркетплейса."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import health, products


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Catalog Service",
    description="Управление товарным каталогом для продавцов маркетплейса",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(products.router, prefix="/api/v1")
