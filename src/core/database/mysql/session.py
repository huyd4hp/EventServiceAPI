from .engine import Engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

SessionLocal = sessionmaker(bind=Engine,autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def async_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

