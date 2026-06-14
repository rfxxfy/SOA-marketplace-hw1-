import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product
from app.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    StockReserveRequest,
    StockReserveResponse,
)

router = APIRouter(tags=["products"])


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/products", response_model=list[ProductResponse])
def list_products(
    category: str | None = Query(default=None),
    seller_id: uuid.UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if seller_id:
        query = query.filter(Product.seller_id == seller_id)
    return query.order_by(Product.created_at.desc()).offset(offset).limit(limit).all()


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: uuid.UUID, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()


@router.post("/products/{product_id}/reserve", response_model=StockReserveResponse)
def reserve_stock(
    product_id: uuid.UUID,
    payload: StockReserveRequest,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < payload.quantity:
        raise HTTPException(status_code=409, detail="Insufficient stock")

    product.stock -= payload.quantity
    db.commit()
    db.refresh(product)

    return StockReserveResponse(
        product_id=product.id,
        reserved=payload.quantity,
        remaining_stock=product.stock,
    )
