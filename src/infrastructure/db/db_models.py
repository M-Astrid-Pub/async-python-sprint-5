from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        func)
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    files = relationship("File", back_populates="user", lazy="noload")

    __mapper_args__ = {"eager_defaults": True}


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="files")
    path = Column(String)
    size = Column(Integer)
    is_downloadable = Column(Boolean)
    name = Column(String)

    __mapper_args__ = {"eager_defaults": True}
