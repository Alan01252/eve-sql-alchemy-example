from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property, relationship, backref

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
    mo_contact_key = Column(String(200))


class Contact(BaseModel):
    __tablename__ = 'ContactDimension'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    numbers = relationship(
        "Number",
        secondary='ContactNumberBridge'
    )
    is_current = 'F'

    table_type = 'historic'
    # Tables of this type need to have historic fields checked
    # If the value is part of the historic then a new contact needs to be created
    # sqlalchemy should sort out creating the contact number bridge table for the new contact
    def getHistoricFields():
        return [
            'numbers'
        ]

class Number(BaseModel):
    __tablename__ = 'NumberDimension'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(50))
    contacts = relationship(
        Contact,
        secondary='ContactNumberBridge'
    )

    table_type = 'current'

class ContactNumberBridge(BaseModel):
    __tablename__ = 'ContactNumberBridge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(50))
    contact_key = Column(Integer, ForeignKey('contact.id'))
    number_key = Column(Integer, ForeignKey('number.id'))
    contact = relationship(Contact, backref=backref("contact_assoc"))
    number = relationship(Number, backref=backref("number_assoc"))
    is_current = 'F'


class EventMeta(BaseModel):
    __tablename__ = 'EventMetaDimension'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200))

    table_type = 'current'


class Comment(BaseModel):
    __tablename__ = 'CommentFact'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_meta_key = Column(Integer)
    text = Column(String(200))
    tags = relationship("TagBridge")

    table_type = "current"

    # If a new comment ready to be added
        # scan the comment for new tags
        # add new tags to tag table and grab list of ids
        # insert new comment with array of tag ids filled in.

class TagBridge(BaseModel):
    __tablename__ = 'TagBridge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment_key = Column(Integer, ForeignKey('commnet.id'))
    tag_key = Column(Integer, ForeignKey('tag.id'))

    table_type = "current"

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






