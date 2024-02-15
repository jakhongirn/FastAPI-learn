import time
from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Depends
from app.product_data import PRODUCTS
from app.schemas.product import Product, ProductCreate
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app import crud
from app import deps

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(title="Learn FastAPI", openapi_url="/openapi.json")

root_router = APIRouter()
app = FastAPI(title="Recipe API")


@root_router.get("/", status_code=200)
async def root(request: Request) -> dict:
    return {"Hello world!"}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response



app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")