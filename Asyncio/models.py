import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'secret')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'swapi')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'swapi')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class SwapiPeople(Base):
    __tablename__ = 'swapi_people'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[int] = mapped_column(Integer)
    eye_color: Mapped[str] = mapped_column(String)
    films: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)
    hair_color: Mapped[str] = mapped_column(String)
    height: Mapped[int] = mapped_column(Integer)
    homeworld: Mapped[str] = mapped_column(String)
    mass: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    skin_color: Mapped[str] = mapped_column(String)
    species: Mapped[str] = mapped_column(String)
    starships: Mapped[str] = mapped_column(String)
    vehicles: Mapped[str] = mapped_column(String)


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()








