from pydantic import BaseModel
from typing import Optional
from datetime import date

class ContractBase(BaseModel):
    customer_id: int
    space_id: str
    start_date: date
    end_date: date
    status: Optional[str] = "Active"

class ContractCreate(ContractBase):
    pass

class ContractResponse(ContractBase):
    id: int

    model_config = {"from_attributes": True}

