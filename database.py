from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./flagged_users.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class FlaggedUser(Base):
    __tablename__ = "flagged_users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    id_number = Column(String)
    trust_score = Column(Integer)
    message = Column(String)

# Create table on first run
Base.metadata.create_all(bind=engine)
