from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

# Database URL as a parameter
engine = create_engine(settings.DATABASE_URL)

# Session Factory
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

# Providing the database session to FastAPI through get_db()
def get_db():
    db = SessionLocal()

    try:
        yield(db)
    finally:
        db.close()