from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .clients import ClientPublic


class ProductBase(BaseModel):
    title: str = Field(max_length=20)
    description: Optional[str] = Field(None, max_length=300)
    client_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=300)
    client_id: Optional[int] = None


class ProductPublic(BaseModel):
    id: int
    title: str = Field(max_length=20)
    description: Optional[str] = Field(None, max_length=300)
    client: ClientPublic


class SavedProductCreate(BaseModel):
    product_id: int


class SavedProductPublic(BaseModel):
    id: int
    product_id: int
    user_id: int
    added_at: datetime
    in_shopping_cart: bool