from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer,primary_key=True,index=True)
    customer_id = Column(Integer,ForeignKey("customer.id"),nullable=False)
    amount = Column(Float,nullable=False)
    payment_date = Column(DateTime(timezone=True),server_default=func.now())
    status =  Column(String(30),default="Paid")

    customer=relationship("Customer")