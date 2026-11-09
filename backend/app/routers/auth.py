from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.user import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """API សម្រាប់ Login ដើម្បីយក JWT Access Token (អាចប្រើ Username ឬ Email ក៏បាន)"""
    # 1. ស្វែងរក User តាម Username ឬ Email ក្នុង Database
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    
    # 2. ផ្ទៀងផ្ទាត់ថា User ពិតជាមាន ហើយ Password ត្រឹមត្រូវ
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # ពិនិត្យមើលថាតើ Account ត្រូវបានបិទ (Inactive) ឬអត់
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account",
        )
    
    # 3. ប្រសិនបើត្រឹមត្រូវ យើងបង្កើត JWT Token ដោយដាក់ username ទៅក្នុង 'sub'
    role_value = user.role.value if hasattr(user.role, "value") else str(user.role)
    access_token = create_access_token(data={"sub": user.username, "role": role_value})
    
    # 4. បញ្ជូន Token ទៅឲ្យ Frontend
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role_value,
        "username": user.username
    }