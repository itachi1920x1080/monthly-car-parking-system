from app.db.session import SessionLocal, engine
from app.db.base import Base
import app.models  # load all models into Base.metadata
from app.models.user import User, RoleEnum
from app.core.security import get_password_hash

def create_superuser():
    # បង្កើត Tables ទាំងអស់ប្រសិនបើវាមិនទាន់មាននៅក្នុង Database
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # ឆែកមើលថាតើមានគណនី admin នេះរួចហើយឬនៅ
        admin_email = "admin@parking.com"
        existing_user = db.query(User).filter(User.email == admin_email).first()

        if not existing_user:
            # ប្រសិនបើមិនទាន់មាន យើងនឹងបង្កើតថ្មី
            admin_user = User(
                username="admin",
                email=admin_email,
                hashed_password=get_password_hash("admin123"), # លេខសម្ងាត់គឺ admin123
                role=RoleEnum.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ គណនី Admin ត្រូវបានបង្កើតដោយជោគជ័យ!")
            print("👉 Username: admin")
            print("👉 Password: admin123")
        else:
            print("⚠️ គណនី Admin មានរួចហើយនៅក្នុងប្រព័ន្ធ។")
    except Exception as e:
        print(f"❌ មានបញ្ហា: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_superuser()