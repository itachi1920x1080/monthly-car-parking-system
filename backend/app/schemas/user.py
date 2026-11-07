from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum

# ទិន្នន័យមូលដ្ឋានរបស់ User
class UserBase(BaseModel):
    username: str
    email: EmailStr

# ទិន្នន័យដែល Frontend ត្រូវបញ្ជូនមកពេលបង្កើត User ថ្មី
class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.CASHIER

# ទិន្នន័យដែល Backend បញ្ជូនទៅឲ្យ Frontend វិញ (មិនបង្ហាញ Password ទេ)
class UserResponse(UserBase):
    id: int
    role: RoleEnum
    is_active: bool

    model_config = {"from_attributes": True}

# ទម្រង់របស់ JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str