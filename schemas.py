from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from enums import ProductCategory

class ProductBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str | None = None
    price: Decimal = Field(gt=0, max_digits=7, decimal_places=2)
    stock: int = Field(ge=0)
    category: ProductCategory | None = None 
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=50)
    description: str | None = None
    price: Decimal | None = Field(None, gt=0, max_digits=7, decimal_places=2)
    stock: int | None = Field(None, ge=0)
    category: ProductCategory | None = None
    is_active: bool | None = None

class ProductRead(ProductBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)