from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Depends
from app.product_data import PRODUCTS
from app.schemas.product import Product, ProductCreate
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app import crud
from app import deps

app = FastAPI(title="Learn FastAPI", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
async def root(request: Request, db: Session = Depends(deps.get_db)) -> dict:
    """
    Root GET
    """

    products = crud.product.get_multi(db=db, limit=10)
    return products


@api_router.get("/products/", status_code=200)
async def get_all_products(db: Session = Depends(deps.get_db)) -> dict:
    """
    Get all products in the list
    """

    products = crud.product.get_multi(db=db)
    return products


@api_router.get("/product/{product_id}", status_code=200)
async def get_product(
    *, product_id: int = 0, db: Session = Depends(deps.get_db)
) -> dict:
    """Get a single product by ID"""

    result = crud.product.get(db=db, id=product_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id} not found!"
        )
    return result


@api_router.get("/search/", status_code=200)
async def search_products(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for products based on label keyword
    """
    products = crud.recipe.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": products}

    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), products)
    return {"results": list(results)[:max_results]}


@api_router.post("/product", status_code=201, response_model=Product)
async def create_product(
    *, product_in: ProductCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new product (in memory only)
    """

    new_product = crud.product.create(db=db, obj_in=product_in)

    return new_product


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")