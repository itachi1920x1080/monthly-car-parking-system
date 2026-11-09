from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db, engine, SessionLocal
from app.db.base import Base
import app.models  # load all models into Base.metadata
from app.models.user import User, RoleEnum
from app.models.customer import Customer
from app.models.parking import ParkingRecord
from app.models.payment import Payment
from app.models.contract import Contract
from app.core.security import get_password_hash
from app.routers import auth, users, customers, parking, payments, contract, parking_space, settings as settings_router


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

            # 2.1 បង្កើតគណនី Cashier (បេឡា/បុគ្គលិក) ប្រសិនបើមិនទាន់មាន
            cashier_user = db.query(User).filter(
                (User.username == "cashier") | (User.email == "cashier@parking.com")
            ).first()
            if not cashier_user:
                new_cashier = User(
                    username="cashier",
                    email="cashier@parking.com",
                    hashed_password=get_password_hash("cashier123"),
                    role=RoleEnum.CASHIER,
                    is_active=True
                )
                db.add(new_cashier)
                db.commit()
                print("✅ គណនី Cashier ត្រូវបានបង្កើតដោយស្វ័យប្រវត្តិ (Username: cashier, Password: cashier123)")

            # 2.2 បង្កើតគណនី Customer (អតិថិជន) ប្រសិនបើមិនទាន់មាន
            customer_user = db.query(User).filter(
                (User.username == "customer") | (User.email == "customer@parking.com")
            ).first()
            if not customer_user:
                new_customer = User(
                    username="customer",
                    email="customer@parking.com",
                    hashed_password=get_password_hash("customer123"),
                    role=RoleEnum.CUSTOMER,
                    is_active=True
                )
                db.add(new_customer)
                db.commit()
                print("✅ គណនី Customer ត្រូវបានបង្កើតដោយស្វ័យប្រវត្តិ (Username: customer, Password: customer123)")
            
            # 3. បង្កើតអតិថិជនគំរូ (Sok Chan) ប្រសិនបើមិនទាន់មាន
            sample_customer = db.query(Customer).filter(Customer.phone_number == "012345678").first()
            if not sample_customer:
                sample_customer = Customer(
                    first_name="Sok",
                    last_name="Chan",
                    phone_number="012345678",
                    email="sokchan@gmail.com"
                )
                db.add(sample_customer)
                db.commit()
                db.refresh(sample_customer)
                print("✅ អតិថិជនគំរូ (Sok Chan) ត្រូវបានបង្កើតដោយស្វ័យប្រវត្តិ")

            # 4. បង្កើតកំណត់ត្រាបង់ប្រាក់គំរូ ($50) ប្រសិនបើមិនទាន់មាន
            sample_payment = db.query(Payment).first()
            if not sample_payment and sample_customer:
                new_payment = Payment(
                    customer_id=sample_customer.id,
                    amount=50.0,
                    status="Paid"
                )
                db.add(new_payment)
                db.commit()
                print("✅ កំណត់ត្រាបង់ប្រាក់គំរូ ($50) ត្រូវបានបង្កើតដោយស្វ័យប្រវត្តិ")

            # 5. បង្កើតកំណត់ត្រាចំណតគំរូ ប្រសិនបើមិនទាន់មាន
            sample_parking = db.query(ParkingRecord).first()
            if not sample_parking and sample_customer:
                new_parking = ParkingRecord(
                    customer_id=sample_customer.id,
                    license_plate="2BA-1234"
                )
                db.add(new_parking)
                db.commit()
                print("✅ កំណត់ត្រាចំណតគំរូ (2BA-1234) ត្រូវបានបង្កើតដោយស្វ័យប្រវត្តិ")

            # 6. បង្កើតកិច្ចសន្យាគំរូ (CT-001) ប្រសិនបើមិនទាន់មាន
            sample_contract = db.query(Contract).first()
            if not sample_contract and sample_customer:
                from datetime import date
                new_contract = Contract(
                    customer_id=sample_customer.id,
                    space_id="A-01",
                    start_date=date.today(),
                    end_date=date(date.today().year + 1, date.today().month, date.today().day),
                    status="Active"
                )
                db.add(new_contract)
                db.commit()
                print("✅ កិច្ចសន្យាគំរូ (CT-001) ត្រូវបានបង្កើតដោយស្វ័យប្រវត្តិ")
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

# កំណត់ CORS Middleware សម្រាប់ Frontend (Vue 3 / Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", # Port ស្តង់ដាររបស់ Vue 3 (Vite)
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"], # អនុញ្ញាតគ្រប់ Method (GET, POST, PUT, DELETE)
    allow_headers=["*"], # អនុញ្ញាតគ្រប់ Header ទាំងអស់ (រួមទាំង Authorization Token)
)

# បញ្ចូល Routers ទាំងអស់
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(customers.router)
app.include_router(parking.router)
app.include_router(payments.router)
app.include_router(contract.router)
app.include_router(parking_space.router)
app.include_router(settings_router.router)

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

