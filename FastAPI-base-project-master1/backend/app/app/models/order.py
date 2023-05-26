from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class Order(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    vin = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    # users = relationship("User", back_populates="country")
    user = relationship("User", back_populates="orders")
    reports = relationship("Report", back_populates="order")
    
