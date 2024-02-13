import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.product_data import PRODUCTS


logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin@productapi.com"


def init_db(db: Session) -> None:  # 1
    if FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=FIRST_SUPERUSER)  # 2
        if not user:
            user_in = schemas.UserCreate(
                full_name="Initial Super User",
                email=FIRST_SUPERUSER,
                is_superuser=True,
            )
            user = crud.user.create(db, obj_in=user_in)
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_SUPERUSER} already exists. "
            )
        if not user.products:
            for product in PRODUCTS:
                product_in = schemas.ProductCreate(
                    label=product["label"],
                    brand=product["brand"],
                    url=product["url"],
                    submitter_id=user.id,
                )
                crud.product.create(db, obj_in=product_in)  # 3