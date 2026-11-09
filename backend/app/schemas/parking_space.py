from pydantic import BaseModel
from typing import Optional

class ParkingSpaceBase(BaseModel):
    name: str
    is_available: bool = True
    description: Optional[str] = None

class ParkingSpaceCreate(ParkingSpaceBase):
    pass

class ParkingSpace(ParkingSpaceBase):
    id: int

    class Config:
        from_attributes = True

