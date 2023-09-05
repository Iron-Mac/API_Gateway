from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped
import time

Base = declarative_base()


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(String)
    url = Column(String)
    output_type = Column(Integer, CheckConstraint('output_type >= 1 AND output_type <= 3'), nullable=False)
    creator: Mapped[list["User"]] = relationship("User", back_populates="modules")

    def __repr__(self):
        return f"{self.title} ({self.creator})"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    phone_number = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
    is_registerer = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    modules: Mapped[list["Module"]] = relationship("Module", back_populates="creator")
    personal_tokens = relationship("AuthToken", back_populates="user")

    def __repr__(self):
        return f"{self.username} ({self.phone_number})"


class AuthToken(Base):
    __tablename__ = "auth_token"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="personal_tokens")
    title = Column(String, index=True)
    description = Column(String)
    token = Column(String)
    expire_date = Column(DateTime)

    def __repr__(self):
        return f"{self.title} ({self.user_id})"


class UserModule(Base):
    __tablename__ = "user_module"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), primary_key=True)
    limit = Column(Integer, default=0)
    tokens = Column(Float, default=0.0)
    last_refill = Column(Float, default=time.time())
    expire_time = Column(DateTime)
