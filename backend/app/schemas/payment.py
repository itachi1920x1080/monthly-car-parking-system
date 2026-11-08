from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    customer_id: int
    amount: float
    status: Optional[str] = "Paid"

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    payment_date: datetime

    model_config = {"from_attributes": True}