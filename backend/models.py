from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import time

Base = declarative_base()


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(String)
    url = Column(String)
    output_type = Column(Integer, CheckConstraint('output_type >= 1 AND output_type <= 2'), nullable=False)
    creator = relationship("User", secondary="user_module", back_populates="modules")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    phone_number = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
    is_registerer = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    modules = relationship("Module", secondary="user_module", back_populates="creator")


class UserModule(Base):
    __tablename__ = "user_module"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), primary_key=True)
    limit = Column(Integer, default=0)
    tokens = Column(Float, default=0.0)
    last_refill = Column(Float, default=time.time())
    expire_time = Column(DateTime)
