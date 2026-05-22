import time
from collections import defaultdict
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database import engine, Base
from api.auth import router as auth_router
from api.transactions import router as transactions_router

# 1. Initialize SQLite Database Tables on boot
print("Initializing database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables initialized successfully!")

# Seed Database with Default Credentials
def seed_database():
    from core.database import SessionLocal
    from models.user import User
    from core.security import get_password_hash
    
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            print("Seeding database with default credentials...")
            admin_user = User(
                username="admin",
                email="admin@fraudshield.com",
                hashed_password=get_password_hash("admin123"),
                role="admin"
            )
            standard_user = User(
                username="user",
                email="user@fraudshield.com",
                hashed_password=get_password_hash("user123"),
                role="user"
            )
            db.add(admin_user)
            db.add(standard_user)
            db.commit()
            print("Database successfully seeded!")
            print("Default Admin: admin / admin123")
            print("Default User:  user / user123")
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
    finally:
        db.close()

seed_database()

# 2. Instantiate FastAPI Application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Full-stack real-time Credit Card Fraud Detection System API with XGBoost scoring and role-based JWT access.",
    version="1.0.0"
)

# 3. Configure CORS Middleware
# Allows the React frontend running on port 5173 to safely communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. In-Memory Client IP Rate Limiter Middleware
# Keeps trace of client requests to prevent API brute forcing
RATE_LIMIT_WINDOW_SECONDS = 60
MAX_REQUESTS_PER_WINDOW = 100 # Allow 100 requests per minute per IP

request_tracker = defaultdict(list)

@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    # Retrieve client IP
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()
    
    # Prune historical timestamps outside the active sliding window
    active_requests = [
        t for t in request_tracker[client_ip]
        if current_time - t < RATE_LIMIT_WINDOW_SECONDS
    ]
    request_tracker[client_ip] = active_requests
    
    # Enforce threshold limit
    if len(active_requests) >= MAX_REQUESTS_PER_WINDOW:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "detail": "Too many requests. Please wait a minute before retrying to ensure platform stability."
            }
        )
        
    # Register current request
    request_tracker[client_ip].append(current_time)
    
    # Process request downstream
    response = await call_next(request)
    return response

# 5. Register API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(transactions_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "api_docs": "/docs",
        "version": "1.0.0"
    }
