from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(50), index=True, nullable=False)
    is_superviser=Column(Boolean, default=False)
    products = relationship("Product", cascade="all, delete-orphan", back_populates="submitter", uselist=True)
    