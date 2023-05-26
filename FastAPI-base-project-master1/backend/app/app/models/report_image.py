from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class ReportImage(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("report.id"), nullable=True)
    img = Column(String)
    report = relationship("Report", back_populates="report_images")
    # users = relationship("User", back_populates="country")
