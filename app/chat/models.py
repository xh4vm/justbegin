from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String

from app.db import Model, ModelId


class Chat(Model):

    user_id: int = Column(ModelId, ForeignKey('users.id'), nullable=False)
    title: str = Column(String(128), nullable=False)


class ChatParty(Model):
    __tablename__ = "chat_party"

    chat_id : int = Column(ModelId, ForeignKey('chats.id'), nullable=False)
    user_id: int = Column(ModelId, ForeignKey('users.id'), nullable=False)


class ChatMessage(Model):

    chat_id : int = Column(ModelId, ForeignKey('chats.id'), nullable=False)
    user_id: int = Column(ModelId, ForeignKey('users.id'), nullable=False)
    content : str = Column(String(4096), nullable=False)


class ChatMessageStatus(Model):
    __tablename__ = "chat_message_status"
    
    chat_message_id : int = Column(ModelId, ForeignKey('chat_messages.id'), nullable=False)
    user_id: int = Column(ModelId, ForeignKey('users.id'), nullable=False)
