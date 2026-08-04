from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text, func, Enum as SqlEnum
from database import Base
from enum import Enum
from enums import ProductCategory


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(precision=7, scale=2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(SqlEnum(ProductCategory))
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())