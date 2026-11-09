from pydantic import BaseModel
from typing import Optional

class SettingBase(BaseModel):
    business_name: str = "CarPark Central Management"
    contact_phone: str = "+855 12 345 678"
    contact_email: str = "support@carpark.com"
    default_hourly_rate: float = 1.5
    default_monthly_rate: float = 50.0
    currency: str = "USD ($)"
    total_capacity: int = 80
    auto_email_receipt: bool = True
    enable_sms_alerts: bool = False

class SettingUpdate(BaseModel):
    business_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    default_hourly_rate: Optional[float] = None
    default_monthly_rate: Optional[float] = None
    currency: Optional[str] = None
    total_capacity: Optional[int] = None
    auto_email_receipt: Optional[bool] = None
    enable_sms_alerts: Optional[bool] = None

class SettingResponse(SettingBase):
    id: int

    class Config:
        from_attributes = True
