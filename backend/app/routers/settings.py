from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.setting import SystemSetting
from app.schemas.setting import SettingResponse, SettingUpdate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/settings", tags=["System Settings"])

def get_or_create_settings(db: Session) -> SystemSetting:
    setting = db.query(SystemSetting).first()
    if not setting:
        setting = SystemSetting()
        db.add(setting)
        db.commit()
        db.refresh(setting)
    return setting

@router.get("/", response_model=SettingResponse)
def get_settings(db: Session = Depends(get_db)):
    """ទាញយកការកំណត់ប្រព័ន្ធបច្ចុប្បន្ន (តម្លៃសេវា និងព័ត៌មានទូទៅ)"""
    return get_or_create_settings(db)

@router.put("/", response_model=SettingResponse)
def update_settings(
    settings_in: SettingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """កែសម្រួលការកំណត់ប្រព័ន្ធ និងតម្លៃសេវាចំណត (Admin Only)"""
    if str(current_user.role).lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="គ្មានសិទ្ធិ! មានតែ Administrator ប៉ុណ្ណោះដែលអាចកែប្រែការកំណត់ប្រព័ន្ធបាន។"
        )
    
    setting = get_or_create_settings(db)
    update_data = settings_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        if value is not None:
            setattr(setting, key, value)
            
    db.commit()
    db.refresh(setting)
    return setting
