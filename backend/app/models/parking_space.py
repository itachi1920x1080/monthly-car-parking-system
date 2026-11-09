from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class ParkingSpace(Base):
    __tablename__ = "parking_spaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False) # ឈ្មោះចំណត (ឧ. A-01)
    is_available = Column(Boolean, default=True) # True = ទំនេរ, False = មានគេជួលហើយ
    description = Column(String(255), nullable=True) # ព័ត៌មានបន្ថែម
