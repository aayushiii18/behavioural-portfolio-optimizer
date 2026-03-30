from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from database import create_tables

# Create tables on startup
create_tables()

app = FastAPI(
    title="Behavioural Portfolio Optimizer API",
    description="Detects investor biases and optimizes portfolios",
    version="1.0.0"
)

# Fix CORS - Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Behavioural Portfolio Optimizer API is running!",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}