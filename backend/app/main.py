from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.routers import auth, users, customers, parking

app = FastAPI(
    title="Monthly Car Parking Management System API",
    description="REST API for the Car Parking Management System",
    version="1.0.0"
)

# បញ្ចូល Routers ទាំងអស់
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(customers.router)
app.include_router(parking.router)

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