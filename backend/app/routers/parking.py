from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models.parking import ParkingRecord
from app.models.customer import Customer
from app.schemas.parking import ParkingRecordCreate, ParkingRecordResponse
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/parking", tags=["Parking Records"])

@router.post("/check-in", response_model=ParkingRecordResponse, status_code=status.HTTP_201_CREATED)
def check_in_car(
    record_in: ParkingRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """កត់ត្រាឡានចូលចំណត (Check-in)"""
    
    # 1. ពិនិត្យមើលថាតើលេខសម្គាល់អតិថិជននេះ (customer_id) ពិតជាមានមែនឬទេ
    customer = db.query(Customer).filter(Customer.id == record_in.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="រកមិនឃើញអតិថិជននេះទេ (Customer not found)")
        
    # 2. បង្កើតកំណត់ត្រាចូលចតថ្មី
    new_record = ParkingRecord(
        customer_id=record_in.customer_id,
        license_plate=record_in.license_plate
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/", response_model=List[ParkingRecordResponse])
def get_parking_records(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ទាញយកប្រវត្តិនៃការចូលចតទាំងអស់"""
    records = db.query(ParkingRecord).offset(skip).limit(limit).all()
    return records

@router.put("/check-out/{record_id}", response_model=ParkingRecordResponse)
def check_out_car(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """កត់ត្រាឡានចេញពីចំណត (Check-out)"""
    
    # 1. ស្វែងរកទិន្នន័យចំណតតាមរយៈ ID (លេខរៀង)
    record = db.query(ParkingRecord).filter(ParkingRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="រកមិនឃើញទិន្នន័យចំណតនេះទេ (Record not found)")

    # 2. ពិនិត្យមើលថាតើឡាននេះធ្លាប់បាន Check-out រួចហើយឬនៅ
    if record.check_out_time is not None:
        raise HTTPException(status_code=400, detail="ឡាននេះបាន Check-out ចេញពីចំណតរួចហើយ")

    # 3. កំណត់ម៉ោងចេញ ជាម៉ោងបច្ចុប្បន្ន
    record.check_out_time = datetime.now()
    db.commit()
    db.refresh(record)
    return record