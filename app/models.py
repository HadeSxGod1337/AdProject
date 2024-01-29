import enum
import uuid
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from enum import auto

from fastapi_restful.enums import StrEnum

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    name = Column(String,  nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    phone_number = Column(String, nullable=True, unique=True)
    verified = Column(Boolean, nullable=False, server_default='False')
    verification_code = Column(String, nullable=True, unique=True)
    role = Column(String, server_default='user', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    ads = relationship('Ad', back_populates='user')

class AdTypes(StrEnum):
    SALE = auto()
    PURCHASE = auto()
    SERVICE = auto()
    DEFAULT = auto()

class Ad(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True,  autoincrement=True)
    title = Column(String(100))
    description = Column(String(500))
    type = Column(Enum(AdTypes, name='ad_types_enum', default=AdTypes.DEFAULT), nullable=False)
    user_id = Column(UUID, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship('User', back_populates='ads')


    def __init__(self, title, description, type, user_id):
        self.title = title
        self.description = description
        self.type = type
        self.user_id = user_id
