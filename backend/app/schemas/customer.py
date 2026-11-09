from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str 
    email: Optional[EmailStr] = None

    @field_validator("email", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        if v == "" or (isinstance(v, str) and not v.strip()):
            return None
        return v

class CustomerCreate (CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id : int 

    model_config ={"from_attributes":True} 


