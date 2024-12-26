from sqlalchemy.ext.asyncio import AsyncAttrs,create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DECIMAL, DateTime, func, ForeignKey
from config import DSN
from datetime import datetime


engine = create_async_engine(DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


class User(Base):
    __tablename__ = 'user'




class Adv(Base):
    __tablename__ = 'adv'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False, Index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL, nullable=False)
    author: Mapped[int] = mapped_column(ForeignKey("User", ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "author": self.author,
            "created_at": self.created_at.isoformat()
        }
