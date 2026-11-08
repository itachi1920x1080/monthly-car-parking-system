from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/customers", tags=["Customers Management"])

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_in: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # តម្រូវឲ្យ Login (Admin ឬ Cashier)
):
    """ចុះឈ្មោះអតិថិជនថ្មីចូលក្នុងប្រព័ន្ធចំណត"""
    
    # ឆែកមើលថាតើលេខទូរស័ព្ទនេះមានរួចហើយឬនៅ
    existing_customer = db.query(Customer).filter(Customer.phone_number == customer_in.phone_number).first()
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="លេខទូរស័ព្ទនេះមានរួចហើយនៅក្នុងប្រព័ន្ធ (Phone number already exists)"
        )
    
    new_customer = Customer(
        first_name=customer_in.first_name,
        last_name=customer_in.last_name,
        phone_number=customer_in.phone_number,
        email=customer_in.email
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get("/", response_model=List[CustomerResponse])
def get_all_customers(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # តម្រូវឲ្យ Login
):
    """ទាញយកបញ្ជីអតិថិជនទាំងអស់"""
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers