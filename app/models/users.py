from sqlalchemy import Integer,Boolean, Column, String
from app.db.session import Base


class User(Base):
    """Model representing a user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False,
                           doc="Hashed password of the user.")
    is_authenticated = Column(
        Boolean(), default=False, doc="Flag indicating if the user is authenticated.")
    is_superuser = Column(Boolean(), default=False,
                          doc="Flag indicating if the user is a superuser.")
    is_blocked = Column(Boolean(), default=False,
                       doc="Flag indicating if the user is blocked.")
    attempts_login_failed = Column(Integer, default=0)
