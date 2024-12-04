import datetime
from typing import List
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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
    owner: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete='CASCADE'))
    user: Mapped["User"] = relationship(back_populates="advs")
    
    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "owner_id": self.owner,
        }
    
    
class User(Base):
    
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    registered_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    advs: Mapped[List["Adv"]] = relationship(back_populates="user")
    
    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "registered_at": self.registered_at.isoformat(),
        }


    