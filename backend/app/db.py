from app.config import DATABASE_URL
from sqlalchemy import create_engine

# Database and engine setup
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    # pool_size=20, max_overflow=10
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
