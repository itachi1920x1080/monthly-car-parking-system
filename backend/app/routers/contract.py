from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.contract import Contract
from app.models.customer import Customer
from app.schemas.contract import ContractCreate, ContractResponse
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/contracts", tags=["Contracts Management"])

@router.post("/", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
def create_contract(
    contract_in: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """បង្កើតកិច្ចសន្យាថ្មីសម្រាប់អតិថិជន"""
    customer = db.query(Customer).filter(Customer.id == contract_in.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="រកមិនឃើញអតិថិជននេះទេ (Customer not found)")
    
    new_contract = Contract(
        customer_id=contract_in.customer_id,
        space_id=contract_in.space_id,
        start_date=contract_in.start_date,
        end_date=contract_in.end_date,
        status=contract_in.status
    )
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    return new_contract

@router.get("/", response_model=List[ContractResponse])
def get_contracts(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ទាញយកបញ្ជីកិច្ចសន្យាទាំងអស់"""
    return db.query(Contract).offset(skip).limit(limit).all()
