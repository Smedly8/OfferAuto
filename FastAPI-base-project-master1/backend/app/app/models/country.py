from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class Country(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # users = relationship("User", back_populates="country")
