import uuid

from sqlalchemy.ext.asyncio import AsyncAttrs,create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DECIMAL, DateTime, UUID, func, ForeignKey, CheckConstraint
from config import DSN
from custom_types import Role
from datetime import datetime
from typing import List


engine = create_async_engine(DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


class User(Base):
    __tablename__ = 'adv_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    role: Mapped[Role] = mapped_column(String, default="user")
    advs: Mapped[List["Adv"]] = relationship("Adv", lazy="joined", back_populates="user")
    tokens: Mapped[List["Token"]] = relationship("Token", lazy="joined", back_populates="user")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at.isoformat()
        }


class Adv(Base):
    __tablename__ = 'adv'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL, nullable=False)
    author: Mapped[int] = mapped_column(ForeignKey("adv_user.id", ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user: Mapped["User"] = relationship("User", back_populates='advs')

    __table_args__ = (
        CheckConstraint('price >= 0'),
    )

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


class Token(Base):
    __tablename__ = 'token'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, server_default=func.gen_random_uuid())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("adv_user.id", ondelete='CASCADE'))
    user: Mapped[User] = relationship("User", lazy="joined", back_populates="tokens")

    @property
    def dict(self):
        return {"token": self.token}


ORM_OBJ = Adv | User | Token
ORM_CLS = type[Adv] | type[User] | type[Token]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
