from fastapi import Depends, FastAPI, HTTPException, Query
from schemas import ProductCreate, ProductRead, ProductUpdate
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
import models
from database import Base, engine
from typing import Literal


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Simple shop API",
    description = "RESTful API for product managements.",
    version="0.1.0",
)

@app.get("/", tags=["products"])
def root():
    return {"message": "TEST"}

@app.post("/products/", response_model=ProductRead, status_code=201, tags=["products"])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product."""
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=list[ProductRead], tags=["products"])
def list_products(
    category: str | None = Query(None),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    is_active: bool | None = Query(None),
    sort_by: Literal["id", "name", "price", "stock", "created_at"] = Query("id"),
    order: Literal["asc", "desc"] = Query("asc"),
    skip: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Show all possible products with sorting and ordering."""
    query = db.query(models.Product)

    # Filters
    if category is not None:
        query = query.filter(models.Product.category == category)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    if is_active is not None:
        query = query.filter(models.Product.is_active == is_active)

    # Sorting
    sort_column = getattr(models.Product, sort_by)
    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    return query.offset(skip).limit(limit).all()

@app.get("/products/{product_id}/", response_model=ProductRead, tags=["products"])
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Select specific product by ID."""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return product

@app.patch("/products/{product_id}/",response_model=ProductRead, tags=["products"])
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """Update a product by ID."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for field, value in product_update.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}/", status_code=204, tags=["products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product by ID."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_product)
    db.commit()