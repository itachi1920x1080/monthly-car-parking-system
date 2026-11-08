from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.payment import Payment
from app.models.customer import Customer
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/payments", tags=["Payments Management"])

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """កត់ត្រាការបង់ប្រាក់របស់អតិថិជនប្រចាំខែ"""
    
    # 1. ពិនិត្យមើលថាតើអតិថិជននេះ (customer_id) ពិតជាមានមែនឬទេ
    customer = db.query(Customer).filter(Customer.id == payment_in.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="រកមិនឃើញអតិថិជននេះទេ (Customer not found)")
        
    # 2. បង្កើតកំណត់ត្រាបង់ប្រាក់ថ្មី
    new_payment = Payment(
        customer_id=payment_in.customer_id,
        amount=payment_in.amount,
        status=payment_in.status
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/", response_model=List[PaymentResponse])
def get_payments(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ទាញយកប្រវត្តិនៃការបង់ប្រាក់ទាំងអស់"""
    payments = db.query(Payment).offset(skip).limit(limit).all()
    return payments