from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        func)
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True)
    hashed_password = Column(String(128))
    created_at = Column(DateTime, server_default=func.now())
    files = relationship("File", back_populates="user", lazy="noload", cascade="delete")

    __mapper_args__ = {"eager_defaults": True}


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="files")
    path = Column(String(256))
    size = Column(Integer)
    is_downloadable = Column(Boolean)
    name = Column(String(64))

    __mapper_args__ = {"eager_defaults": True}
