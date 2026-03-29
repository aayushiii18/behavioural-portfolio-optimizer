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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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