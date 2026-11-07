from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# កំណត់ប្រភេទ Hashing ជា bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ផ្ទៀងផ្ទាត់ Password ធម្មតា ជាមួយ Password ដែលបាន Hash រួច"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """បំប្លែង (Hash) Password ធម្មតា ទៅជាកូដសម្ងាត់"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """បង្កើត JWT Token សម្រាប់បញ្ជាក់អត្តសញ្ញាណ User"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # ត្រង់នេះត្រូវបានកែពី minute ទៅ minutes វិញ
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt