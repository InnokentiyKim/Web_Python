from datetime import datetime
from base import Base
from typing import List
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    advs: Mapped[List["Adv"]] = relationship(back_populates="user")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at.isoformat(),
        }