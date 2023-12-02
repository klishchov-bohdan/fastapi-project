from app.db_conn import DBBase
from sqlalchemy import Column, String, Integer, text, TIMESTAMP, Uuid


class Chat(DBBase):
    __tablename__ = 'chats'
    id = Column(Uuid, primary_key=True, unique=True)
    user_id = Column(Integer)
    # client_unique_string = Column(String, unique=True)
    message = Column(String)
    gpt_answer = Column(String)
    time_created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
