from app.db_conn import DBBase
from sqlalchemy import Column, String, Integer, text, DateTime, Boolean, TIMESTAMP


class User(DBBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, nullable=True)
    hashed_password = Column(String)
    disabled = Column(Boolean)
    verified = Column(Boolean)
    is_admin = Column(Boolean)
    time_created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    time_updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
