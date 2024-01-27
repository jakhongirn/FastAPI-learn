from fastapi import FastAPI, HTTPException
from product_data import PRODUCTS
from schemas.product import Product, ProductCreate
from typing import List, Dict


app = FastAPI(title="Learn FastAPI")

@app.get("/")
async def root():
    return {"message": "Hello world!"}

@app.get("/products/", status_code=200)
async def get_all_products():
    """
        Get all products in the list
    """
    
    products = PRODUCTS
    return products

@app.get("/product/{product_id}", status_code=200)
async def get_product(*, product_id: int = 0) -> dict:
    """ Get a single product by ID """
    
    result = [product for product in PRODUCTS if product["id"] == product_id]
    
    print(result)
    if not result:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    return result[0]

@app.get("/search/", status_code=200)
async def search_products(keyword: str | None = None, max_results: int | None = 5):
    """Search for products based on label keyword"""
    if not keyword: 
        return {"results": PRODUCTS[:max_results]}
    
    # Anoter simple solution
    # results = []
    # for product in PRODUCTS:
    #     if keyword.lower() in product["label"].lower():
    #         results.append(product)
    # if not results:
    #     return {"message": "There is no product with given keyword."}
    
    results = filter(lambda product: keyword.lower() in product["label"].lower(), PRODUCTS)
    
    return {"results": list(results)[:max_results]}


@app.post("/product", status_code=201, response_model=Product)
async def create_product(*, product_in: ProductCreate) -> dict:
    """
        Create a new product (in memory only)
    """
    
    new_prod_id = len(PRODUCTS) + 1
    new_product = Product(
        id=new_prod_id,
        label=product_in.label,
        brand=product_in.brand,
        url=product_in.url
    ).dict()
    PRODUCTS.append(new_product)
    
    return new_product
