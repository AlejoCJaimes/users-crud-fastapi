from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

# Create the SQLAlchemy engine with the specified URI from settings
engine = create_engine(settings.DATABASE_URL)

# Create a session factory to generate new SessionLocal instances
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for declarative models
Base = declarative_base()
