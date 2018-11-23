import os
 
from sqlalchemy import Column, DateTime, String, SmallInteger, Enum, BigInteger, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))

class Event(BaseModel):
    __tablename__ = 'event'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_meta_id = Column(BigInteger, ForeignKey('event_meta.id'))
    event_meta = relationship("EventMeta", back_populates="event")
    mo_contact_key = Column(String(200))

class EventMeta(BaseModel):
    __tablename__ = 'event_meta'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event = relationship("Event", back_populates="event_meta", uselist=False)
    url = Column(String(200))

    table_type = 'current'

class ContactTeam(BaseModel):
    __tablename__ = 'contact_team'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    table_type = 'current'
    contacts = relationship(
        'Contact',
        backref="contact_team"
    )

class Contact(BaseModel):
    __tablename__ = 'contact'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    numbers = relationship(
        'Number',
        secondary='contact_number_bridge',
    )
    team_id = Column(BigInteger, ForeignKey('contact_team.id'))

    is_current = 'F'
    table_type = 'historic'
    # Tables of this type need to have historic fields checked
    # If the value is part of the historic then a new contact needs to be created
    # sqlalchemy should sort out creating the contact number bridge table for the new contact
    def getHistoricFields(self):
        return [
            'numbers'
        ]
 
class Number(BaseModel):
    __tablename__ = 'number'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(300))
    contacts = relationship(
        Contact,
        secondary='contact_number_bridge'
    )
 
class ContactNumberBridge(BaseModel):
    __tablename__ = 'contact_number_bridge'
    id = Column(BigInteger, primary_key=True)
    contact_id = Column(BigInteger, ForeignKey('contact.id'))
    number_id = Column(BigInteger, ForeignKey('number.id'))
    extra_data = Column(String(256))
    number = relationship(Number, backref=backref("number_assoc"))

class Comment(BaseModel):
    __tablename__ = 'comment'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    # TODO IMPLEMENT RELATIONS
    event_meta_key = Column(BigInteger)
    text = Column(String(200))
    tags = relationship(
        'Tag',
        secondary='comment_tag_bridge'
    )

    table_type = "current"

    # If a new comment ready to be added
        # scan the comment for new tags
        # add new tags to tag table and grab list of ids
        # insert new comment with array of tag ids filled in.

class Tag(BaseModel):
    __tablename__ = 'tag'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String(100))

class CommentTagBridge(BaseModel):
    __tablename__ = 'comment_tag_bridge'
    id = Column(BigInteger, primary_key=True)
    comment_id = Column(BigInteger, ForeignKey('comment.id'))
    tag_id = Column(BigInteger, ForeignKey('tag.id'))
    extra_data = Column(String(256))
    comment = relationship(Comment, backref=backref("comment_assoc"))
    tag = relationship(Tag, backref=backref("tag_assoc"))

class Totp(BaseModel):
    __tablename__ = 'totp_token'
    id = Column(BigInteger, primary_key=True)
    token = Column(String(256))
    another_token = Column(String(256))
    portal_uuid = Column(BigInteger)
    valid_until = Column(DateTime)
    
class PortalUser(BaseModel):
    __tablename__ = 'portal_user'
    id = Column(BigInteger, primary_key=True)
    full_name = Column(String(200))
    email = Column(String(571))
    password_hash = Column('password_hash',String(200))
    status = Column(Enum("Active", "Disabled" ,"Locked", "Archived"))
    two_fa = Column(Enum("Enabled", "Disabled"))
    totp_key = Column(String(550))
    failed_sign_in_attempts_count = Column(SmallInteger, default=None)

class OpLog(BaseModel):
    __tablename__ = 'oplog'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    r = Column(String(100))
    o = Column(String(100))
    i = Column(String(100))
    ip = Column(String(100))
    u = Column(String(100))
    c = Column(String(100))