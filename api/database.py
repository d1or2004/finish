from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL ma'lumotlar bazasiga ulanish
DATABASE_URL = 'postgresql://postgres:2004@localhost/finish'

# SQLAlchemy engine yaratish
engine = create_engine(DATABASE_URL, echo=True)

# Deklarativ baza
Base = declarative_base()
session = sessionmaker()

# Sessiya ishlab chiqaruvchisi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
