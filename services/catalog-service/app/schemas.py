import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    seller_id: uuid.UUID
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    category: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0, default=0)


class ProductUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    category: str | None = Field(default=None, min_length=1, max_length=100)
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    seller_id: uuid.UUID
    title: str
    description: str | None
    category: str
    price: Decimal
    stock: int
    created_at: datetime
    updated_at: datetime


class StockReserveRequest(BaseModel):
    quantity: int = Field(gt=0)


class StockReserveResponse(BaseModel):
    product_id: uuid.UUID
    reserved: int
    remaining_stock: int
