from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from app.models.user import RoleEnum

# ទិន្នន័យមូលដ្ឋានរបស់ User
class UserBase(BaseModel):
    username: str
    email: EmailStr

# ទិន្នន័យដែល Frontend ត្រូវបញ្ជូនមកពេលបង្កើត User ថ្មី
class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.CASHIER

    @field_validator('role', mode='before')
    @classmethod
    def normalize_role(cls, v):
        if isinstance(v, str):
            clean = v.strip().lower()
            if clean in ("staff", "cashier", "staff (បុគ្គលិក)", "clerk", "teller"):
                return RoleEnum.CASHIER
            if clean in ("admin", "administrator"):
                return RoleEnum.ADMIN
            if clean in ("customer", "user", "client"):
                return RoleEnum.CUSTOMER
        return v

# ទិន្នន័យដែល Backend បញ្ជូនទៅឲ្យ Frontend វិញ (មិនបង្ហាញ Password ទេ)
class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool

    model_config = {"from_attributes": True}

# ទម្រង់របស់ JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str
    role: Optional[str] = None
    username: Optional[str] = None
