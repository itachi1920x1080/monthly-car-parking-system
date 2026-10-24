from fastapi import FastAPI

app = FastAPI(
    title="Monthly Car Parking Management System API",
    description="REST API for the Car Parking Management System",
    version="1.0.0"
)

@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Check if the API server is running successfully.
    """
    return {"status": "ok", "message": "Backend API is running!"}