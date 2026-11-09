from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.parking_space import ParkingSpace as DBParkingSpace
from app.schemas.parking_space import ParkingSpace, ParkingSpaceCreate

router = APIRouter(prefix="/parking-spaces", tags=["Parking Spaces"])

@router.post("/", response_model=ParkingSpace, status_code=status.HTTP_201_CREATED)
def create_parking_space(space: ParkingSpaceCreate, db: Session = Depends(get_db)):
    # ពិនិត្យមើលក្រែងលោឈ្មោះចំណតនេះមានរួចហើយ
    db_space = db.query(DBParkingSpace).filter(DBParkingSpace.name == space.name).first()
    if db_space:
        raise HTTPException(status_code=400, detail="ឈ្មោះចំណតនេះមានរួចហើយក្នុងប្រព័ន្ធ!")
        
    new_space = DBParkingSpace(**space.model_dump())
    db.add(new_space)
    db.commit()
    db.refresh(new_space)
    return new_space

@router.get("/", response_model=list[ParkingSpace])
def read_parking_spaces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(DBParkingSpace).offset(skip).limit(limit).all()

