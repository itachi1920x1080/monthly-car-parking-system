from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ParkingRecordBase(BaseModel):
    customer_id: int
    license_plate: str

class ParkingRecordCreate(ParkingRecordBase):
    pass

class ParkingRecordResponse(ParkingRecordBase):
    id: int
    check_in_time: datetime
    check_out_time: Optional[datetime] = None

    model_config = {"from_attributes": True}