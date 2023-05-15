from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class Report(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    created = Column(Integer, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    img = Column(String)
    order = relationship("Order", back_populates="reports")
    # users = relationship("User", back_populates="country")
