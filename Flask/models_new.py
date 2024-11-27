import os
import datetime
from sqlalchemy import create_engine, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship


POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")


class Base(DeclarativeBase):
    
    @property
    def id_dict(self):
        return {"id": self.id}
    

class Adv(Base):
    
    __tablename__ = "adv"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[int] = mapped_column(ForeignKey("parent.id"))
    
    
class User(Base):
    
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    

    