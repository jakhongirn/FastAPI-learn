from fastapi import FastAPI, HTTPException, Request, Depends
from product_data import PRODUCTS
from schemas.product import Product, ProductCreate
from typing import List, Dict
from db.session import Session
import crud
import deps


app = FastAPI(title="Learn FastAPI")

@app.get("/", status_code=200)
async def root(
    request: Request,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Root GET
    """
    
    products = crud.product.get_multi(db=db, limit=10)
    return TEMPLATES.TemplateResponse("index.html", {"request": request, "products": products})
    
    
    
@app.get("/products/", status_code=200)
async def get_all_products():
    """
        Get all products in the list
    """
    
    products = PRODUCTS
    return products

@app.get("/product/{product_id}", status_code=200)
async def get_product(
    *, 
    product_id: int = 0,
    db: Session = Depends(deps.get_db)
    ) -> dict:
    """ Get a single product by ID """
    
    result = crud.product.get(db=db, id=product_id)
    if not result: 
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found!")
    return result
    


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
async def create_product(
    *, 
    product_in: ProductCreate,
    db:Session = Depends(deps.get_db)
    ) -> dict:
    """
        Create a new product (in memory only)
    """
    
    new_product = crud.product.create(db=db, obj_in=product_in)
    
    return new_product
