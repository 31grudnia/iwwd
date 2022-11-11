import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
load_dotenv(".env")

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]
# ASYNC_SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)
# async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
# AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# async def async_get_db():
#     async with AsyncSessionLocal() as db:
#         yield db
#         await db.commit()