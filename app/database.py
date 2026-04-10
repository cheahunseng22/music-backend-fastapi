from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use Render's DATABASE_URL (will be set in environment variables)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5432/music_db")

# For Render PostgreSQL, add SSL mode
if "render.com" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL + "?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()