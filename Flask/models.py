import os
import atexit
import datetime
from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")
POSTGRES_DB = os.getenv("POSTGRES_DB", "netology")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DSN)
Session = sessionmaker(engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    
    @property
    def id_dict(self):
        return {"id": self.id}
    
class User(Base):
    
    __tablename__ = "app_user"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    
    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": self.registration_time.isoformat(),
        }
        
        
Base.metadata.create_all(bind=engine)


    
    
    


