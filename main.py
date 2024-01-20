from fastapi import FastAPI
from typing import List, Dict


app = FastAPI(title="Learn FastAPI")

PRODUCTS: List[Dict[str, str | int]] = [
    {
        "id": 1,
        "label": "Iphone 15 Pro",
        "brand": "Apple",
        "url": "http://www.seriouseats.com/products/2011/12/chicken-vesuvio-product.html",
    },
    {
        "id": 2,
        "label": "Samsung Galaxy S24",
        "brand": "Samsung",
        "url": "http://noproducts.com/product/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "HP Pavilion Gaming",
        "brand": "Hewlett Packard",
        "url": "http://www.seriouseats.com/products/2011/02/cauliflower-and-tofu-curry-product.html",
    },
]

@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/product/{product_id}", status_code=200)
async def get_product(*, product_id: int = 0) -> dict:
    """ Get a single product by ID """
    
    result = [product for product in PRODUCTS if product["id"] == product_id]
    
    print(result)
    if result:
        return result[0]
    else:
        return {"message": "There is no products assigned with given id."}


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

