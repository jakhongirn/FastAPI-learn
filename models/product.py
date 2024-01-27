from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    label=Column(String(256), nullable=False)
    url=Column(String(256), index=True, nullable=True)
    brand=Column(String(256), nullable=True)
    submitter_id=Column(Integer, ForeignKey("user.id"), nullable=True)
    submitter=relationship("User", back_populates="products")
    