from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db, engine, SessionLocal
from app.db.base import Base
import app.models  # load all models into Base.metadata
from app.models.user import User, RoleEnum
from app.core.security import get_password_hash
from app.routers import auth, users, customers, parking, payments

def init_db():
    """បង្កើត Tables ទាំងអស់ និង Account Admin ដោយស្វ័យប្រវត្តិនៅពេល Server ចាប់ផ្តើមដំណើរការ"""
    try:
        # 1. បង្កើត Tables ទាំងអស់ដែលមិនទាន់មានក្នុង Database
        Base.metadata.create_all(bind=engine)
        
        # 2. បង្កើតគណនី Admin ដំបូងដោយស្វ័យប្រវត្តិ ប្រសិនបើមិនទាន់មាន
        db = SessionLocal()
        try:
            admin_user = db.query(User).filter(
                (User.username == "admin") | (User.email == "admin@parking.com")
            ).first()
            if not admin_user:
                new_admin = User(
                    username="admin",
                    email="admin@parking.com",
                    hashed_password=get_password_hash("admin123"),
                    role=RoleEnum.ADMIN,
                    is_active=True
                )
                db.add(new_admin)
                db.commit()
                print("✅ គណនី Admin ត្រូវបានបង្កើតដោយស្វ័យប្រវត្តិ (Username: admin, Password: admin123)")
        finally:
            db.close()
    except Exception as e:
        print(f"⚠️ ការរៀបចំ Database: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Monthly Car Parking Management System API",
    description="REST API for the Car Parking Management System",
    version="1.0.0",
    lifespan=lifespan
)

# បញ្ចូល Routers ទាំងអស់
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(customers.router)
app.include_router(parking.router)
app.include_router(payments.router)

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Check if the API server is running successfully."""
    return {"status": "ok", "message": "Backend API is running!"}

@app.get("/db-check", tags=["Health Check"])
def check_db_connection(db: Session = Depends(get_db)):
    """Test the database connection."""
    try:
        result = db.execute(text("SELECT DATABASE();")).scalar()
        return {"status": "success", "connected_to": result}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

