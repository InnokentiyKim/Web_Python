from config_new import DSN
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy import String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


engine = create_async_engine(DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    important: Mapped[bool] = mapped_column(Boolean, default=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    @property
    def dict(self):
        end_time = None
        if self.end_time is not None:
            end_time = self.end_time.isoformat()
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "important": self.important,
            "done": self.done,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
        }


ORM_OBJ = Todo
ORM_CLS = type[Todo]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
