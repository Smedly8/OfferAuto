from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class Report(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)    
    created = Column(Integer, index=True)
    # users = relationship("User", back_populates="country")
