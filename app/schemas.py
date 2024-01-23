from pydantic import BaseModel, HttpUrl

class Product(BaseModel):
    id: int
    label: str
    brand: str
    url: HttpUrl

class ProductCreate(BaseModel):
    label: str
    brand: str
    url: HttpUrl
    submitter_id: int