import uuid
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


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


class Post(Base):
    __tablename__ = 'posts'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship('User')


class AdType(Base):
    __tablename__ = 'ad_types'

    id = Column(Integer, primary_key=True)
    name = Column(Enum('Продажа', 'Покупка', 'Оказание услуг', name='ad_types_enum'), nullable=False)


class Ad(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True,  autoincrement=True)
    title = Column(String(100))
    description = Column(String(500))
    type_id = Column(Integer, ForeignKey('ad_types.id'))
    user_id = Column(UUID, ForeignKey('users.id'))

    user = relationship('User', back_populates='ads')

    def __init__(self, title, description, ad_type, user):
        self.title = title
        self.description = description
        self.ad_type = ad_type
        self.user = user
