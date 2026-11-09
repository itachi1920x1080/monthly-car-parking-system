from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, RoleEnum
from app.schemas.user import UserResponse, UserCreate
from app.core.deps import get_current_user
from app.db.session import get_db
from app.core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["Users Management"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """ទាញយកព័ត៌មាន Profile របស់ User ដែលកំពុងប្រើប្រាស់ Token"""
    return current_user

@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ទាញយកបញ្ជី Users ទាំងអស់នៅក្នុងប្រព័ន្ធ"""
    return db.query(User).all()
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """បង្កើតគណនីថ្មី (សម្រាប់តែ Admin ប៉ុណ្ណោះដែលអាចបង្កើតបាន)"""
    
    # 1. ពិនិត្យមើលថាតើអ្នកដែលកំពុងហៅ API នេះជា Admin ដែរឬទេ
    if str(current_user.role).lower() != RoleEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="គ្មានសិទ្ធិ! មានតែ Admin ប៉ុណ្ណោះដែលអាចបង្កើតគណនីថ្មីបាន។"
        )
    
    # 2. ពិនិត្យមើលថាតើ Username ឬ Email នេះមានអ្នកប្រើហើយឬនៅ
    user_exists = db.query(User).filter(
        (User.username == user_in.username) | (User.email == user_in.email)
    ).first()
    
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username ឬ Email នេះមានរួចហើយនៅក្នុងប្រព័ន្ធ។"
        )
    
    # 3. បង្កើតគណនីថ្មី និង Hash Password មុននឹងបញ្ចូលទៅ DB
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # ទាញយកទិន្នន័យ (រួមទាំង ID ថ្មី) ពី DB មកវិញ
    
    return new_user