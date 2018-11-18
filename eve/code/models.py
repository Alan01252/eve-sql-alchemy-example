from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property

from eve_sqlalchemy import SQL
from eve_sqlalchemy.config import DomainConfig, ResourceConfig

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))


class Event(BaseModel):
    __tablename__ = 'EventFact'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_meta_key = Column(Integer)
    contact = Column(String(200))


class EventMeta(BaseModel):
    __tablename__ = 'EventMetaDimension'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200))


class Conversation(BaseModel):
    __tablename__ = 'ConversationFact'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_meta_key = Column(Integer)
    tag_bridge_key = Column(Integer)
    text = Column(String(200))


class TagBridge(BaseModel):
    __tablename__ = 'TagBridge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_bridge_key = Column(Integer)
    tag_key = Column(Integer)


class Tag(BaseModel):
    __tablename__ = 'TagDimension'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(100))

class OpLog(BaseModel):
    __tablename__ = 'oplog'
    id = Column(Integer, primary_key=True, autoincrement=True)
    r = Column(String(100))
    o = Column(String(100))
    i = Column(String(100))
    ip = Column(String(100))
    u = Column(String(100))






