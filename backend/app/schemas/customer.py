from pydantic import BaseModel ,EmailStr
from typing import Optional
class CustomerBase (BaseModel):
    first_name : str
    last_name : str
    phone_number : str 
    email : Optional[EmailStr] = None

class CustomerCreate (CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id : int 

    model_config ={"from_attributes":True} 


