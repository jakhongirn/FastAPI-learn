from pydantic import BaseModel, HttpUrl
from typing import Sequence

class ProductBase(BaseModel):
    label: str
    brand: str
    url: HttpUrl


class ProductCreate(ProductBase):
    label: str
    brand: str
    url: HttpUrl
    submitter_id: int


class ProductUpdate(ProductBase):
    label: str

class ProductInDBBase(ProductBase):
    id: int
    submitter_id: int

    class Config:
        orm_mode = True

class Product(ProductInDBBase):
    pass


# Properties properties stored in DB
class ProductInDB(ProductInDBBase):
    pass


class ProductSearchResults(BaseModel):
    results: Sequence[Product]

    