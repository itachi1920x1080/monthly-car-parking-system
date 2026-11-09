from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.base import Base

class SystemSetting(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(100), default="CarPark Central Management", nullable=False)
    contact_phone = Column(String(50), default="+855 12 345 678", nullable=False)
    contact_email = Column(String(100), default="support@carpark.com", nullable=False)
    default_hourly_rate = Column(Float, default=1.5, nullable=False)
    default_monthly_rate = Column(Float, default=50.0, nullable=False)
    currency = Column(String(20), default="USD ($)", nullable=False)
    total_capacity = Column(Integer, default=80, nullable=False)
    auto_email_receipt = Column(Boolean, default=True, nullable=False)
    enable_sms_alerts = Column(Boolean, default=False, nullable=False)


