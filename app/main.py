from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import public, admin
from database import engine
import models

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Music API", version="1.0")

# CORS - Allow your Netlify frontend
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://chncam.netlify.app",
    "https://chncam.uk"
]

# CORS - ONLY ONE allow_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # ← Use this ONE
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(public.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Music API is running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}
