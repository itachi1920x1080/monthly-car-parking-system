from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.db.base import Base
import enum

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    CASHIER = "cashier"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.CASHIER, nullable=False)
    is_active = Column(Boolean, default=True)