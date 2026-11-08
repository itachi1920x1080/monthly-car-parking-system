from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class ParkingRecord(Base):
    __tablename__ = "parking_records"

    id = Column(Integer, primary_key=True, index=True)
    # ភ្ជាប់ Foreign Key ទៅកាន់ Table customer
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    license_plate = Column(String(20), nullable=False) # ស្លាកលេខឡាន
    check_in_time = Column(DateTime(timezone=True), server_default=func.now())
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship ដើម្បីងាយស្រួលទាញយកឈ្មោះអតិថិជន
    customer = relationship("Customer")