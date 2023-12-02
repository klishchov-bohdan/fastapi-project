from app.db_conn import DBBase
from sqlalchemy import Column, String, Integer, text, DateTime, Boolean, TIMESTAMP, Uuid, BigInteger


class Session(DBBase):
    __tablename__ = 'sessions'
    id = Column(Uuid, primary_key=True, unique=True)
    user_id = Column(Integer)
    token = Column(String, unique=True)
    client_unique_string = Column(String, unique=True)
    expires_in = Column(BigInteger)
    time_created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
